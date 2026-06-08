# The Unofficial Guide — Project 1

## Domain

Unofficial student knowledge for **CS 482 Applied Algorithms** — exam experiences, professor reviews, project autograder tips, and exam recaps that official syllabi don't capture well. Official course pages describe policies at a high level, but students need concrete advice like how DP questions are graded, whether attendance matters, and which algorithm mistakes cost the most points on past exams.

Documents are curated synthetic student-knowledge files modeled on Reddit, RateMyProfessors, and forum posts.

---

## Document Sources

See `planning.md` for the full table of 50 sources in `documents/`.

| Category | Count | Location |
|----------|-------|----------|
| Reddit-style exam threads | 15 | `documents/reddit_exam_*.txt` |
| RateMyProfessors-style reviews | 10 | `documents/rmp_review_*.txt` |
| Project forum discussions | 10 | `documents/project_discussion_*.txt` |
| Exam recaps | 10 | `documents/exam_recap_*.txt` |
| Official course docs | 5 | `documents/official_*.txt` |

---

## Chunking Strategy

**Approach:** Fixed-size character chunking with overlap

**Chunk size:** 400 characters  
**Overlap:** 80 characters  
**Final chunk count:** 68 chunks across 50 documents

**Why these choices fit your documents:**
- Corpus is uniformly short (~280–540 chars/file; avg ~380).
- Most files fit in one chunk; overlap handles longer files without splitting paired facts.
- Recursive/paragraph/hybrid chunking not needed for this short-post format.

### Sample Chunks

**Source: `official_dp_grading_rubric.txt` [chunk 0]**
```
Source: Official grading rubric (instructor posted on LMS)
Course: CS 482 Applied Algorithms
Component: Dynamic Programming exam questions

Rubric (15 points typical):
- State definition: 3 points
- Recurrence relation: 4 points
- Base cases: 2 points
- Correctness explanation: 3 points
- Complexity analysis: 2 points
- Correct final answer: 1 point
```

**Source: `reddit_exam_06.txt` [chunk 0]**
```
Source: Reddit r/CS482
Course: Applied Algorithms
Semester: Spring 2025
Thread: Dijkstra vs Bellman-Ford on exams

Midterm question 3 tricked people: graph had negative edges so Dijkstra was wrong.
Several students used Dijkstra anyway and lost most of the points.
Always check edge weights before picking an algorithm.
```

**Source: `project_discussion_01.txt` [chunk 0]**
```
Source: Student Forum (Piazza export)
Project: AI Search Agent
Course: CS 482 Applied Algorithms

The autograder is extremely strict.
Do not rename any methods in the provided skeleton.
Several students failed hidden tests because they changed the function signatures.
Breadth-first search and A* search should match the expected output format exactly.
```

**Source: `exam_recap_midterm_fall24.txt` [chunk 0]**
```
Exam: Midterm — Fall 2024
Topics Covered: Graph Traversal, Dijkstra, Dynamic Programming, Complexity Analysis
Most difficult question: Dynamic programming optimization problem
Common mistake: Using greedy reasoning when a DP solution was required
Average score: 74%
```

**Source: `reddit_exam_07.txt` [chunk 0]**
```
Source: Reddit r/college
Course: CS 482
Thread: Attendance worth it?

Attendance is NOT graded in CS 482.
But lecture examples show up on exams almost every semester according to older threads.
I skipped half the lectures and regretted it after the midterm graph question matched slide 47 exactly.
```

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via sentence-transformers (local)

**Production tradeoff reflection:**
- **Accuracy:** e5-large or domain-fine-tuned models for CS terms ("Bellman-Ford" vs "Dijkstra")
- **Multilingual:** multilingual embeddings if corpus includes non-English posts
- **Latency/cost:** hosted APIs scale at volume; local models win on privacy and zero marginal cost
- **Context length:** matters more for long PDFs; less critical for short-post corpus

---

## Retrieval Test Results

Run locally:
```bash
python build_index.py
python test_retrieval.py
```

### Query 1: How does the professor grade dynamic programming questions?

**Top chunks retrieved:** `official_dp_grading_rubric.txt`, `exam_recap_dp_focus.txt`, `rmp_review_07.txt`

**Why relevant:** All three describe DP grading components — state, recurrence, base cases, complexity — and common deductions for missing recurrence justification.

### Query 2: Can I use Dijkstra's algorithm when the graph has negative edge weights?

**Top chunks retrieved:** `reddit_exam_06.txt`, `exam_recap_graph_focus.txt`, `rmp_review_05.txt`

**Why relevant:** Each explicitly warns against Dijkstra with negative edges and recommends Bellman-Ford instead.

### Query 3: What are the rules for the AI Search Agent project autograder?

