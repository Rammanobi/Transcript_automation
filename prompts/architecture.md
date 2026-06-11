# Architecture
flowchart TD

A[PDF / DOCX / Text Input]
--> B[Text Extraction]

B --> C[Transcript Cleaning]

C --> D[RecursiveCharacterTextSplitter]

D --> E1[Chunk 1]
D --> E2[Chunk 2]
D --> E3[Chunk 3]
D --> EN[Chunk N]

E1 --> F[Map Phase]
E2 --> F
E3 --> F
EN --> F

F --> G[Collect Raw Action Items]

G --> H[Reduce Engine]

H --> I[Deduplication]

I --> J[Ownership Resolution]

J --> K[Deadline Resolution]

K --> L[Priority Resolution]

L --> M[Confidence Aggregation]

M --> N[Validation Pass]

N --> O[Final Action Item JSON]

O --> P[n8n Webhook]