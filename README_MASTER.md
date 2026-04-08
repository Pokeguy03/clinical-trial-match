# 🏥 Clinical Trial Patient Matching — Master Reference

> **Hackathon**: Meta × Hugging Face OpenEnv Hackathon  
> **GitHub**: https://github.com/Pokeguy03/clinical-trial-match  
> **HF Space**: https://huggingface.co/spaces/GurunathM03/clinical-trial-match  
> **Author**: Gurunath M (`GurunathM03`)

---

## 🎯 What This Project Does

An **AI agent** acts as a clinical trial matching specialist. It reads patient medical records, reviews clinical trial protocols, and decides whether each patient is eligible for each trial — justifying its decisions with medical reasoning.

> **Why it matters**: 80% of clinical trials fail enrollment timelines. Manual patient screening takes weeks. This environment trains agents to automate that process.

---

## 📁 Project Structure

```
clinical_trial_match/
├── inference.py          ← AI agent that solves the task (RUN THIS)
├── openenv.yaml          ← Environment identity (name, runtime, port)
├── pyproject.toml        ← Build config & dependencies
├── uv.lock               ← Locked dependency versions
├── __init__.py           ← Exports ClinicalTrialEnv client
├── client.py             ← MCPToolClient subclass
├── models.py             ← Action/Observation type definitions
├── .gitignore            ← Ignores __pycache__, .egg-info, .env
├── README.md             ← HF Space homepage (has frontmatter)
└── server/
    ├── app.py            ← FastAPI server (create_app)
    ├── environment.py    ← 6 MCP tools + reward logic
    ├── data.py           ← 8 patients, 6 trials, ground truth
    ├── Dockerfile        ← Multi-stage Docker build
    └── requirements.txt  ← Server-only deps
```

---

## ⚙️ Environment Variables (inference.py)

```python
API_BASE_URL    = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME      = os.getenv("MODEL_NAME",   "meta-llama/Llama-3.3-70B-Instruct")
HF_TOKEN        = os.getenv("HF_TOKEN")          # NO default — required at runtime
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME") # Optional Docker image override
```

> ✅ `HF_TOKEN` has **no default** — set it at run time via `export HF_TOKEN=hf_xxx`

---

## 🛠️ The 6 MCP Tools

| Tool | Arguments | What It Does |
|------|-----------|-------------|
| `list_patients` | — | Summaries of all patients in the task |
| `get_patient_record` | `patient_id` | Full record: labs, meds, conditions, allergies |
| `list_trials` | — | Summaries of all clinical trials in the task |
| `get_trial_details` | `trial_id` | Full protocol: inclusion/exclusion criteria |
| `submit_match` | `patient_id, trial_id, eligible, reasoning` | Submit decision + get reward |
| `get_progress` | — | Current score, remaining matches, done flag |

---

## 🏆 Tasks (3 Difficulty Levels)

| Task | Patients | Trials | Decisions | Max Steps |
|------|----------|--------|-----------|-----------|
| **easy** | 3 (P001–P003) | 2 (T001–T002) | 6 | 30 |
| **medium** | 5 (P001–P005) | 3 (T001, T003–T004) | 15 | 50 |
| **hard** | 8 (P001–P008) | 4 (T001, T004–T006) | 32 | 80 |

---

## 🏅 Reward Function

| What | Points |
|------|--------|
| Correct decision (eligible/ineligible) | **+1.00** |
| Reasoning mentions key criteria | **+0.25** |
| Agent reviewed patient record first | **+0.10** |
| Agent reviewed trial protocol first | **+0.05** |
| **Max per decision** | **1.40** |

Score normalised to `0.0 – 1.0`. Success threshold = **0.60**.

---

## 🧬 Data at a Glance