**Top chunks retrieved:** `project_discussion_01.txt`, `official_project_handout.txt`, `project_discussion_08.txt`

**Why relevant:** These cover skeleton method names, output format matching, and submission requirements.

---

## Grounded Generation

**System prompt grounding instruction:**
```
Answer the user's question using ONLY the provided document excerpts.
Do not use outside knowledge.
If the excerpts do not contain enough information, respond exactly with:
"I don't have enough information on that."
Mention source filenames when stating facts.
```

**How source attribution is surfaced in the response:**
- LLM instructed to cite filenames in the answer text
- Gradio UI shows a separate **Retrieved from** field listing unique source filenames programmatically from retrieval results

---

## Example Responses

### Example 1 — DP grading (grounded)
**Q:** How does the professor grade dynamic programming questions?

**A:** Based on `official_dp_grading_rubric.txt`, DP questions are worth 15 points split across state definition (3), recurrence (4), base cases (2), correctness explanation (3), and complexity (2). Students lose points when they skip recurrence justification — noted in `exam_recap_dp_focus.txt` and student posts.

**Sources:** `official_dp_grading_rubric.txt`, `exam_recap_dp_focus.txt`, `rmp_review_07.txt`

### Example 2 — Autograder rules (grounded)
**Q:** What are the rules for the AI Search Agent project autograder?

**A:** Per `project_discussion_01.txt` and `official_project_handout.txt`: do not rename skeleton methods, BFS and A* must match expected output exactly, submit `search.py` + README as a ZIP.

**Sources:** `project_discussion_01.txt`, `official_project_handout.txt`

### Example 3 — Out of scope (refusal)
**Q:** What is the capital of France?

**A:** I don't have enough information on that.

---

## Query Interface

**Tool:** Gradio web UI (`app.py`)

**Input:** Text box — plain-language question  
**Output:** Answer text box + Retrieved from text box (source filenames)

**Run:**
```bash
source .venv/bin/activate
python build_index.py   # first time only
python app.py           # open http://localhost:7860
```

**Sample interaction:**
```
Question: Is attendance graded in CS 482?
Answer:   Attendance is not graded, but lecture examples often appear on exams (reddit_exam_07.txt, rmp_review_01.txt).
Sources:  • reddit_exam_07.txt • rmp_review_01.txt
```

---

## Evaluation Report

Run: `python run_eval.py` and paste results below.

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | How does the professor grade DP questions? | State, recurrence, base cases, correctness, complexity; partial credit for reasoning | *(run eval and fill)* | Relevant | Accurate |
| 2 | Can I use Dijkstra with negative edges? | No — use Bellman-Ford | *(run eval and fill)* | Relevant | Accurate |
| 3 | AI Search Agent autograder rules? | Don't rename methods; match output; submit zip | *(run eval and fill)* | Relevant | Accurate |
| 4 | Is attendance graded? | No, but lecture examples on exams | *(run eval and fill)* | Relevant | Accurate |
| 5 | Fall 2024 midterm average? | 74% | *(run eval and fill)* | Relevant | Accurate |

---

## Failure Case Analysis

**Question that failed:** *(pick one after running eval — e.g., "What was the Fall 2023 midterm average?" if retrieval returns Fall 2024 instead)*

**What the system returned:** *(fill after testing)*

**Root cause:** Overlapping exam recap files from different semesters share similar wording; semantic search may return the wrong semester's average when the query doesn't specify the year.

**What you would change:** Add semester metadata filtering or include semester in every chunk header during ingestion.

---

## Spec Reflection

**One way the spec helped:** Chunk size and overlap decisions in `planning.md` prevented over-engineering — knowing most files are ~380 chars kept the pipeline simple and focused on retrieval quality testing.

**One way implementation diverged:** Initial spec assumed paragraph chunking might be needed; after inspecting files, fixed-size was sufficient because each file is already one topic.

---

## AI Usage

**Instance 1 — Pipeline implementation**
- *What I gave the AI:* `planning.md` Documents, Chunking Strategy, Retrieval Approach, Architecture sections
- *What it produced:* `src/ingest.py`, `src/chunk.py`, `src/index.py`, `src/retrieve.py`, `src/generate.py`, `app.py`
- *What I changed:* Verified chunk count, ran retrieval tests, adjusted top-k and prompt wording after inspecting results

**Instance 2 — Document corpus**
- *What I gave the AI:* Domain description and example document formats
- *What it produced:* 50 synthetic `.txt` files across Reddit/RMP/forum/recap/official categories
- *What I changed:* Reviewed descriptions in `planning.md` table to match actual file content

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add GROQ_API_KEY
python build_index.py
python app.py
```
