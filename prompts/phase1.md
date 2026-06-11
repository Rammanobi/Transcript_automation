# Phase 1
PHASE 1 — TRANSCRIPT INGESTION, EXTRACTION, CLEANING, AND DYNAMIC CHUNKING

PROJECT OBJECTIVE

Build a transcript-processing system that accepts meeting transcripts from text input, PDF files, or DOCX files and prepares them for Map-Reduce processing.

This phase ends when a clean set of dynamically generated overlapping chunks is produced and ready for LLM processing.

Do NOT implement Jira, Slack, Reduce logic, embeddings, vector databases, RAG, ticket creation, or notification systems in this phase.

==================================================
FINAL ARCHITECTURE DECISIONS (LOCKED)
=====================================

Backend:

* Python
* FastAPI

Frontend:

* Simple HTML/CSS frontend OR minimal React frontend
* User can:

  * Paste transcript text
  * Upload PDF
  * Upload DOCX

LLM:

* Gemini API (can be swapped later)

Chunking Strategy:

* LangChain RecursiveCharacterTextSplitter

Chunk Type:

* Dynamic chunking

Chunk Target:

* Approximately 500 words per chunk

Overlap:

* Approximately 100 words

Processing Pattern:

* Map-Reduce

Embeddings:

* Not used

Vector Database:

* Not used

RAG:

* Not used

Reason:
This system processes the entire transcript and does not perform semantic retrieval. Therefore embeddings and vector databases add unnecessary complexity.

==================================================
USER FLOW
=========

Step 1

User opens application.

Application displays:

* Upload PDF
* Upload DOCX
* Paste Transcript

User chooses one option.

User presses:

ANALYZE

==================================================
SUPPORTED INPUTS
================

Input Type 1

Raw Transcript Text

Example:

Sarah: We need to update the landing page.
John: I will handle that before Friday.

Input Type 2

PDF

Use:

PyMuPDF

Package:

pip install pymupdf

Extraction Goal:

Convert PDF contents into plain text.

Output:

String

Input Type 3

DOCX

Use:

python-docx

Package:

pip install python-docx

Extraction Goal:

Convert DOCX contents into plain text.

Output:

String

==================================================
TRANSCRIPT EXTRACTION LAYER
===========================

Create a Transcript Extraction Service.

Responsibilities:

1. Detect file type.
2. Extract text.
3. Return plain text.

Output Format:

{
"transcript_text": "complete extracted transcript"
}

No cleaning yet.

No chunking yet.

Only extraction.

==================================================
TRANSCRIPT CLEANING LAYER
=========================

Create a Transcript Cleaning Service.

Purpose:

Normalize transcript before chunking.

Cleaning Rules:

1. Remove excessive spaces.

Example:

"We     need     updates"

Becomes:

"We need updates"

2. Normalize line breaks.

3. Remove empty lines.

4. Preserve speaker labels.

Example:

Sarah:
John:

Must remain intact.

5. Preserve timestamps if present.

Example:

[00:12:05]

Should remain.

6. Remove extraction artifacts from PDF conversion.

7. Preserve sentence boundaries.

8. Preserve paragraph boundaries whenever possible.

Output:

{
"clean_transcript": "normalized transcript"
}

==================================================
WHY SPLIT() IS NOT USED
=======================

Do not use:

text.split()

Reason:

Simple split can cut sentences in the middle.

Example:

Chunk 1:
Sarah will update the landing page and

Chunk 2:
finish the work by Friday.

Meaning becomes fragmented.

Future transcripts may be significantly larger.

Production systems require preserving semantic structure.

==================================================
CHUNKING ENGINE
===============

Use:

RecursiveCharacterTextSplitter

Package:

pip install langchain-text-splitters

Import:

from langchain_text_splitters import RecursiveCharacterTextSplitter

Purpose:

Create meaningful chunks while preserving context.

==================================================
CHUNKING CONFIGURATION
======================

Target Chunk Size:

Approximately 500 words.

Target Overlap:

Approximately 100 words.

Implementation Notes:

RecursiveCharacterTextSplitter operates primarily on characters.

Tune chunk_size and chunk_overlap so resulting chunks are approximately:

500 words

with

100 word overlap

Expected Chunk Count:

Transcript:
2000 words

Result:
5–6 chunks

Transcript:
2400 words

Result:
6–7 chunks

Transcript:
800 words

Result:
2 chunks

Transcript:
10000 words

Result:
Automatically scales.

No hardcoded chunk count.

==================================================
DYNAMIC CHUNKING REQUIREMENTS
=============================

System must:

Automatically calculate chunk count.

Never assume transcript length.

Never hardcode:

5 chunks
6 chunks
10 chunks

Chunk count must be generated dynamically from transcript size.

Example:

Transcript Length:
2200 words

Possible Output:

Chunk 1
Chunk 2
Chunk 3
Chunk 4
Chunk 5
Chunk 6

Generated automatically.

==================================================
OVERLAP REQUIREMENTS
====================

Chunk overlap must be maintained.

Purpose:

Prevent action items from being lost at chunk boundaries.

Example:

Chunk 1:
"...Sarah will update the landing page"

Chunk 2:
"Sarah will update the landing page before Friday"

The overlap ensures context survives splitting.

==================================================
OUTPUT OF PHASE 1
=================

Phase 1 ends with:

{
"transcript_length": 2200,
"chunk_count": 6,
"chunks": [
{
"chunk_id": 1,
"content": "..."
},
{
"chunk_id": 2,
"content": "..."
}
]
}

No LLM processing.

No Map stage.

No Reduce stage.

No Jira.

No Slack.

Only:

Input
→ Extraction
→ Cleaning
→ Dynamic Chunking

==================================================
SUCCESS CRITERIA
================

Phase 1 is complete when:

1. User can upload PDF.
2. User can upload DOCX.
3. User can paste transcript text.
4. Transcript is extracted.
5. Transcript is cleaned.
6. RecursiveCharacterTextSplitter generates dynamic chunks.
7. Overlap is preserved.
8. Chunk count adjusts automatically.
9. Final chunk JSON is returned.
10. System is ready for Map Processing.

END OF PHASE 1
