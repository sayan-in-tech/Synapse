# **Synapse Annual First Ever AI Hackathon - Sourcing Agent Challenge**

## **Deadline: Monday 7 PM PST**

## **Website: [`www.synapsehire.com](http://www.synapsehire.com)`**

## **🚀 Overview**

Build an autonomous AI agent that sources LinkedIn profiles at scale, scores candidates using our fit score algorithm, and generates personalized outreach - all in 2-3 hours using Cursor.

This isn't a typical coding challenge. We want to see if you can build what we actually build at Synapse.

### 🌍 Why This Is Special

We will promote your win through our company and high-profile personal LinkedIn pages to:

- **Hundreds of our clients**, including hiring managers and startup founders
- **Top VCs and investors** across the U.S. who rely on Synapse to build their founding teams
- 10s of thousands of other hiring managers and potential future connections
- Our **SRN recruiter network of 1100+ professionals**, many of whom can connect you to incredible job and internship opportunities

This isn’t just a coding challenge — it's your **fast track to visibility, credibility, and opportunity**.

## **💰 Prizes**

**Top 2 Winners Each Receive:**

- $500 cash prize
- 2-month paid internship ($750/month = $1,500 total)
- Work directly with PhDs and top AI engineers
- Build production AI systems used by 1000s of recruiters and companies
- Strong potential for full-time offer post-graduation

## **🎯 The Challenge**

**Build a LinkedIn Sourcing Agent that:**

1. **Finds LinkedIn Profiles**
    - Takes a job description as input
    - Searches for relevant LinkedIn profile URLs
    - Extracts basic candidate data from search results
2. **Scores Candidates**
    - Implements our fit score rubric (provided below)
    - Rates candidates 1-10 based on job match
    - Shows scoring breakdown
3. **Generates Outreach**
    - Creates personalized LinkedIn messages using AI
    - References specific candidate details
    - Maintains professional tone
4. **Handles Scale**
    - Can process multiple jobs simultaneously
    - Manages rate limiting intelligently
    - Stores minimal data (just URLs + scores)

## **🏆 Bonus Points**

- **Multi-Source Enhancement**: Combine LinkedIn data with GitHub, Twitter, or personal websites to improve fit scoring
- **Smart Caching**: Implement intelligent caching to avoid re-fetching
- **Batch Processing**: Handle 10+ jobs in parallel
- **Confidence Scoring**: Show confidence levels when data is incomplete

## **⚙️ Technical Requirements**

### **Required Stack**

- **Development**: Must use Cursor
- **Language**: Python or TypeScript
- **LLM**: Any (OpenAI, Claude, etc.)
- **Data Storage**: Minimal (PostgreSQL, SQLite, or even JSON)

### **Required Features**

```python
# 1. Job Input
job_description = "Senior Backend Engineer at fintech startup..."

# 2. Candidate Discovery
candidates = agent.search_linkedin(job_description)
# Returns: [{"name": "John Doe", "linkedin_url": "...", "headline": "..."}]

# 3. Fit Scoring
scored_candidates = agent.score_candidates(candidates, job_description)
# Returns: [{"name": "...", "score": 8.5, "breakdown": {...}}]

# 4. Message Generation
messages = agent.generate_outreach(scored_candidates[:5], job_description)
# Returns: [{"candidate": "...", "message": "Hi John, I noticed..."}]

```

### **Example Architecture**

```
Input Job → Search LinkedIn → Extract Profiles → Score Fit → Generate Messages
     ↓                              ↓                ↓              ↓
   Queue → RapidAPI/Scraping → Parse Data → Fit Algorithm → GPT-4

```

## **📊 Fit Score Rubric (Simplified)**

Use this scoring framework:

**Education (20%)**

- Elite schools (MIT, Stanford, etc.): 9-10
- Strong schools: 7-8
- Standard universities: 5-6
- Clear progression: 8-10

**Career Trajectory (20%)**

- Steady growth: 6-8
- Limited progression: 3-5

**Company Relevance (15%)**

- Top tech companies: 9-10
- Relevant industry: 7-8
- Any experience: 5-6

**Experience Match (25%)**

- Perfect skill match: 9-10
- Strong overlap: 7-8
- Some relevant skills: 5-6

**Location Match (10%)**

- Exact city: 10
- Same metro: 8
- Remote-friendly: 6

