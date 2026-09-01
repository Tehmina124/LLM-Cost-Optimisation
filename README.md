<p align="center">
  <img src="LLM" width="100%" alt="LLM Cost Optimisation Study">
</p>

<h1 align="center">💰 LLM Cost Optimisation Study</h1>

<p align="center">
  <b>Reduce LLM Costs Without Materially Hurting Quality</b>
</p>

<p align="center">
  A practical Generative AI project demonstrating prompt compression,
  model routing, response caching, token reduction, cost analysis,
  and quality evaluation.
</p>

<p align="center">
  <a href="https://llm-cost-optimisation-r9jrfo3yrfuuqrxs9e2xhg.streamlit.app/">
    <img src="https://img.shields.io/badge/🚀%20LIVE%20DEMO-Streamlit-red?style=for-the-badge&logo=streamlit" alt="Live Demo">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Streamlit-red?style=for-the-badge&logo=streamlit&logoColor=white">
  <img src="https://img.shields.io/badge/Ollama-black?style=for-the-badge&logo=ollama&logoColor=white">
  <img src="https://img.shields.io/badge/Pandas-purple?style=for-the-badge&logo=pandas&logoColor=white">
  <img src="https://img.shields.io/badge/Generative%20AI-green?style=for-the-badge">
</p>

---

# 📌 About the Project

**LLM Cost Optimisation Study** is a Generative AI project focused on reducing the operational cost of Large Language Model applications while maintaining or improving response quality.

The project compares a traditional **Baseline Implementation** with an **Optimized Implementation**.

The optimized approach demonstrates:

* ✂️ Prompt Compression
* 🤖 Model Routing
* ⚡ Response Caching
* 📉 Token Reduction
* 🎯 Quality Evaluation
* 💰 Cost Analysis
* 📊 Cost Comparison
* 📅 Monthly Cost Projection

The application provides an interactive **Streamlit dashboard** where users can run experiments and analyze the cost-quality trade-off.

---

# 🎯 Project Goal

The main goal is:

> **Reduce LLM cost without materially reducing response quality.**

Instead of focusing only on using a cheaper model, this project combines several optimization techniques to improve the overall efficiency of an LLM-powered application.

```text
Better Prompts
      +
Smart Model Selection
      +
Response Caching
      +
Fewer Tokens
      +
Quality Evaluation
      ↓
Lower Cost + Better Efficiency
```

---

# ✨ Key Features

| Feature                  | Description                                              |
| ------------------------ | -------------------------------------------------------- |
| ✂️ Prompt Compression    | Reduces unnecessary prompt instructions                  |
| 🤖 Model Routing         | Selects an appropriate model based on request complexity |
| ⚡ Response Caching       | Reuses responses for repeated questions                  |
| 📉 Token Reduction       | Measures token savings                                   |
| 🎯 Quality Evaluation    | Compares response quality                                |
| 💰 Cost Analysis         | Calculates estimated benchmark costs                     |
| 📊 Cost Comparison       | Compares baseline and optimized implementations          |
| 📅 Monthly Projection    | Estimates monthly cost and savings                       |
| 🏆 Recommendation Engine | Recommends the better implementation                     |
| 📈 Experiment History    | Tracks experiments during the session                    |
| 📥 CSV Export            | Exports experiment results                               |
| 🦙 Local LLM             | Supports local inference with Ollama                     |
| ☁️ Streamlit Dashboard   | Interactive web application                              |

---

# 📊 Benchmark Results

A benchmark experiment was performed using:

> **How can I reset my password?**

The results demonstrate the effect of optimization.

## 🔴 Baseline vs 🟢 Optimized

| Metric                | 🔴 Baseline |   🟢 Optimized |
| --------------------- | ----------: | -------------: |
| Token Usage           |         736 |         **96** |
| Token Reduction       |           — |     **86.96%** |
| Cost / 1,000 Requests |     $1.0504 |    **$0.1236** |
| Cost Reduction        |           — |     **88.23%** |
| Quality Score         |    80 / 100 |   **90 / 100** |
| Quality Change        |           — | **+10 points** |
| Cache                 |           — |           MISS |

