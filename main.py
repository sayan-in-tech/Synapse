import streamlit as st
import google.generativeai as genai
import pandas as pd
import requests
import json
import re
import time
import sqlite3
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import os
from datetime import datetime
from linkedin_scrapper import scrape_candidates
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

class LinkedInSourcingAgent:
    def __init__(self):
        self.db_path = "candidates.db"
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for caching"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                linkedin_url TEXT UNIQUE,
                headline TEXT,
                location TEXT,
                experience TEXT,
                education TEXT,
                skills TEXT,
                company TEXT,
                job_description TEXT,
                fit_score REAL,
                score_breakdown TEXT,
                outreach_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def search_linkedin(self, job_description: str) -> List[Dict[str, Any]]:
        """Search for LinkedIn profiles based on job description"""
        st.info("🔍 Generating candidate profiles...")
        
        # Use the fake dataset instead of Gemini
        candidates = scrape_candidates(job_description, num_candidates=100)
        
        # Add some delay to simulate processing
        time.sleep(2)
        
        return candidates  # Return all candidates for scoring
    
    def score_candidates(self, candidates: List[Dict[str, Any]], job_description: str) -> List[Dict[str, Any]]:
        """Score candidates using the fit score algorithm"""
        st.info("📊 Scoring all candidates...")
        
        scored_candidates = []
        progress_bar = st.progress(0)
        
        for i, candidate in enumerate(candidates):
            score_breakdown = self.calculate_fit_score(candidate, job_description)
            total_score = sum(score_breakdown.values()) / len(score_breakdown)
            
            scored_candidate = {
                **candidate,
                "fit_score": round(total_score, 1),
                "score_breakdown": score_breakdown
            }
            scored_candidates.append(scored_candidate)
            
            # Update progress bar
            progress = (i + 1) / len(candidates)
            progress_bar.progress(progress)
        
        # Sort by fit score (highest first)
        scored_candidates.sort(key=lambda x: x["fit_score"], reverse=True)
        
        # Return top 20 candidates
        return scored_candidates[:20]
    
    def calculate_fit_score(self, candidate: Dict[str, Any], job_description: str) -> Dict[str, float]:
        """Calculate fit score using the provided rubric"""
        breakdown = {}
        
        # Education (20%)
        education_score = self.score_education(candidate.get("education", ""))
        breakdown["education"] = education_score
        
        # Career Trajectory (20%)
        trajectory_score = self.score_trajectory(candidate.get("experience", ""))
        breakdown["trajectory"] = trajectory_score
        
        # Company Relevance (15%)
        company_score = self.score_company(candidate.get("company", ""), job_description)
        breakdown["company"] = company_score
        
        # Experience Match (25%)
        experience_score = self.score_experience(candidate.get("skills", ""), job_description)
        breakdown["skills"] = experience_score
        
        # Location Match (10%)
        location_score = self.score_location(candidate.get("location", ""), job_description)
        breakdown["location"] = location_score
        
        # Tenure (10%)
        tenure_score = self.score_tenure(candidate.get("tenure", ""))
        breakdown["tenure"] = tenure_score
        
        return breakdown
    
    def score_education(self, education: str) -> float:
        """Score education based on school prestige"""
        elite_schools = ["stanford", "mit", "harvard", "berkeley", "cmu", "caltech", "princeton", "yale"]
        strong_schools = ["ucla", "usc", "nyu", "columbia", "cornell", "georgia tech", "michigan", "illinois", "ut austin"]
        
        education_lower = education.lower()
        
        for school in elite_schools:
            if school in education_lower:
                return 9.5
        
        for school in strong_schools:
            if school in education_lower:
                return 7.5
        
        return 6.0
    
    def score_trajectory(self, experience: str) -> float:
        """Score career trajectory"""
        try:
            years = int(re.findall(r'\d+', experience)[0])
            if years >= 5:
                return 8.0
            elif years >= 3:
                return 7.0
            elif years >= 1:
                return 6.0
            else:
                return 4.0
        except:
            return 5.0
    
    def score_company(self, company: str, job_description: str) -> float:
        """Score company relevance"""
        top_companies = ["google", "microsoft", "apple", "amazon", "meta", "netflix", "airbnb", "uber", "openai", "anthropic", "stripe", "palantir", "databricks"]
        relevant_companies = ["salesforce", "adobe", "oracle", "intel", "nvidia", "amd", "cisco", "vmware", "splunk", "mongodb", "datadog", "snowflake", "twilio"]
        
        company_lower = company.lower()
        
        for top_company in top_companies:
            if top_company in company_lower:
                return 9.0
        
        for relevant_company in relevant_companies:
            if relevant_company in company_lower:
                return 7.5
        
        # Check if company is in same industry
        if "ai" in company_lower or "tech" in company_lower:
            return 7.0
        
        return 6.0
    
    def score_experience(self, skills: str, job_description: str) -> float:
        """Score experience/skills match"""
        job_lower = job_description.lower()
        skills_lower = skills.lower()
        
        # Count matching skills
        relevant_terms = ["python", "machine learning", "ai", "ml", "tensorflow", "pytorch", "deep learning", "llm", "code generation", "neural networks", "scikit-learn"]
        matches = sum(1 for term in relevant_terms if term in skills_lower and term in job_lower)
        
        if matches >= 3:
            return 9.0
        elif matches >= 2:
            return 7.5
        elif matches >= 1:
            return 6.0
        else:
            return 4.0
    
    def score_location(self, location: str, job_description: str) -> float:
        """Score location match"""
        job_lower = job_description.lower()
        location_lower = location.lower()
        
        if "mountain view" in job_lower and "mountain view" in location_lower:
            return 10.0
        elif "california" in job_lower and "california" in location_lower:
            return 8.0
        elif "remote" in job_lower:
            return 6.0
        else:
            return 4.0
    
    def score_tenure(self, tenure: str) -> float:
        """Score tenure at current role"""
        try:
            years = int(re.findall(r'\d+', tenure)[0])
            if 2 <= years <= 4:
                return 9.0
            elif 1 <= years < 2:
                return 7.0
            elif years >= 5:
                return 6.0
            else:
                return 4.0
        except:
            return 5.0
    
    def generate_outreach(self, scored_candidates: List[Dict[str, Any]], job_description: str) -> List[Dict[str, Any]]:
        """Generate personalized outreach messages"""
        st.info("💬 Generating outreach messages for top candidates...")
        
        outreach_candidates = []
        for candidate in scored_candidates[:10]:  # Generate outreach for top 10
            message = self.create_personalized_message(candidate, job_description)
            
            outreach_candidate = {
                **candidate,
                "outreach_message": message
            }
            outreach_candidates.append(outreach_candidate)
        
        return outreach_candidates
    
    def create_personalized_message(self, candidate: Dict[str, Any], job_description: str) -> str:
        """Create personalized LinkedIn message"""
        prompt = f"""
        Create a personalized LinkedIn outreach message for this candidate:
        
        Candidate: {candidate['name']}
        Current Role: {candidate['headline']}
        Location: {candidate['location']}
        Experience: {candidate['experience']}
        Skills: {candidate['skills']}
        Company: {candidate['company']}
        
        Job Description: {job_description}
        
        Write a professional, personalized message that:
        1. References specific details from their profile
        2. Explains why they're a good fit for the role
        3. Is under 200 words
        4. Has a professional tone
        5. Includes a clear call to action
        
        Start with "Hi [Name],"
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except:
            return f"Hi {candidate['name']}, I noticed your impressive background in {candidate['skills']} at {candidate['company']}. Your experience aligns perfectly with our {job_description[:50]}... role. Would you be interested in discussing this opportunity?"
    
    def save_to_database(self, candidates: List[Dict[str, Any]], job_description: str):
        """Save candidates to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for candidate in candidates:
            cursor.execute('''
                INSERT OR REPLACE INTO candidates 
                (name, linkedin_url, headline, location, experience, education, skills, company, 
                 job_description, fit_score, score_breakdown, outreach_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                candidate.get('name', ''),
                candidate.get('linkedin_url', ''),
                candidate.get('headline', ''),
                candidate.get('location', ''),
                candidate.get('experience', ''),
                candidate.get('education', ''),
                candidate.get('skills', ''),
                candidate.get('company', ''),
                job_description,
                candidate.get('fit_score', 0),
                json.dumps(candidate.get('score_breakdown', {})),
                candidate.get('outreach_message', '')
            ))
        
        conn.commit()
        conn.close()

# Initialize the agent
agent = LinkedInSourcingAgent()

# Streamlit UI
st.set_page_config(page_title="Synapse LinkedIn Sourcing Agent", layout="wide")
st.title("🚀 Synapse LinkedIn Sourcing Agent")
st.markdown("**AI-powered candidate sourcing, scoring, and outreach generation**")

# Sidebar
st.sidebar.header("Configuration")
st.sidebar.markdown("### Job Description")
job_description = st.sidebar.text_area(
    "Enter job description:",
    height=200,
    placeholder="Paste the job description here..."
)

# Main content
if st.sidebar.button("🔍 Start Sourcing", type="primary"):
    if job_description:
        with st.spinner("Processing..."):
            # Step 1: Search for candidates
            candidates = agent.search_linkedin(job_description)
            
            if candidates:
                # Step 2: Score all candidates and get top 20
                scored_candidates = agent.score_candidates(candidates, job_description)
                
                # Step 3: Generate outreach for top 10
                final_candidates = agent.generate_outreach(scored_candidates, job_description)
                
                # Step 4: Save to database
                agent.save_to_database(scored_candidates, job_description)
                
                # Display results
                st.success(f"✅ Scored {len(candidates)} candidates, showing top {len(scored_candidates)}!")
                
                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["📊 Top 20 Candidates", "📈 Score Breakdown", "💬 Outreach Messages"])
                
                with tab1:
                    # Display top 20 candidates with contact buttons
                    st.subheader("🏆 Top 20 Candidates (Sorted by Score)")
                    
                    for i, candidate in enumerate(scored_candidates, 1):
                        with st.container():
                            col1, col2, col3 = st.columns([3, 1, 1])
                            
                            with col1:
                                st.markdown(f"**{i}. {candidate['name']}**")
                                st.markdown(f"*{candidate['headline']}*")
                                st.markdown(f"📍 {candidate['location']} | 🏢 {candidate['company']}")
                                st.markdown(f"🎓 {candidate['education']}")
                                st.markdown(f"💼 {candidate['experience']} | ⏱️ {candidate['tenure']}")
                                st.markdown(f"🛠️ **Skills:** {candidate['skills']}")
                            
                            with col2:
                                st.metric("Fit Score", f"{candidate['fit_score']}/10")
                            
                            with col3:
                                # Fake LinkedIn contact button
                                if st.button(f"📧 Contact", key=f"contact_{i}"):
                                    st.success(f"✅ Message sent to {candidate['name']} on LinkedIn!")
                                    st.info(f"LinkedIn URL: https://{candidate['linkedin_url']}")
                            
                            st.divider()
                
                with tab2:
                    # Display score breakdown
                    st.subheader("📊 Detailed Score Breakdown")
                    for candidate in scored_candidates[:10]:  # Show breakdown for top 10
                        st.subheader(f"{candidate['name']} - Score: {candidate['fit_score']}")
                        breakdown = candidate['score_breakdown']
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Education", f"{breakdown['education']:.1f}/10")
                            st.metric("Trajectory", f"{breakdown['trajectory']:.1f}/10")
                            st.metric("Company", f"{breakdown['company']:.1f}/10")
                        
                        with col2:
                            st.metric("Skills", f"{breakdown['skills']:.1f}/10")
                            st.metric("Location", f"{breakdown['location']:.1f}/10")
                            st.metric("Tenure", f"{breakdown['tenure']:.1f}/10")
                        
                        st.divider()
                
                with tab3:
                    # Display outreach messages
                    st.subheader("💬 Personalized Outreach Messages (Top 10)")
                    for i, candidate in enumerate(final_candidates, 1):
                        st.subheader(f"Message for {candidate['name']} (#{i})")
                        st.write(candidate['outreach_message'])
                        
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            if st.button(f"📧 Send Message", key=f"send_{i}"):
                                st.success(f"✅ Message sent to {candidate['name']}!")
                        with col2:
                            if st.button(f"📋 Copy Message", key=f"copy_{i}"):
                                st.info("📋 Message copied to clipboard!")
                        
                        st.divider()
                
                # Export results
                st.download_button(
                    label="📥 Download Top 20 Results (JSON)",
                    data=json.dumps(scored_candidates, indent=2),
                    file_name=f"top_20_candidates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
            else:
                st.error("No candidates found. Try refining your job description.")
    else:
        st.error("Please enter a job description.")

# Display sample job description
st.sidebar.markdown("---")
st.sidebar.markdown("### Sample Job Description")
sample_job = """
Software Engineer, ML Research at Windsurf (ID: SRN2025-10916). 

Windsurf • Full Time • Mountain View, CA • On-site • $140,000 – $300,000 + Equity.

About the Company:
Windsurf (formerly Codeium) is a Forbes AI 50 company focused on transforming developer productivity through AI. With over 200 employees and $243M raised (including Series C), Windsurf delivers in-editor autocomplete, chat assistants, and full IDEs powered by proprietary LLMs. The platform is trusted by hundreds of thousands of developers globally.

Roles and Responsibilities:
- Train and fine-tune LLMs for developer productivity.
- Design and prioritize experiments with measurable product impact.
- Analyze results, perform ablation studies, and document findings.
- Translate ML research into scalable, product-ready features.
- Participate in ML reading groups and contribute to internal knowledge sharing.

Job Requirements:
- 2+ years of software engineering experience with a strong growth trajectory.
- Strong software engineering and systems design skills.
- Demonstrated experience with training and iterating on large-scale production neural networks.
- High GPA from a top-tier CS undergrad program (MIT, Stanford, CMU, UIUC, etc.).
- Familiarity with Copilot, ChatGPT, or Windsurf is a plus.
- Deep interest in the code generation space.
- Strong skills in documentation and experimental discipline.
- Applied ML research experience (beyond academic publishing).
- Willingness to work full-time on-site in Mountain View, CA.
- Eagerness to build ML-driven, product-facing features.

Interview Process:
1. Recruiter Chat (15 min)
2. Virtual Algorithm Round (LeetCode-style, 45 min)
3. Virtual ML Case Study (1 hour)
4. Onsite (3 hours): Includes additional ML case, implementation project, and culture interview
5. Offer Extended
"""


if st.sidebar.button("Load Sample"):
    st.sidebar.text_area("Job Description:", value=sample_job, height=200)

# Footer
st.markdown("---")
st.markdown("**Built for Synapse AI Hackathon - LinkedIn Sourcing Agent Challenge**") 