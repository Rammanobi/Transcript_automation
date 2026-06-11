import uuid
import asyncio
from typing import Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, firestore

from app.extractor import TranscriptExtractor
from app.cleaner import TranscriptCleaner
from app.chunker import TranscriptChunker
from app.map_engine import MapEngine
from app.reduce_engine import ReduceEngine
from app.validator import Validator
from app.webhook import WebhookDelivery
from app.models import Phase3Output

import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase
try:
    if not firebase_admin._apps:
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if cred_path and os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.initialize_app()
except Exception as e:
    pass

db = firestore.client()
jobs_col = db.collection("transcript_jobs")

app = FastAPI(title="Transcript Action Item Extraction System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def process_transcript_pipeline(job_id: str, raw_text: str):
    doc_ref = jobs_col.document(job_id)
    try:
        doc_ref.update({"status": "Transcript Cleaned"})
        cleaner = TranscriptCleaner()
        cleaned_text = cleaner.clean(raw_text)
        
        doc_ref.update({"status": "Chunks Generated"})
        chunker = TranscriptChunker()
        phase1_out = chunker.chunk(cleaned_text)
        
        doc_ref.update({"status": "Map Processing"})
        map_engine = MapEngine()
        phase2_out = await map_engine.process_chunks(phase1_out.chunks)
        
        doc_ref.update({"status": "Reduce Processing"})
        reduce_engine = ReduceEngine()
        phase3_out = reduce_engine.process(phase2_out)
        
        doc_ref.update({"status": "Generating Final Output"})
        final_out = Validator.validate_output(phase3_out)
        
        # Send to Webhook
        webhook_url = os.getenv("N8N_WEBHOOK_URL")
        webhook = WebhookDelivery(webhook_url=webhook_url)
        webhook_success = await webhook.deliver(final_out)
        
        doc_ref.update({
            "status": "Completed",
            "results": final_out.model_dump(),
            "webhook_status": "sent" if webhook_success else "failed"
        })
        
    except Exception as e:
        doc_ref.update({
            "status": "Failed",
            "error": str(e)
        })

@app.post("/api/v1/analyze")
async def analyze_transcript(
    background_tasks: BackgroundTasks,
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None)
):
    extractor = TranscriptExtractor()
    raw_text = ""
    
    if file:
        content = await file.read()
        if file.filename.endswith(".pdf"):
            raw_text = extractor.extract_from_pdf(content)
        elif file.filename.endswith(".docx"):
            raw_text = extractor.extract_from_docx(content)
        elif file.filename.endswith(".txt"):
            raw_text = extractor.extract_from_txt(content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format.")
    elif text:
        raw_text = extractor.extract_from_text(text)
    else:
        raise HTTPException(status_code=400, detail="Must provide either file or text input")

    job_id = str(uuid.uuid4())
    
    jobs_col.document(job_id).set({
        "status": "Transcript Loaded",
        "results": None,
        "error": None
    })
    
    background_tasks.add_task(process_transcript_pipeline, job_id, raw_text)
    
    return {"job_id": job_id, "status": "Transcript Loaded"}

@app.get("/api/v1/status/{job_id}")
async def get_status(job_id: str):
    doc = jobs_col.document(job_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = doc.to_dict()
    return {"job_id": job_id, "status": job.get("status", "Unknown"), "error": job.get("error")}

@app.get("/api/v1/results/{job_id}")
async def get_results(job_id: str):
    doc = jobs_col.document(job_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = doc.to_dict()
    if job.get("status") != "Completed":
        raise HTTPException(status_code=400, detail="Job not completed yet")
        
    return {
        "status": "success",
        "webhook_status": job.get("webhook_status", "unknown"),
        "results": job.get("results")
    }