### Patients (8 synthetic)
| ID | Name | Age | Key Conditions |
|----|------|-----|----------------|
| P001 | Maria Santos | 58 | Type 2 Diabetes, Hypertension |
| P002 | James Liu | 34 | Major Depressive Disorder |
| P003 | Robert Johnson | 67 | NSCLC (Lung Cancer), COPD |
| P004 | Aisha Patel | 45 | Rheumatoid Arthritis, Anemia |
| P005 | William Chen | 72 | Atrial Fibrillation, Heart Failure, CKD |
| P006 | Elena Rodriguez | 31 | Lupus, Lupus Nephritis |
| P007 | Michael Thompson | 52 | NASH, Obesity, Sleep Apnea |
| P008 | Sarah Kim | 29 | Multiple Sclerosis |

### Trials (6 realistic)
| ID | Drug | Condition | Phase |
|----|------|-----------|-------|
| T001 | Semaglutide | Type 2 Diabetes | III |
| T002 | Psilocybin | Treatment-Resistant Depression | II |
| T003 | Anti-CD20 | Rheumatoid Arthritis | III |
| T004 | Pembrolizumab | PD-L1-High NSCLC | II |
| T005 | Voclosporin | Lupus Nephritis | III |
| T006 | Resmetirom | NASH with Fibrosis | III |

---

## 🚀 How to Run

### Option 1 — Local Server + Inference
```bash
# Terminal 1: start server
cd clinical_trial_match
pip install -e .
uvicorn server.app:app --host 0.0.0.0 --port 8000

# Terminal 2: run agent
export API_BASE_URL="https://api-inference.huggingface.co/v1"
export MODEL_NAME="meta-llama/Llama-3.3-70B-Instruct"
export HF_TOKEN="hf_your_token_here"
python inference.py
```

### Option 2 — Docker
```bash
docker build -f server/Dockerfile -t clinical-trial-match:latest .
docker run -p 8000:8000 clinical-trial-match:latest

# Then in another terminal:
export ENV_BASE_URL="http://localhost:8000"
python inference.py
```

### Option 3 — Against HF Space
```bash
export API_BASE_URL="https://api-inference.huggingface.co/v1"
export MODEL_NAME="meta-llama/Llama-3.3-70B-Instruct"
export HF_TOKEN="hf_your_token_here"
export ENV_BASE_URL="https://gurunathm03-clinical-trial-match.hf.space"
python inference.py
```

---

## 📋 Stdout Log Format

```
[START] task=easy env=clinical_trial_match model=meta-llama/Llama-3.3-70B-Instruct
[STEP] step=1 action="list_patients({})" reward=0.0000 done=False
[STEP] step=2 action="get_patient_record({\"patient_id\": \"P001\"})" reward=0.0000 done=False
[STEP] step=5 action="submit_match({...})" reward=0.2143 done=False
[END] success=True steps=12 score=0.8571 rewards=[0.0, 0.0, ..., 0.8571]
```

---

## 🔑 Key Technical Choices

| Choice | Why |
|--------|-----|
| **FastMCP** | Simple `@mcp.tool` decorator to register tools in one line |
| **FastAPI + uvicorn** | Standard async web server, required by OpenEnv |
| **2-stage Dockerfile** | Builder stage installs tools; runtime stage stays lean |
| **uv.lock** | Reproducible installs across environments |
| **Pydantic v2** | Strict type validation for all actions/observations |

---

## 📊 Baseline Scores (GPT-4o-mini)

| Task | Score | Steps | Status |
|------|-------|-------|--------|
| Easy | ~0.85 | ~12 | ✅ |
| Medium | ~0.72 | ~30 | ✅ |
| Hard | ~0.55 | ~65 | ⚠️ |

---

## 🔧 Deployment Commands

```bash
# Validate before pushing
openenv validate

# Push to HF Space
openenv push . --repo-id GurunathM03/clinical-trial-match

# Push to GitHub
git add . && git commit -m "update" && git push origin main
```

---

## ✅ Submission Checklist

- [x] `API_BASE_URL` — has default
- [x] `MODEL_NAME` — has default
- [x] `HF_TOKEN = os.getenv("HF_TOKEN")` — no default
- [x] `LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")` — present
- [x] All LLM calls use `OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)`
- [x] Logs follow `[START]` / `[STEP]` / `[END]` format
- [x] GitHub repo is public
- [x] HF Space uses Docker SDK on port 8000

---

*Built for the Meta × Hugging Face OpenEnv Hackathon 🚀*
