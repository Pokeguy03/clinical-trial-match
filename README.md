---
title: Clinical Trial Patient Matching
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
---

# 🏥 Clinical Trial Patient Matching — OpenEnv Environment

An AI agent reviews patient medical records and determines eligibility for clinical trials by evaluating inclusion/exclusion criteria against detailed patient data.

> **Why this matters**: 80% of clinical trials fail to meet enrollment timelines. Manual patient screening takes weeks per site. This environment trains agents to automate the matching process — a genuine, high-impact healthcare task.

## 🎯 Environment Overview

The agent operates as a **clinical trial matching specialist**:

1. **Browse** patients and trials via summaries
2. **Review** detailed medical records and trial protocols
3. **Evaluate** each inclusion/exclusion criterion against patient data
4. **Submit** eligibility decisions with medical reasoning
5. **Earn rewards** based on accuracy, reasoning quality, and thoroughness

## 🛠️ Action Space (MCP Tools)

| Tool | Arguments | Description |
|------|-----------|-------------|
| `list_patients` | — | Patient summaries (ID, name, age, sex, conditions) |
| `get_patient_record` | `patient_id` | Full record: demographics, conditions, labs, meds, allergies, history |
| `list_trials` | — | Trial summaries (ID, title, phase, condition) |
| `get_trial_details` | `trial_id` | Full protocol: inclusion/exclusion criteria, endpoints, duration |
| `submit_match` | `patient_id, trial_id, eligible, reasoning` | Submit eligibility decision |
| `get_progress` | — | Current score, matches remaining, review status |

## 📊 Observation Space

Each observation includes:
- **Tool result**: JSON response from the called tool
- **Reward**: Normalized cumulative score (0.0–1.0)
- **Done**: Whether episode is complete
- **Metadata**: Task info, progress counters, final scores

## 🏆 Tasks (Easy → Medium → Hard)

| Task | Patients | Trials | Decisions | Description |
|------|----------|--------|-----------|-------------|
| **Easy** | 3 | 2 | 6 | Clear-cut criteria: age ranges, specific diagnoses, obvious labs |
| **Medium** | 5 | 3 | 15 | Lab value ranges, medication conflicts, comorbidity checks, disease scores |
| **Hard** | 8 | 4 | 32 | Temporal criteria, drug washout periods, biomarker thresholds, edge cases |

### Reward Function

| Component | Points | Description |
|-----------|--------|-------------|
| Decision correctness | +1.0 | Correct eligible/ineligible determination |
| Reasoning quality | +0.25 | References correct key criteria in reasoning |
| Patient review bonus | +0.10 | Agent reviewed patient record before deciding |
| Trial review bonus | +0.05 | Agent reviewed trial protocol before deciding |

**Max per decision**: 1.40 · **Episode score**: Normalized to 0.0–1.0

## 🚀 Setup & Usage

### Prerequisites

- Python 3.10+
- Docker
- `pip install openenv-core[core]`

### Quick Start (Local)

```bash
# Clone and install
cd clinical_trial_match
pip install -e .

# Run server
uvicorn server.app:app --host 0.0.0.0 --port 8000

# In another terminal, interact via Python
python -c "
from clinical_trial_match import ClinicalTrialEnv
with ClinicalTrialEnv(base_url='http://localhost:8000').sync() as env:
    result = env.reset(task='easy')
    print(result.observation.metadata)
    tools = env.list_tools()
    print([t.name for t in tools])
"
```

### Docker

```bash
cd clinical_trial_match
docker build -f server/Dockerfile -t clinical-trial-match:latest .
docker run -p 8000:8000 clinical-trial-match:latest
```

### Run Inference

```bash
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4o-mini"
export HF_TOKEN="your-api-key"

python inference.py
```

## 📈 Baseline Scores

| Task | Score | Steps | Status |
|------|-------|-------|--------|
| Easy | ~0.85 | ~12 | ✅ |
| Medium | ~0.72 | ~30 | ✅ |
| Hard | ~0.55 | ~65 | ⚠️ |

*Scores with GPT-4o-mini. Frontier models (GPT-4o, Claude Sonnet) expected to score higher.*

## 🏗️ Architecture

```
clinical_trial_match/
├── openenv.yaml          # OpenEnv manifest
├── pyproject.toml        # Dependencies
├── __init__.py           # Package exports
├── client.py             # MCPToolClient subclass
├── inference.py          # Baseline inference script
├── README.md             # This file
└── server/
    ├── app.py            # FastAPI application
    ├── environment.py    # MCPEnvironment with 6 tools
    ├── data.py           # Patient records, trials, ground truth
    ├── Dockerfile        # Container definition
    └── requirements.txt  # Server dependencies
```

## 🔬 Medical Domain Details

### Patient Profiles

8 synthetic patients spanning conditions:
- Type 2 Diabetes, Hypertension, Hyperlipidemia
- Major Depressive Disorder, Generalized Anxiety
- Non-Small Cell Lung Cancer, COPD
- Rheumatoid Arthritis, Iron Deficiency Anemia
- Atrial Fibrillation, Heart Failure, CKD
- Systemic Lupus Erythematosus, Lupus Nephritis
- NASH, Obesity, Obstructive Sleep Apnea
- Relapsing-Remitting Multiple Sclerosis

### Clinical Trial Protocols

6 realistic trials:
- **T001**: Semaglutide for T2DM (Phase III)
- **T002**: Psilocybin for Treatment-Resistant Depression (Phase II)
- **T003**: Anti-CD20 for Rheumatoid Arthritis (Phase III)
- **T004**: Pembrolizumab for PD-L1-High NSCLC (Phase II)
- **T005**: Voclosporin for Lupus Nephritis (Phase III)
- **T006**: Resmetirom for NASH with Fibrosis (Phase III)

## 📜 License

MIT
