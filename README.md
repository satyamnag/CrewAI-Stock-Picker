# 📈 CrewAI Stock Picker
#### An automated multi-agent AI workflow that identifies trending companies, researches them, and selects the best investment opportunity using CrewAI, real-time search, and persistent memory.

## 🚀 Features
#### - 🔍 Find Trending Companies in a chosen sector
#### - 📊 Deep Financial Research using structured analysis
#### - 🎯 Select Best Stock with investment thesis
#### - 🧠 Long-term & short-term memory to avoid repeats
#### - 📑 Outputs in JSON + Markdown
#### - 🔧 Modular YAML configuration

## 🧠 Agent Workflow
#### 1. Trending Company Finder → discovers trending companies
#### 2. Financial Researcher → produces full structured reports
#### 3. Stock Picker → selects the best company + thesis
#### 4. Manager Agent → orchestrates the workflow

## 📤 Output Files
#### /output/trending_companies.json: Found trending companies
#### /output/research_report.json: Analysis reports
#### /output/decision.md: Final selected stock
#### /memory/long_term_memory_storage.db: Persistent long-term memory database used by agents

## 🔐 Environment Variables
#### OPENAI_API_KEY=your openai api key
#### PUSHOVER_USER=your pushover user ID
#### PUSHOVER_TOKEN=your pushover token
#### SERPER_API_KEY=your serper api key

