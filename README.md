# $\text{🧬 SUMMED.ai (Scientific Literature Summary and Trend Dashboard)}$

> **AI-Powered Biomedical Text Mining & Genomic Trend Analysis Platform**
> 
> SUMMED is an intelligent dashboard designed to analyze and visualize real-time trends in the latest genomics and biomedical literature based on massive datasets from PubMed. By integrating Large Language Models (LLMs), the platform precisely summarizes complex abstracts and classifies clinical evidence levels, serving as a researcher-centric informatics tool.

---

## $\text{✨ Key Features}$

- **Multi-Route Input Processing Pipeline:**
  - **Analysis with Topic:** Generates an AI-curated clinical evidence table containing key insights and summary points for a specific search term (genes, diseases, drugs, or even broad topics).
  - **Trend Exploration without Topic:** Automatically mines and explores global research keywords within a specific year range when no search term is provided.
- **AI-Driven Text Mining:**
  - Powered by the `meta-llama/llama-4-scout-17b-16e-instruct` model to filter out generic academic vocabulary (e.g., 'study', 'effect') and statistical noise from paper abstracts.
  - Precisely extracts high-value biological and clinical entities including Genes, Proteins, Pathways, and Lab Methodologies.
- **Data Visualisation:**
  - **AI-Curated Word Cloud:** Visually graphs the latest research landscapes using filtered, high-density biomedical tokens.
  - **Top 10 Keyword Frequency Chart:** Provides a chart for quantitative frequency analysis of mined keywords.
- **Utilities for Researchers:**
  - **Markdown Export:** Enables one-click downloading of summary tables with auto-generated filenames matching the user's query and date (`[Topic]_[Date].md`).
  - **Cross-Validation Links:** Dynamically lists direct PubMed URLs for all fetched articles to allow source verification.

---

## $\text{🛠️ Tech Stack}$

- **Frontend/UI:** Streamlit (Custom Theme Applied)
- **Data Fetching:** Bio.Entrez (Biopython PubMed API)
- **AI Engine:** Groq API (`meta-llama/llama-4-scout-17b-16e-instruct`)
- **Data Visualization:** Matplotlib, WordCloud
- **Environment Management:** Streamlit Secrets

---

## $\text{📂 Project Structure}$
`summed.ai/`
<br>├── `main.py  # Main Streamlit application source code`
<br>├── `summed.png               # Custom PNG icon applied to the web browser tab`
<br>├── `Tektur-Medium.ttf             # Cool font for cool app`
<br>├── `requirements.txt       # Dependency package manifest (Biopython, Groq, etc.)`
<br>└── `README.md              # Documentation and system manual`

---

## $\text{🔐 Environment Variables and Security}$
This project utilises .env files for secure API Key management in local environments and relies on the Streamlit Secrets system for cloud deployments. (API Keys are strictly git-ignored and never exposed publicly.)

`# Example .env configuration`
<br>`GROQ_API_KEY=gsk_your_secret_key`
<br>`NCBI_EMAIL=your_email@example.com`

---

## $\text{🚀 Future Roadmap}$
- **Implementing of Streamlit's `@st.cache_data` mechanism: Plan to refactory the whole code to prevent redundant API calls, accelerating loading speeds by over 90%.**
- **📬 Automated Daily Mailing Subscription: Plan to construct a backend automation pipeline integrating a CronJob batch scheduler and an SQLite database. This will allow researchers to subscribe to specific keywords and receive AI-generated daily abstract reports directly in their inboxes via SMTP.**

- **🧬 Domain-Specific Filtering Expansion: Enhance text-mining engines with fine-tuned sub-specialty tags for specialised fields such as Oncology and Immunology.**