---

# 🏆 Benchmark Outcome

```text
📉 Token Reduction
86.96%

💰 Cost Reduction
88.23%

🎯 Quality Improvement
+10 points
```

### Final Recommendation

> 🟢 **RECOMMEND OPTIMIZED**

The optimized implementation achieved a significant reduction in token usage and estimated cost while improving the measured quality score in this experiment.

---

# 🧠 Optimization Architecture

```text
                         👤 User Question
                                │
                                ▼
                       📝 Input Processing
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼                             ▼
          🔴 BASELINE                    🟢 OPTIMIZED
                 │                             │
                 │                    ✂️ Prompt Compression
                 │                             │
                 │                    🤖 Model Routing
                 │                             │
                 │                    ⚡ Response Cache
                 │                             │
                 ▼                             ▼
          LLM Generation                LLM Generation
                 │                             │
                 └──────────────┬──────────────┘
                                ▼
                       🎯 Quality Evaluation
                                │
                                ▼
                         📊 Cost Analysis
                                │
                                ▼
                      🏆 Final Recommendation
```

---

# ✂️ 1. Prompt Compression

Large prompts can contain unnecessary instructions that increase token usage.

The optimized implementation simplifies the prompt while preserving the important requirements.

```text
Long Prompt
     ↓
Remove Unnecessary Instructions
     ↓
Shorter Prompt
     ↓
Fewer Tokens
     ↓
Lower Cost
```

### Benefits

* 📉 Lower token usage
* 💰 Lower estimated cost
* ⚡ Faster processing
* 🎯 Maintains essential instructions

---

# 🤖 2. Model Routing

Different questions require different levels of model capability.

Simple requests can be handled by smaller and faster models, while complex requests can be routed to stronger models.

```text
Simple Question
      ↓
Smaller / Faster Model
      ↓
Lower Cost


Complex Question
      ↓
Stronger Model
      ↓
Better Reasoning
```

The objective is to balance:

**Cost + Speed + Quality**

---

# ⚡ 3. Response Caching

If the same question is asked multiple times, generating a new response every time is unnecessary.

The application stores responses in memory and returns the cached response when the same request appears again.

```text
User Question
      ↓
Check Cache
      │
 ┌────┴────┐
 │         │
HIT       MISS
 │         │
 ▼         ▼
Return   Generate
Cached   Response
Answer      │
            ▼
        Store Cache
```

### Cache Benefits

* ⚡ Faster responses
* 💰 Lower generation cost
* 📉 Avoids unnecessary token generation
* 🚀 Improves application efficiency

---

# 📉 4. Token Reduction

The application measures token usage for both implementations.

### Formula

```text
Token Reduction (%)
=
(Baseline Tokens - Optimized Tokens)
------------------------------------ × 100
        Baseline Tokens
```

### Benchmark

```text
Baseline Tokens  = 736

Optimized Tokens = 96

Token Reduction  = 86.96%
```

---

# 💰 5. Cost Analysis

The dashboard calculates estimated benchmark costs based on recorded token usage.

It provides:

* 💵 Baseline cost
* 💵 Optimized cost
* 💸 Cost savings
* 📊 Cost per 1,000 requests
* 📅 Monthly projected cost
* 💰 Monthly savings

### Benchmark

```text
Baseline
$1.0504 / 1,000 requests

Optimized
$0.1236 / 1,000 requests
```

### Estimated Saving

```text
$1.0504 - $0.1236

= $0.9268 saved / 1,000 requests
```

---

# 📅 Monthly Cost Projection

The dashboard allows users to enter their expected monthly request volume.

### Example

```text
Monthly Requests = 10,000
```

Projected result:

```text
🔴 Baseline Monthly Cost
$10.50

🟢 Optimized Monthly Cost
$1.24

💰 Monthly Saving
$9.27
```

This demonstrates how small savings per request can become significant at higher request volumes.

