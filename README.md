# 🚀 Synapse LinkedIn Sourcing Agent

**AI-powered candidate sourcing, scoring, and outreach generation for the Synapse AI Hackathon**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.46+-red.svg)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

This project implements a comprehensive LinkedIn sourcing agent that automatically finds, scores, and generates personalized outreach messages for job candidates. Built for the **Synapse AI Hackathon**, it demonstrates advanced AI-powered recruitment workflows.

### 🎯 Key Features

- **🔍 Intelligent Candidate Discovery**: Generates realistic LinkedIn profiles based on job requirements
- **📊 Advanced Fit Scoring**: Implements Synapse's proprietary scoring rubric (Education, Trajectory, Company, Skills, Location, Tenure)
- **💬 Personalized Outreach**: AI-generated LinkedIn messages tailored to each candidate
- **📈 Comprehensive Analytics**: Detailed score breakdowns and candidate insights
- **🔄 Scalable Architecture**: FastAPI backend with Streamlit frontend
- **💾 Data Persistence**: SQLite database for caching and result storage

## 🏗️ Architecture

```
Job Description → Candidate Generation → Fit Scoring → Outreach Generation → Results Display
       ↓                    ↓                ↓              ↓                ↓
   Gemini API → Fake Dataset → Scoring Algorithm → Personalized Messages → UI/API
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sayan-in-tech/Synapse.git
   cd Synapse
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
   ```

4. **Run the application**

   **Option A: Streamlit UI**
   ```bash
   streamlit run main.py
   ```
   Open http://localhost:8501

   **Option B: FastAPI Backend**
   ```bash
   uvicorn api:app --reload
   ```
   Open http://localhost:8000/docs

## 📖 Usage

### Web Interface (Streamlit)

1. **Enter Job Description**: Paste or use the sample Windsurf job description
2. **Start Sourcing**: Click "🔍 Start Sourcing" to begin the process
3. **View Results**: 
   - **Top 20 Candidates**: Sorted by fit score with contact buttons
   - **Score Breakdown**: Detailed scoring for top 10 candidates
   - **Outreach Messages**: Personalized LinkedIn messages for top 10

### API Endpoints

#### POST `/sourcing`
Source candidates for a job description.

**Request:**
```json
{
  "job_description": "Software Engineer, ML Research at Windsurf..."
}
```

**Response:**
```json
{
  "job_id": "job_20241230_143022",
  "candidates_found": 20,
  "total_candidates_scored": 100,
  "top_candidates": [
    {
      "name": "Sarah Chen",
      "linkedin_url": "linkedin.com/in/sarah-chen-ml",
      "headline": "Senior ML Engineer at Google",
      "location": "Mountain View, CA",
      "experience": "6 years",
      "education": "Stanford University, MS Computer Science",
      "skills": "Python, TensorFlow, PyTorch, Machine Learning",
      "company": "Google",
      "fit_score": 8.5,
      "score_breakdown": {
        "education": 9.5,
        "trajectory": 8.0,
        "company": 9.0,
        "skills": 9.0,
        "location": 10.0,
        "tenure": 7.0
      },
      "outreach_message": "Hi Sarah, I noticed your impressive background..."
    }
  ]
}
```

#### GET `/health`
Health check endpoint.

## 🎯 Fit Score Algorithm

The scoring system uses Synapse's proprietary rubric with the following weights:

| Category | Weight | Scoring Criteria |
|----------|--------|------------------|
| **Education** | 20% | Elite schools (9-10), Strong schools (7-8), Standard (5-6) |
| **Career Trajectory** | 20% | Steady growth (6-8), Limited progression (3-5) |
| **Company Relevance** | 15% | Top tech companies (9-10), Relevant industry (7-8), Any experience (5-6) |
| **Experience Match** | 25% | Perfect skill match (9-10), Strong overlap (7-8), Some relevant skills (5-6) |
| **Location Match** | 10% | Exact city (10), Same metro (8), Remote-friendly (6) |
| **Tenure** | 10% | 2-3 years average (9-10), 1-2 years (6-8), Job hopping (3-5) |

### Elite Schools
MIT, Stanford, Harvard, UC Berkeley, Carnegie Mellon, Caltech, Princeton, Yale

### Top Tech Companies
Google, Microsoft, Apple, Amazon, Meta, Netflix, Airbnb, Uber, OpenAI, Anthropic, Stripe, Palantir, Databricks

## 🗂️ Project Structure

```
Synapse/
├── main.py                      # Streamlit web application
├── api.py                       # FastAPI backend
├── fake_candidates_dataset.py   # Candidate generation logic
├── requirements.txt             # Python dependencies
├── work.md                      # Hackathon requirements
├── candidates.db               # SQLite database (auto-generated)
└── README.md                   # This file
```

## 🔧 Technical Details

### Dependencies

- **Streamlit**: Web interface
- **FastAPI**: REST API backend
- **Google Generative AI**: LLM integration for outreach messages
- **Pandas**: Data manipulation
- **SQLite**: Local data storage
- **Pydantic**: Data validation

### Key Components

1. **LinkedInSourcingAgent**: Core business logic
2. **Fake Dataset Generator**: Realistic candidate profiles
3. **Scoring Engine**: Fit score calculation
4. **Outreach Generator**: Personalized message creation
5. **Database Layer**: Result persistence

## 🎨 Features Demo

### Candidate Discovery
- Generates 100 realistic LinkedIn profiles
- Analyzes job requirements for optimal matching
- Provides diverse candidate pool

### Intelligent Scoring
- Comprehensive fit score calculation
- Detailed breakdown by category
- Transparent scoring methodology

### Personalized Outreach
- AI-generated LinkedIn messages
- References specific candidate details
- Professional tone and clear call-to-action

### Interactive UI
- Real-time progress tracking
- Contact buttons for each candidate
- Export functionality (JSON)
- Score visualization

## 🙏 Acknowledgments

- **Synapse** for the hackathon challenge and scoring rubric
- **Google Gemini** for AI capabilities
- **Streamlit** and **FastAPI** for the excellent frameworks
- **Windsurf (Codeium)** for the sample job description

**Built with ❤️ for the Synapse AI Hackathon**

*This project demonstrates advanced AI-powered recruitment workflows and showcases the potential of automated candidate sourcing and outreach generation.* 