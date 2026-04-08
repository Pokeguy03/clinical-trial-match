# 🏥 Clinical Trial Patient Matching — A Simple Guide

> **One-line explanation**: We built a training ground where AI learns to match sick patients with the right medical experiments (clinical trials) — just like a doctor would!

---

## 📖 What's the Problem?

Imagine you're sick and there's a new medicine being tested that could help you. But how do doctors know if YOU can join the experiment?

They check a **long list of rules** like:
- ✅ Are you the right age? (e.g., 18–75 years old)
- ✅ Do you have the right disease? (e.g., diabetes)
- ✅ Are your blood tests in the right range?
- ❌ Are you taking any medicines that could interfere?
- ❌ Do you have other illnesses that make it risky?

**The problem**: Real doctors spend **weeks** checking these rules for each patient. There are thousands of patients and hundreds of trials. It's slow, and 80% of clinical trials fail just because they can't find enough patients in time!

**Our solution**: Train an AI to do this matching automatically! 🤖

---

## 🎮 How Does It Work? (Think of It Like a Game)

Our project is like a **training simulator** for AI — similar to how a flight simulator trains pilots.

```
🧑‍⚕️ AI Agent (the learner)
    │
    │  Uses tools to explore:
    │  📋 "Show me the patients"
    │  📄 "Show me patient #1's medical record"
    │  🧪 "Show me the clinical trial rules"
    │  ✅ "I think Patient #1 IS eligible for Trial #1 because..."
    │
    ▼
🏥 Our Environment (the simulator)
    │
    │  Responds with:
    │  📊 Patient data, trial criteria
    │  ⭐ Score: "You got 0.85 / 1.0 — good job!"
    │
    ▼
📈 AI gets better over time!
```

---

## 🧩 What Are the Pieces?

### 1. 👤 Patients (Fake but Realistic)

We created **8 fake patients** with detailed medical records. Here's an example:

| Field | Maria Santos (P001) |
|-------|-------------------|
| Age | 58 years old |
| Sex | Female |
| Diseases | Type 2 Diabetes, High Blood Pressure |
| Medicines | Metformin 1000mg (for diabetes) |
| Blood Sugar (HbA1c) | 8.2% (higher than normal) |
| Kidney Function (eGFR) | 72 (healthy enough) |
| Allergies | Sulfonamides |

### 2. 🧪 Clinical Trials (Also Realistic)

We created **6 fake trials**. Here's one:

> **Trial T001: GLYCOMASTER-3**
> Testing a new diabetes drug (semaglutide) for people whose diabetes isn't well controlled.
>
> **To join, you MUST have:**
> - Age 18–75 ✅
> - Type 2 Diabetes for 6+ months ✅
> - HbA1c between 7.5%–10.5% ✅
> - Taking metformin ≥1000mg/day ✅
>
> **You CANNOT join if you have:**
> - Cancer ❌
> - Liver problems ❌
> - Kidney function below 60 ❌

### 3. 🤖 The AI's Job

The AI must check: **"Can Patient X join Trial Y?"**

For Maria (P001) and Trial T001:
- Age 58 → within 18–75 ✅
- Has diabetes for 6+ months ✅
- HbA1c 8.2% → within 7.5–10.5% ✅
- On metformin 1000mg ✅
- No cancer ✅
- Kidney function 72 ≥ 60 ✅

**Answer: YES, she's eligible!** 🎉

---

## ⭐ How Is the AI Scored?

The AI earns points for every decision:

| What the AI Does | Points |
|-------------------|--------|
| ✅ Correct decision (eligible or not) | **+1.0** |
| 📝 Good reasoning (mentions specific criteria) | **+0.25** |
| 👀 Actually read the patient's record first | **+0.10** |
| 📖 Actually read the trial's rules first | **+0.05** |
| ❌ Wrong decision | **+0.0** |

**Final score** = Total points earned ÷ Maximum possible points (always between 0.0 and 1.0)

---

## 📊 Three Difficulty Levels

| Level | Patients | Trials | Decisions | What Makes It Hard? |
|-------|----------|--------|-----------|-------------------|
| 🟢 **Easy** | 3 | 2 | 6 | Simple rules: "Do you have diabetes?" |
| 🟡 **Medium** | 5 | 3 | 15 | Tricky rules: blood test ranges, medicine conflicts |
| 🔴 **Hard** | 8 | 4 | 32 | Sneaky rules: "Were you diagnosed less than 6 months ago?" + red herrings |

---

## 🗂️ Project Files Explained