---

# 🎯 6. Quality Evaluation

Cost reduction should not come at the expense of response quality.

Therefore, the project compares the quality of both implementations.

### Benchmark

```text
🔴 Baseline Quality
80 / 100

🟢 Optimized Quality
90 / 100
```

### Result

```text
🎯 Quality Change
+10 points
```

In this benchmark, optimization reduced estimated cost while improving the measured quality score.

---

# 🏆 Recommendation Engine

The application evaluates the cost-quality trade-off and generates a recommendation.

For the benchmark:

```text
Cost Reduction     → 88.23%
Token Reduction    → 86.96%
Quality Change     → +10 points
Monthly Saving     → $9.27
```

### Recommendation

```text
🟢 RECOMMEND OPTIMIZED
```

---

# 📊 Streamlit Dashboard

The interactive dashboard provides several sections.

### 📈 Performance Metrics

* Baseline tokens
* Optimized tokens
* Token reduction
* Baseline cost
* Optimized cost
* Cost reduction

### 🎯 Quality Analysis

* Baseline quality
* Optimized quality
* Quality change
* Cost-quality trade-off

### 💰 Cost Analysis

* Cost per 1,000 requests
* Savings per 1,000 requests
* Monthly projected cost
* Monthly savings

### ⚡ Cache Analysis

* Cache HIT
* Cache MISS
* Cached response reuse

### 📈 Experiment History

Experiments can be recorded during the current Streamlit session.

---

# 📥 CSV Export

The application allows experiment results to be exported as CSV.

Exported information can include:

```text
Question
Baseline Tokens
Optimized Tokens
Token Reduction
Baseline Cost
Optimized Cost
Cost Reduction
Baseline Quality
Optimized Quality
Quality Change
Cache Status
```

This allows the results to be analyzed later using tools such as Excel or Pandas.

---

# 🛠️ Technologies Used

| Technology                   | Purpose                      |
| ---------------------------- | ---------------------------- |
| 🐍 Python                    | Application development      |
| 🎈 Streamlit                 | Interactive dashboard        |
| 🦙 Ollama                    | Local LLM inference          |
| 🐼 Pandas                    | Data analysis and CSV export |
| 🧠 LLM                       | Natural-language generation  |
| 📊 CSV                       | Experiment storage           |
| 🐙 GitHub                    | Version control              |
| ☁️ Streamlit Community Cloud | Deployment                   |

---

# 🧠 Concepts Demonstrated

This project demonstrates practical knowledge of:

* Artificial Intelligence
* Generative AI
* Large Language Models
* Prompt Engineering
* Prompt Compression
* Model Routing
* Response Caching
* Token Economics
* LLM Evaluation
* Quality Measurement
* Cost Optimization
* Data Analysis
* Python Development
* Streamlit
* Local LLM Deployment
* Cloud Deployment

---

# 📂 Project Structure

```text
LLM-Cost-Optimisation/
│
├── 🖼️ LLM.png
├── 📄 README.md
├── 📄 app.py
├── 📄 baseline.py
├── 📄 optimized.py
├── 📄 evaluator.py
├── 📄 cost_analysis.py
├── 📄 requirements.txt
├── 📄 .env.example
├── 📄 .gitignore
│
└── 📁 data/
    └── 📄 test_questions.json
```

---

# 📄 File Description

### `app.py`

Main Streamlit dashboard containing:

* User interface
* Baseline vs optimized comparison
* Cost analysis
* Quality evaluation
* Cache handling
* Monthly projection
* Experiment history
* CSV export

### `baseline.py`

Contains the baseline LLM implementation used as the original benchmark.

### `optimized.py`

Contains the optimized LLM implementation using:

* Prompt compression
* Model routing
* Response caching

### `evaluator.py`

Handles response quality evaluation and comparison.

### `cost_analysis.py`

Calculates:

* Token usage
* Benchmark cost
* Cost reduction
* Savings
* Monthly projection

### `data/test_questions.json`

