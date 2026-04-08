# 🔧 Technical Deep Dive — Why Groq & Hugging Face?

> This document explains **why** we chose each technology, **what** it does in our project, and **how** the entire system works end-to-end.

---

## 🧠 The Big Picture

Our project has **3 main parts** that work together:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│   GROQ API      │     │  OUR ENVIRONMENT │     │  HUGGING FACE       │
│   (The Brain)   │◄───►│  (The Simulator) │     │  (The Cloud Host)   │
│                 │     │                  │     │                     │
│ Runs the AI     │     │ Scores the AI    │     │ Hosts everything    │
│ model that      │     │ decisions and    │     │ online so anyone    │
│ makes medical   │     │ provides patient │     │ can access and      │
│ decisions       │     │ data + trial     │     │ test our project    │
│                 │     │ protocols        │     │                     │
└─────────────────┘     └──────────────────┘     └─────────────────────┘
```

---

## 🤖 Why Groq API?

### What is Groq?

Groq is a **free AI inference platform** that runs large language models (LLMs) extremely fast. Think of it as a supercomputer that can run AI models — and they offer a free tier for developers.

### Why NOT OpenAI?

| Factor | OpenAI (GPT-4o-mini) | Groq (Llama-3.3-70B) |
|--------|----------------------|----------------------|
| **Cost** | 💰 Paid ($5 minimum) | ✅ **Completely free** |
| **Speed** | 🐌 ~2-3 seconds/response | ⚡ **~0.3 seconds/response** |
| **Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ (nearly as good) |
| **API Format** | OpenAI standard | ✅ **OpenAI-compatible** |
| **Rate Limits** | Higher limits | Lower (but enough for demo) |
| **Sign-up** | Credit card needed | ✅ **No credit card** |

### Why we chose Groq:
1. **Free for hackathons** — No budget needed, anyone can reproduce our results
2. **OpenAI-compatible API** — Same code works with OpenAI, Groq, or any other provider. Just change the URL!
3. **Fast inference** — Groq's custom LPU chips are 10x faster than GPUs for inference
4. **Strong model** — Llama-3.3-70B scores competitively with GPT-4o-mini on medical reasoning

### How we use Groq in our code:

```python
# inference.py — This is ALL it takes to switch providers!

# For Groq (free):
API_BASE_URL = "https://api.groq.com/openai/v1"
MODEL_NAME = "llama-3.3-70b-versatile"

# For OpenAI (paid):
# API_BASE_URL = "https://api.openai.com/v1"
# MODEL_NAME = "gpt-4o-mini"

# The rest of the code is IDENTICAL — that's the beauty of OpenAI-compatible APIs
client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
```

### How to get a Groq API key:

1. Go to **https://console.groq.com** → Sign up (free, no credit card)
2. Click **API Keys** in the sidebar
3. Click **Create API Key** → Copy the key (starts with `gsk_...`)
4. Set it as an environment variable:
   ```bash
   export HF_TOKEN="gsk_your-key-here"
   ```

---

## 🤗 Why Hugging Face Spaces?

### What is Hugging Face?

Hugging Face is the **GitHub for AI** — it's the largest platform for sharing AI models, datasets, and applications. **Hugging Face Spaces** is their free hosting service for AI demos.

### Why we need it:

Our project is a **server** that needs to run somewhere. Without hosting:
- ❌ Only works on YOUR computer
- ❌ Hackathon judges can't access it
- ❌ No one else can test it
- ❌ You'd need to keep your laptop running 24/7

With Hugging Face Spaces:
- ✅ **Free hosting** — Runs in the cloud at no cost
- ✅ **Always online** — Judges can access anytime
- ✅ **Docker support** — Runs our exact container
- ✅ **Public URL** — Anyone can access your environment
- ✅ **Required by OpenEnv** — The hackathon framework is built to deploy to HF

### What gets deployed:

```
Your computer                          Hugging Face Cloud
─────────────                          ──────────────────
clinical_trial_match/
├── server/
│   ├── Dockerfile  ──────────────────► Docker container gets built
│   ├── app.py      ──────────────────► FastAPI server starts
│   ├── environment.py ───────────────► MCP tools become available
│   └── data.py     ──────────────────► Patient/trial data loads
├── inference.py    ──────────────────► Available for download
└── README.md       ──────────────────► Becomes the Space's homepage
                                        │
                                        ▼
                                   Live at:
                    https://huggingface.co/spaces/GurunathM03/clinical-trial-match