**Tenure (10%)**

- 2-3 years average: 9-10
- 1-2 years: 6-8
- Job hopping: 3-5

## **🛠️ Resources We Provide**

### **Use the role below for your challenge:**

We're recruiting for a **Software Engineer, ML Research** role at **Windsurf** (the company behind Codeium) - a Forbes AI 50 company building AI-powered developer tools. They're looking for someone to train LLMs for code generation, with $140-300k + equity in Mountain View.

This is perfect for the challenge because Windsurf builds AI coding assistants (like Cursor!), so you'll be sourcing candidates who understand exactly what you're building with.

**Job Description To Use: [`https://app.synapserecruiternetwork.com/job-page/1750452159644x262203891027542000`](https://app.synapserecruiternetwork.com/job-page/1750452159644x262203891027542000)**

### **LinkedIn Search Options**

1. **Google Search**: `site:linkedin.com/in "backend engineer" "fintech" "San Francisco"`
2. **RapidAPI**: Fresh LinkedIn Data API (free tier available)
3. **Direct parsing**: Extract from search result snippets

### **Sample Output Format**

```json
{
  "job_id": "backend-fintech-sf",
  "candidates_found": 25,
  "top_candidates": [
    {
      "name": "Jane Smith",
      "linkedin_url": "linkedin.com/in/janesmith",
      "fit_score": 8.5,
      "score_breakdown": {
        "education": 9.0,
        "trajectory": 8.0,
        "company": 8.5,
        "skills": 9.0,
        "location": 10.0,
        "tenure": 7.0
      },
      "outreach_message": "Hi Jane, I noticed your 6 years..."
    }
  ]
}

```

## **📋 Submission Requirements**

1. **GitHub Repository** with your code
2. **README** with setup instructions
3. **Demo Video** (3 minutes max) showing:
    - Running your agent on a job
    - Candidates being discovered and scored
    - Generated outreach messages
4. **Brief Write-up** (500 words max):
    - Your approach
    - Challenges faced
    - How you'd scale to 100s of jobs
5. Bonus: Share an api link created using FastAPI hosted on huggingface:
- [ ]  which takes job description as input and returns top 10 candidates for that job along with there personalized outreach message.
- [ ]  The outreach message should highlighting there profile’s key characteristics and how it matches with this job all in json format.

## **⏰ Timeline**

- **Submit by**: Monday, June 30, 2025 @ 7:00 PM PST
- **Winners Announced**: within 24 hours after deadline

## **📝 How to Submit**

**Fill out submission form:** [**`https://forms.gle/v4byfXiGXFej5heq6`**](https://forms.gle/v4byfXiGXFej5heq6)

## **❓ FAQ**

**Q: Can I use web scraping libraries?**
A: Yes, any method to get LinkedIn URLs/data is fine.

**Q: What if I can't get full profile data?**
A: Work with what you can get. We care more about your approach than perfect data.

**Q: Should I worry about rate limiting?**
A: Basic rate limiting awareness is good. Don't overthink it for the MVP.

**Q: Can I use multiple LLMs?**
A: Yes, use whatever combination works best.

**Q: What about LinkedIn ToS?**
A: This is an educational challenge. Use public data responsibly.

## **💡 Tips for Success**

- **Start Simple**: Get basic search → score → message working first
- **Use Cursor AI**: Let it help you write boilerplate quickly
- **Focus on the Pipeline**: We care more about architecture than perfect accuracy
- **Show Your Thinking**: Comment your code, explain decisions
- **Make it Runnable**: We should be able to clone and run your code easily

## **🤝 About the Internship**

**What You'll Work On:**

- Production AI agents handling 10,000+ candidates/month
- Real-time matching algorithms
- Distributed scraping systems
- LLM optimization at scale

**Who You'll Work With:**

- AI engineers from top companies
- Researchers published in top conferences
- Full-stack engineers building at scale

**Location**: Fully remote
**Commitment**: 2 month contract
**Start Date**: this week

## **🚨 Final Notes**

- This is exactly what we build at Synapse
- The best solutions will actually be integrated into our platform
- We're looking for builders who can ship, not perfect code
- Using Cursor effectively is a key skill we value

**Questions?** email srn@synapserecruiternetwork.com

---

**Ready to build the future of recruiting?**

Start now: Fork our starter template → Build your agent → Submit ASAP