```
clinical_trial_match/
│
├── 📄 openenv.yaml          ← "ID card" for our environment
├── 📄 pyproject.toml         ← List of software libraries we need
├── 📄 __init__.py            ← Tells Python "this is a package"
├── 📄 client.py              ← How other programs connect to us
├── 📄 inference.py           ← Script that runs the AI against our simulator
├── 📄 README.md              ← Technical documentation
├── 📄 README_GUIDE.md        ← This file! (the simple guide)
│
└── 📁 server/                ← The brain of the simulator
    ├── 📄 app.py             ← Starts the web server
    ├── 📄 environment.py     ← The game logic (tools, scoring, rules)
    ├── 📄 data.py            ← All patient records & trial data
    ├── 📄 Dockerfile         ← Instructions to package everything in a container
    └── 📄 requirements.txt   ← Server-specific library list
```

---

## 🚀 How to Run It (Step by Step)

### Step 1: Install the tools
```bash
pip install openenv-core[core]
```

### Step 2: Go to the project folder
```bash
cd clinical_trial_match
pip install -e .
```

### Step 3: Start the simulator server
```bash
uvicorn server.app:app --host 0.0.0.0 --port 8000
```
You should see: `Uvicorn running on http://0.0.0.0:8000` ✅

### Step 4: Check it's working
Open a **new terminal** and run:
```bash
curl http://localhost:8000/health
```
You should see: `{"status":"healthy"}` ✅

### Step 5: Run the AI!
```bash
export API_BASE_URL="https://api.groq.com/openai/v1"  # Free AI provider
export MODEL_NAME="llama-3.3-70b-versatile"             # Free AI model
export HF_TOKEN="your-api-key-here"                     # Get from console.groq.com
python inference.py
```

### Step 6: Watch the AI work!
You'll see output like:
```
[STEP] step=1 action="list_patients({})" reward=0.0000
[STEP] step=2 action="get_patient_record(P001)" reward=0.0000
[STEP] step=3 action="submit_match(P001, T001, eligible=true)" reward=0.147

RESULTS SUMMARY
  easy      score=0.6940  ✅ PASS
  medium    score=0.8650  ✅ PASS
```

---

## 🔄 How the AI Talks to the Simulator

```
    AI (Agent)                          Simulator (Server)
    ─────────                           ──────────────────
         │                                     │
    1.   │──── "list_patients()" ─────────────▶│
         │◀─── P001: Maria, P002: James... ───│
         │                                     │
    2.   │──── "get_patient_record(P001)" ────▶│
         │◀─── Age 58, Diabetes, HbA1c 8.2% ──│
         │                                     │
    3.   │──── "get_trial_details(T001)" ─────▶│
         │◀─── Age 18-75, HbA1c 7.5-10.5%... ─│
         │                                     │
    4.   │──── "submit_match(P001, T001,       │
         │      eligible=true, reason=...)" ──▶│
         │◀─── reward=1.208, 5 remaining ──────│
         │                                     │
    5.   │──── ... repeats for all pairs ... ──▶│
         │◀─── Final score: 0.85 ──────────────│
```

---

## ❓ Frequently Asked Questions

**Q: Is this using real patient data?**
No! All patients are completely made up (synthetic). But they're designed to look realistic.

**Q: Can this replace real doctors?**
Not yet! This is a training simulator. In real life, doctors would review the AI's suggestions before making final decisions.

**Q: What is OpenEnv?**
OpenEnv is a framework by Meta (Facebook) that makes it easy to build training simulators for AI. Think of it as a standard format — like how all USB chargers fit the same port.

**Q: What is a Docker container?**
Imagine putting your entire computer program into a shipping container 📦. No matter what computer you open it on, it works exactly the same. That's Docker!

**Q: What does "RL" mean?**
Reinforcement Learning — teaching AI through trial and error, like how a puppy learns tricks: do it right → get a treat 🦴, do it wrong → no treat.

---

## 🏆 Our Baseline Scores

We tested with Llama-3.3-70b (a free AI model):

| Task | Score | What It Means |
|------|-------|--------------|
| 🟢 Easy | **0.694** | Got ~70% right with good reasoning |
| 🟡 Medium | **0.865** | Got ~87% right — impressive! |
| 🔴 Hard | In progress | Still being tested |

---

## 🙏 Credits

- Built using [Meta's OpenEnv](https://github.com/meta-pytorch/OpenEnv) framework
- AI inference via [Groq](https://groq.com) (free tier)
- All medical data is synthetic — no real patients were involved

---

*Made with ❤️ for the Meta × Hugging Face OpenEnv Hackathon*