```

### How the deployment works (what `openenv push` does):

```
Step 1: Validate     → Checks openenv.yaml, models.py, Dockerfile exist
Step 2: Authenticate → Uses your HF token to verify identity
Step 3: Create Space → Creates a new HF Space (like a GitHub repo)
Step 4: Upload Files → Sends all project files to HF
Step 5: Build Image  → HF builds the Docker container in cloud
Step 6: Start Server → Container starts, server goes live on port 8000
Step 7: Live! 🎉     → Space is accessible at your public URL
```

### How to get a Hugging Face token:

1. Go to **https://huggingface.co/join** → Create account
2. Go to **https://huggingface.co/settings/tokens**
3. Click **New token** → Name: "hackathon" → Role: **Write**
4. Copy the token (starts with `hf_...`)

---

## 🔄 How Everything Connects (Full Flow)

Here's the complete end-to-end flow when the inference script runs:

```
YOU (Developer)
│
│ Step 1: Start the server (locally or on HF Spaces)
│ Command: uvicorn server.app:app --port 8000
▼
┌─────────────────────────────────────────────────────────┐
│                    OUR SERVER (Port 8000)                │
│                                                         │
│  FastAPI App → MCPEnvironment → 6 MCP Tools             │
│  • 8 patient records (synthetic)                        │
│  • 6 clinical trials (synthetic)                        │
│  • Ground truth eligibility matrix                      │
│  • Reward calculator (accuracy + reasoning + review)    │
└───────────────────────┬─────────────────────────────────┘
                        │ WebSocket connection
                        │
YOU (Developer)         │
│                       │
│ Step 2: Run inference │
│ Command: python inference.py
▼                       │
┌───────────────────────┴─────────────────────────────────┐
│                   INFERENCE SCRIPT                       │
│                                                         │
│  1. Connects to our server via WebSocket                │
│  2. Calls env.reset(task="easy")                        │
│  3. Sends task description to LLM                       │
│  4. LLM decides which tool to call                      │
│  5. Script executes tool on server                      │
│  6. Result goes back to LLM                             │
│  7. Repeat until all matches submitted                  │
│  8. Print final scores                                  │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTPS API calls
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                     GROQ API                            │
│                                                         │
│  Model: Llama-3.3-70B-Versatile                         │
│  • Receives patient data + trial criteria               │
│  • Reasons about eligibility                            │
│  • Returns tool calls (which tool + arguments)          │
│  • Provides medical reasoning for each decision         │
│                                                         │
│  Example response:                                      │
│  "Call submit_match(P001, T001, eligible=true,          │
│   reasoning='Patient has T2DM, HbA1c 8.2% within       │
│   7.5-10.5% range, on metformin 1000mg...')"            │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Our Results

Using Groq (Llama-3.3-70B, completely free):

| Task | Patients × Trials | Score | Time | Verdict |
|------|-------------------|-------|------|---------|
| 🟢 Easy | 3 × 2 = 6 | **0.694** (69.4%) | ~5 sec | ✅ PASS |
| 🟡 Medium | 5 × 3 = 15 | **0.865** (86.5%) | ~15 sec | ✅ PASS |
| 🔴 Hard | 8 × 4 = 32 | In progress | ~60 sec | ⏳ |

### What the scores mean:
- **0.694** = The AI got ~70% of decisions correct with some reasoning quality
- **0.865** = The AI got ~87% correct — it actually reviewed records carefully and cited specific criteria
- The medium score is HIGHER than easy because the AI learned from the pattern and was more thorough

---

## ❓ Common Questions

**Q: Can I use a different AI provider?**
Yes! Just change `API_BASE_URL` and `MODEL_NAME`. Any OpenAI-compatible API works:
- OpenAI, Groq, Together AI, OpenRouter, Ollama (local), etc.

**Q: Is Groq really free?**
Yes, Groq offers a generous free tier. For our hackathon demo, it's more than enough. They make money from enterprise customers.

**Q: Why not run the AI model locally?**
You could! Using Ollama, set `API_BASE_URL="http://localhost:11434/v1"`. But you'd need a powerful GPU and the quality would be lower with smaller models.

**Q: Can Hugging Face Spaces handle production traffic?**
For a hackathon demo, absolutely. For production, you'd upgrade to a paid HF Space or deploy to AWS/GCP.

**Q: What does the Docker container actually do?**
It packages our entire server (Python code, dependencies, patient data) into a portable box. HF Spaces runs this box in the cloud, so our server is always available.

---

*Built with ❤️ for the Meta × Hugging Face OpenEnv Hackathon*
