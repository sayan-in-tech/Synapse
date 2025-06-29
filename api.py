from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import google.generativeai as genai
import json
import re
import time
from datetime import datetime
from fake_candidates_dataset import generate_fake_candidates
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI(title="Synapse LinkedIn Sourcing Agent API", version="1.0.0")

class JobRequest(BaseModel):
    job_description: str

class CandidateResponse(BaseModel):
    name: str
    linkedin_url: str
    headline: str
    location: str
    experience: str
    education: str
    skills: str
    company: str
    fit_score: float
    score_breakdown: Dict[str, float]
    outreach_message: str

class SourcingResponse(BaseModel):
    job_id: str
    candidates_found: int
    total_candidates_scored: int
    top_candidates: List[CandidateResponse]

class LinkedInSourcingAgent:
    def __init__(self):
        pass
    
    def search_linkedin(self, job_description: str) -> List[Dict[str, Any]]:
        """Search for LinkedIn profiles based on job description"""
        
        # Use the fake dataset instead of Gemini
        candidates = generate_fake_candidates(job_description, num_candidates=100)
        
        # Add some delay to simulate processing
        time.sleep(1)
        
        return candidates  # Return all candidates for scoring
    
    def score_candidates(self, candidates: List[Dict[str, Any]], job_description: str) -> List[Dict[str, Any]]:
        """Score candidates using the fit score algorithm"""
        
        scored_candidates = []
        for candidate in candidates:
            score_breakdown = self.calculate_fit_score(candidate, job_description)
            total_score = sum(score_breakdown.values()) / len(score_breakdown)
            
            scored_candidate = {
                **candidate,
                "fit_score": round(total_score, 1),
                "score_breakdown": score_breakdown
            }
            scored_candidates.append(scored_candidate)
        
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

# Initialize the agent
agent = LinkedInSourcingAgent()

@app.get("/")
async def root():
    return {"message": "Synapse LinkedIn Sourcing Agent API", "version": "1.0.0"}

@app.post("/sourcing", response_model=SourcingResponse)
async def source_candidates(request: JobRequest):
    """
    Source LinkedIn candidates for a job description.
    
    Scores all candidates and returns top 20 with fit scores and personalized outreach messages.
    """
    try:
        # Step 1: Search for candidates
        candidates = agent.search_linkedin(request.job_description)
        
        if not candidates:
            raise HTTPException(status_code=404, detail="No candidates found")
        
        # Step 2: Score all candidates and get top 20
        scored_candidates = agent.score_candidates(candidates, request.job_description)
        
        # Step 3: Generate outreach for top 10
        final_candidates = agent.generate_outreach(scored_candidates, request.job_description)
        
        # Convert to response format
        candidate_responses = []
        for candidate in scored_candidates:  # Include all top 20 candidates
            # Check if outreach message exists (only for top 10)
            outreach_message = ""
            for final_candidate in final_candidates:
                if final_candidate["name"] == candidate["name"]:
                    outreach_message = final_candidate["outreach_message"]
                    break
            
            candidate_response = CandidateResponse(
                name=candidate["name"],
                linkedin_url=candidate["linkedin_url"],
                headline=candidate["headline"],
                location=candidate["location"],
                experience=candidate["experience"],
                education=candidate["education"],
                skills=candidate["skills"],
                company=candidate["company"],
                fit_score=candidate["fit_score"],
                score_breakdown=candidate["score_breakdown"],
                outreach_message=outreach_message
            )
            candidate_responses.append(candidate_response)
        
        # Create response
        job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        response = SourcingResponse(
            job_id=job_id,
            candidates_found=len(candidate_responses),
            total_candidates_scored=len(candidates),
            top_candidates=candidate_responses
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 