Contains sample questions used for optimization experiments.

### `LLM.png`

Banner image displayed at the top of this README.

---

# 🚀 Installation & Setup

## 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

## 2. Open the Project

```bash
cd LLM-Cost-Optimisation
```

## 3. Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Setup Ollama

Install Ollama and make sure your required local model is available.

Check installed models:

```bash
ollama list
```

## 6. Run the Application

```bash
python -m streamlit run app.py
```

## 7. Open in Browser

```text
http://localhost:8501
```

---

# 🌐 Live Demo

<p align="center">
  <a href="https://llm-cost-optimisation-r9jrfo3yrfuuqrxs9e2xhg.streamlit.app/">
    🚀 <b>Open Live Demo</b>
  </a>
</p>

🔗 https://llm-cost-optimisation-r9jrfo3yrfuuqrxs9e2xhg.streamlit.app/

---

# ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

```text
🐍 Python
   ↓
🧠 LLM Application
   ↓
🎈 Streamlit
   ↓
🐙 GitHub
   ↓
☁️ Streamlit Community Cloud
   ↓
🌐 Live Demo
```

> **Note:** Local development can use Ollama for local LLM inference. Cloud deployment may require a cloud-compatible inference configuration depending on the selected model and deployment environment.

---

# 🎯 Project Objectives

* 💰 Reduce LLM inference costs
* 📉 Reduce unnecessary token usage
* ✂️ Optimize prompts
* 🤖 Route requests intelligently
* ⚡ Implement response caching
* 🎯 Measure response quality
* 📊 Compare baseline and optimized implementations
* 📅 Project savings at scale
* 🏆 Generate data-driven recommendations
* 🚀 Build an interview-ready Generative AI project

---

# 🔮 Future Improvements

* 🤖 Support additional LLM providers
* 🧠 Advanced model-routing strategies
* 💬 Conversational memory
* 📊 Automated benchmark datasets
* 🎯 Human evaluation
* 📈 Statistical experiment analysis
* 🗄️ Persistent experiment database
* 🔍 Advanced prompt optimization
* ⚡ Distributed caching
* 📊 Real-time cost monitoring
* 🔐 Authentication and user management
* 🚀 Production-scale deployment

---

# 👩‍💻 About Me

## Tehmina Anwar

**AI/ML Engineer | Python Developer | Generative AI Enthusiast**

I am a Bachelor of Science in Artificial Intelligence student passionate about building practical AI, Machine Learning, Generative AI, NLP, and Python applications.

### Areas of Interest

* 🐍 Python
* 🤖 Machine Learning
* 🧠 Generative AI
* 💬 Large Language Models
* 🔎 Retrieval-Augmented Generation
* 📝 Natural Language Processing
* 👁️ Computer Vision
* 📊 Data Analytics
* 🚀 AI Application Development

---

# 🔗 Connect With Me

### 💻 GitHub

<a href="https://github.com/Tehminaanwar543">
  <img src="https://img.shields.io/badge/GitHub-Profile-black?style=for-the-badge&logo=github" alt="GitHub">
</a>

### 🔗 LinkedIn

<a href="https://www.linkedin.com/in/tehmina-anwar-77b8a8414/">
  <img src="https://img.shields.io/badge/LinkedIn-Profile-blue?style=for-the-badge&logo=linkedin" alt="LinkedIn">
</a>

### 🌐 Portfolio

<a href="https://tehmina-portfolio-five.vercel.app/">
  <img src="https://img.shields.io/badge/Portfolio-Website-purple?style=for-the-badge" alt="Portfolio">
</a>

---

# ⭐ Support

If you found this project useful, consider giving the repository a ⭐ **Star**.

---

<p align="center">
  <b>💰 Cut Cost. Keep Quality. Optimise Intelligently.</b>
</p>

<p align="center">
  Built with 🐍 Python • 🎈 Streamlit • 🦙 Ollama • 🐼 Pandas
</p>

<p align="center">
  © 2026 Tehmina Anwar
</p>
