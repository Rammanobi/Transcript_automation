# Problem Constraints
# Problem Constraints Document

## Project Name

Meeting Transcript Action Item Extraction System

---

# 1. Problem Statement

Build an AI-powered system that accepts meeting transcripts and automatically extracts actionable tasks using a Map-Reduce architecture.

The system must:

* Accept meeting transcripts from multiple input sources.
* Analyze the transcript.
* Extract explicit and implicit action items.
* Preserve ownership, priority, deadlines, and context.
* Generate a final validated JSON output.
* Send the final output to an n8n webhook.

This phase does NOT include Jira or Slack implementation.

Those systems will be integrated later.

---

# 2. Core Objective

Input:

Meeting Transcript

Output:

Validated Action Item JSON

Example:

```json
{
  "title": "Update Landing Page",
  "assignee": "Sarah",
  "priority": "High",
  "due_context": "Friday"
}
```

---

# 3. Supported Inputs

The application must support:

### Input Type 1

Plain text transcript

Example:

```text
Sarah: Update the landing page.
John: I will do it by Friday.
```

### Input Type 2

PDF

Extract text using:

PyMuPDF

### Input Type 3

DOCX

Extract text using:

python-docx

No other formats are required.

---

# 4. Non-Goals

The following are explicitly out of scope:

* Embeddings
* Vector databases
* Pinecone
* ChromaDB
* FAISS
* RAG
* Semantic search
* Historical transcript search
* Multi-document retrieval
* Agentic workflows
* Jira integration
* Slack integration

Reason:

The system processes a single transcript and analyzes the entire document.

Retrieval systems are unnecessary.

---

# 5. Architecture Decision

Selected Architecture:

Map-Reduce

Reason:

Action items may appear anywhere in the transcript.

Chunk overlap prevents boundary information loss.

Map-Reduce provides higher extraction completeness.

---

# 6. High-Level Architecture

```text
Transcript Input
       ↓
Extraction
       ↓
Cleaning
       ↓
Dynamic Chunking
       ↓
Map Processing
       ↓
Reduce Processing
       ↓
Validation
       ↓
Final JSON
       ↓
n8n Webhook
```

---

# 7. Technology Stack

Backend:

* Python
* FastAPI

Frontend:

* Minimal HTML/CSS frontend
  OR
* Minimal React frontend

LLM:

* Gemini

Future Compatible:

* Claude
* OpenAI
* DeepSeek

Transcript Extraction:

* PyMuPDF
* python-docx

Chunking:

* LangChain RecursiveCharacterTextSplitter

Similarity Matching:

* RapidFuzz

Webhook:

* n8n

---

# 8. Input Size Assumptions

Target Meeting Length:

10–15 minutes

Expected Transcript Size:

2000–2400 words

System must also support:

* 500 words
* 1000 words
* 5000 words
* 10000+ words

Chunking must scale automatically.

No hardcoded chunk count.

---

# 9. Dynamic Chunking Constraints

Do not use:

```python
text.split()
```

as the final chunking solution.

Reason:

Sentence boundaries may be broken.

Use:

```python
RecursiveCharacterTextSplitter
```

from:

```python
langchain-text-splitters
```

---

# 10. Chunking Requirements

Target chunk size:

Approximately 500 words

Target overlap:

Approximately 100 words

Requirements:

* Dynamic chunk generation
* No fixed chunk count
* Overlap preservation
* Context preservation

Example:

```text
Chunk 1
Words 1–500

Chunk 2
Words 401–900

Chunk 3
Words 801–1300
```

---

# 11. Transcript Cleaning Requirements

Cleaning layer must:

* Remove excessive spaces
* Normalize line breaks
* Remove empty lines
* Preserve speaker labels
* Preserve timestamps
* Remove extraction artifacts
* Preserve sentence boundaries
* Preserve paragraph boundaries

Example:

Before:

```text
Sarah      will     update
the page
```

After:

```text
Sarah will update the page
```

---

# 12. Map Phase Requirements

Each chunk must be processed independently.

Map phase responsibilities:

* Extract action items
* Extract assignee
* Extract deadlines
* Extract priority
* Extract supporting context
* Generate confidence score

Each chunk returns JSON only.

Example:

```json
{
  "title": "",
  "description": "",
  "assignee": "",
  "priority": "",
  "due_context": "",
  "chunk_id": 1,
  "confidence": 0.91
}
```

---

# 13. API Execution Strategy

Do not process all chunks simultaneously.

Use Hybrid Execution.

Example:

Wave 1:

* Chunk 1
* Chunk 2

Parallel

Wave 2:

* Chunk 3
* Chunk 4

Parallel

Wave 3:

* Chunk 5
* Chunk 6

Parallel

Reason:

* Lower latency
* Safer rate limits
* Easier debugging

---

# 14. Retry Strategy

All LLM calls must support:

* Retry
* Exponential Backoff

Retry Pattern:

```text
Attempt 1
↓
1 second

Attempt 2
↓
2 seconds

Attempt 3
↓
4 seconds

Attempt 4
↓
8 seconds

Attempt 5
↓
Fail
```

Maximum retries:

5

---

# 15. Failure Handling

A failed chunk must not fail the entire transcript.

Example:

```text
Chunk 1 = Success
Chunk 2 = Success
Chunk 3 = Failed
Chunk 4 = Success
```

Workflow continues.

Failed chunks must be logged.

---

# 16. Reduce Phase Requirements

Responsibilities:

* Flatten chunk outputs
* Normalize text
* Detect duplicates
* Merge duplicates
* Resolve assignees
* Resolve deadlines
* Resolve priorities
* Aggregate confidence scores
* Validate final actions

---

# 17. Duplicate Detection

Use:

RapidFuzz

Do not use:

* Embeddings
* Vector similarity

Reason:

Expected action item count is small.

RapidFuzz is simpler and faster.

Target similarity threshold:

85%

---

# 18. Validation Requirements

Every action item must contain:

* Title
* Description

Optional:

* Assignee
* Due date
* Priority

Action items must be actionable.

Bad:

```text
Landing Page
```

Good:

```text
Update Landing Page
```

---

# 19. Final Output Format

```json
{
  "transcript_id": "TR-001",
  "total_chunks": 6,
  "total_raw_items": 22,
  "final_action_items": 8,
  "actions": [
    {
      "action_id": "ACT-001",
      "title": "Update Landing Page",
      "description": "Update homepage content",
      "assignee": "Sarah",
      "priority": "High",
      "due_context": "Friday",
      "confidence": 0.91,
      "source_chunks": [1, 2]
    }
  ]
}
```

---

# 20. System Boundary

This project ends at:

```text
Validated JSON
       ↓
n8n Webhook
```

Jira creation and Slack notification are separate implementation phases and must not be included in the current system scope.

---

# 21. Success Criteria

The system is considered successful when:

* Transcript extraction works.
* Cleaning works.
* Dynamic chunking works.
* Chunk overlap works.
* Map processing works.
* Retry handling works.
* Reduce processing works.
* Validation works.
* Final JSON is generated.
* Final JSON is delivered to n8n webhook.

END OF DOCUMENT
