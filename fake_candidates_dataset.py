"""
Fake LinkedIn Candidates Dataset
Based on the Synapse Fit Score Rubric
"""

import random
from typing import List, Dict, Any

# Elite schools (9-10 points)
ELITE_SCHOOLS = [
    "MIT", "Stanford University", "Harvard University", "UC Berkeley", 
    "Carnegie Mellon University", "Caltech", "Princeton University", "Yale University"
]

# Strong schools (7-8 points)
STRONG_SCHOOLS = [
    "UCLA", "USC", "NYU", "Columbia University", "Cornell University", 
    "Georgia Tech", "University of Michigan", "University of Illinois", "UT Austin"
]

# Standard universities (5-6 points)
STANDARD_SCHOOLS = [
    "San Jose State University", "Santa Clara University", "UC Davis", 
    "UC Irvine", "UC San Diego", "University of Washington", "University of Oregon"
]

# Top tech companies (9-10 points)
TOP_TECH_COMPANIES = [
    "Google", "Microsoft", "Apple", "Amazon", "Meta", "Netflix", "Airbnb", 
    "Uber", "OpenAI", "Anthropic", "Stripe", "Palantir", "Databricks"
]

# Relevant tech companies (7-8 points)
RELEVANT_TECH_COMPANIES = [
    "Salesforce", "Adobe", "Oracle", "Intel", "NVIDIA", "AMD", "Cisco", 
    "VMware", "Splunk", "MongoDB", "Datadog", "Snowflake", "Twilio"
]

# Standard companies (5-6 points)
STANDARD_COMPANIES = [
    "Bank of America", "Wells Fargo", "JP Morgan", "Goldman Sachs", 
    "McKinsey", "Bain", "BCG", "Deloitte", "PwC", "EY"
]

# Job titles for ML/AI roles
ML_JOB_TITLES = [
    "Senior ML Engineer", "Machine Learning Engineer", "AI Research Engineer",
    "ML Research Engineer", "Senior Software Engineer - ML", "AI Engineer",
    "Deep Learning Engineer", "ML Scientist", "AI Research Scientist",
    "Software Engineer - ML", "ML Infrastructure Engineer", "AI/ML Engineer"
]

# Skills for ML/AI roles
ML_SKILLS = [
    "Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning",
    "Natural Language Processing", "Computer Vision", "LLMs", "Code Generation",
    "Neural Networks", "Scikit-learn", "Pandas", "NumPy", "Jupyter",
    "Docker", "Kubernetes", "AWS", "GCP", "Azure", "Git", "SQL"
]

# Locations
LOCATIONS = [
    "Mountain View, CA", "San Francisco, CA", "Palo Alto, CA", "San Jose, CA",
    "Seattle, WA", "New York, NY", "Austin, TX", "Boston, MA", "Los Angeles, CA",
    "Denver, CO", "Chicago, IL", "Atlanta, GA", "Remote"
]

# Names for diversity
FIRST_NAMES = [
    "Sarah", "Michael", "Emily", "David", "Jessica", "Christopher", "Ashley",
    "Matthew", "Amanda", "Joshua", "Stephanie", "Andrew", "Nicole", "Daniel",
    "Rachel", "James", "Lauren", "Ryan", "Megan", "Justin", "Hannah", "Brandon",
    "Amber", "Tyler", "Samantha", "Kevin", "Danielle", "Brian", "Brittany",
    "Steven", "Melissa", "Timothy", "Christina", "Jeffrey", "Heather", "Mark",
    "Michelle", "Paul", "Tiffany", "Donald", "Kimberly", "Kenneth", "Crystal",
    "Anthony", "Stephanie", "Charles", "Katherine", "Thomas", "Laura", "Jason",
    "Amy", "Ronald", "Angela", "Edward", "Sharon", "Brian", "Emma", "Kevin",
    "Lisa", "Jason", "Nancy", "Jeffrey", "Karen", "Ryan", "Betty", "Jacob",
    "Helen", "Gary", "Sandra", "Nicholas", "Donna", "Eric", "Carol", "Jonathan",
    "Ruth", "Stephen", "Julie", "Larry", "Joyce", "Justin", "Virginia", "Scott",
    "Victoria", "Brandon", "Kelly", "Benjamin", "Lauren", "Frank", "Christine",
    "Gregory", "Joan", "Raymond", "Evelyn", "Samuel", "Cheryl", "Patrick",
    "Megan", "Alexander", "Andrea", "Jack", "Hannah", "Dennis", "Jacqueline",
    "Jerry", "Martha", "Tyler", "Gloria", "Aaron", "Teresa", "Jose", "Ann",
    "Adam", "Sara", "Nathan", "Madison", "Henry", "Frances", "Douglas", "Kathryn",
    "Peter", "Janice", "Zachary", "Jean", "Kyle", "Abigail", "Walter", "Alice",
    "Harold", "Julia", "Jeremy", "Judy", "Ethan", "Sophia", "Carl", "Grace",
    "Keith", "Denise", "Roger", "Amber", "Gerald", "Doris", "Christian", "Marilyn",
    "Terry", "Danielle", "Sean", "Beverly", "Arthur", "Madison", "Austin", "Theresa",
    "Noah", "Mia", "Lawrence", "Diana", "Jesse", "Brittany", "Joe", "Natalie",
    "Bryan", "Sofia", "Billy", "Chloe", "Jordan", "Aria", "Albert", "Avery",
    "Dylan", "Ella", "Bruce", "Stella", "Willie", "Nora", "Gabriel", "Ellie",
    "Alan", "Lily", "Juan", "Hazel", "Logan", "Violet", "Wayne", "Aurora",
    "Roy", "Lucy", "Ralph", "Anna", "Randy", "Sadie", "Eugene", "Aria",
    "Vincent", "Lillian", "Russell", "Aubrey", "Elijah", "Brooklyn", "Louis",
    "Paisley", "Bobby", "Savannah", "Philip", "Claire", "Johnny", "Skylar"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Kim", "Chen", "Zhang", "Wang", "Li",
    "Singh", "Patel", "Kumar", "Sharma", "Gupta", "Malhotra", "Kapoor",
    "Reddy", "Khan", "Ali", "Hassan", "Ahmed", "Rahman", "Hussain", "Ibrahim",
    "Omar", "Mahmoud", "Saleh", "Abdullah", "Mohammed", "Yusuf", "Hassan",
    "Garcia", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera", "Gomez",
    "Cruz", "Morales", "Reyes", "Jimenez", "Moreno", "Alvarez", "Romero",
    "Gutierrez", "Castro", "Vargas", "Mendoza", "Ramos", "Ruiz", "Diaz",
    "Herrera", "Medina", "Aguilar", "Vega", "Castillo", "Ortiz", "Silva",
    "Nunez", "Cruz", "Flores", "Reyes", "Morales", "Gutierrez", "Castro",
    "Vargas", "Mendoza", "Ramos", "Ruiz", "Diaz", "Herrera", "Medina",
    "Aguilar", "Vega", "Castillo", "Ortiz", "Silva", "Nunez", "Cruz",
    "Flores", "Reyes", "Morales", "Gutierrez", "Castro", "Vargas", "Mendoza"
]

def generate_fake_candidates(job_description: str, num_candidates: int = 50) -> List[Dict[str, Any]]:
    """
    Generate fake LinkedIn candidates based on the job description and scoring rubric.
    
    Args:
        job_description: The job description to match candidates against
        num_candidates: Number of candidates to generate
    
    Returns:
        List of candidate dictionaries with realistic profile data
    """
    candidates = []
    
    # Extract job requirements from description
    job_lower = job_description.lower()
    is_ml_role = any(term in job_lower for term in ["ml", "machine learning", "ai", "llm", "code generation"])
    is_senior = any(term in job_lower for term in ["senior", "lead", "principal", "staff"])
    is_mountain_view = "mountain view" in job_lower
    is_california = "california" in job_lower or "ca" in job_lower
    
    for i in range(num_candidates):
        # Generate name
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}"
        
        # Generate LinkedIn URL
        linkedin_url = f"linkedin.com/in/{first_name.lower()}-{last_name.lower()}-{random.randint(100, 999)}"
        
        # Generate education based on scoring
        education_quality = random.choices(
            ["elite", "strong", "standard"],
            weights=[0.2, 0.4, 0.4]  # 20% elite, 40% strong, 40% standard
        )[0]
        
        if education_quality == "elite":
            school = random.choice(ELITE_SCHOOLS)
            degree = random.choice(["MS Computer Science", "PhD Computer Science", "MS Machine Learning"])
        elif education_quality == "strong":
            school = random.choice(STRONG_SCHOOLS)
            degree = random.choice(["MS Computer Science", "BS Computer Science", "MS Data Science"])
        else:
            school = random.choice(STANDARD_SCHOOLS)
            degree = random.choice(["BS Computer Science", "BS Engineering", "MS Software Engineering"])
        
        education = f"{school}, {degree}"
        
        # Generate experience years
        if is_senior:
            experience_years = random.randint(4, 12)
        else:
            experience_years = random.randint(1, 6)
        
        experience = f"{experience_years} years"
        
        # Generate company based on scoring
        company_quality = random.choices(
            ["top", "relevant", "standard"],
            weights=[0.3, 0.5, 0.2]  # 30% top, 50% relevant, 20% standard
        )[0]
        
        if company_quality == "top":
            company = random.choice(TOP_TECH_COMPANIES)
        elif company_quality == "relevant":
            company = random.choice(RELEVANT_TECH_COMPANIES)
        else:
            company = random.choice(STANDARD_COMPANIES)
        
        # Generate job title
        if is_ml_role:
            job_title = random.choice(ML_JOB_TITLES)
        else:
            job_title = random.choice([
                "Senior Software Engineer", "Software Engineer", "Backend Engineer",
                "Full Stack Engineer", "DevOps Engineer", "Data Engineer"
            ])
        
        headline = f"{job_title} at {company}"
        
        # Generate location
        if is_mountain_view:
            location = "Mountain View, CA"
        elif is_california:
            location = random.choice([loc for loc in LOCATIONS if "CA" in loc])
        else:
            location = random.choice(LOCATIONS)
        
        # Generate skills
        if is_ml_role:
            num_skills = random.randint(4, 8)
            skills = random.sample(ML_SKILLS, num_skills)
        else:
            skills = random.sample([
                "Python", "Java", "JavaScript", "React", "Node.js", "SQL",
                "Docker", "Kubernetes", "AWS", "Git", "REST APIs", "Microservices"
            ], random.randint(4, 8))
        
        skills_str = ", ".join(skills)
        
        # Generate tenure at current role
        tenure_years = random.randint(1, 5)
        tenure_months = random.randint(0, 11)
        if tenure_months == 0:
            tenure = f"{tenure_years} years"
        else:
            tenure = f"{tenure_years} years {tenure_months} months"
        
        candidate = {
            "name": name,
            "linkedin_url": linkedin_url,
            "headline": headline,
            "location": location,
            "experience": experience,
            "education": education,
            "skills": skills_str,
            "company": company,
            "tenure": tenure
        }
        
        candidates.append(candidate)
    
    return candidates

def get_sample_job_description() -> str:
    """Return the sample job description from the challenge."""
    return """Software Engineer, ML Research at Windsurf (Codeium)

We're looking for a Software Engineer to train LLMs for code generation. You'll work on cutting-edge AI models that power developer tools.

Requirements:
- Strong Python and machine learning experience
- Experience with PyTorch/TensorFlow
- Located in Mountain View, CA
- 3+ years of experience
- MS/PhD in Computer Science preferred

Compensation: $140-300k + equity"""

if __name__ == "__main__":
    # Test the dataset generation
    job_desc = get_sample_job_description()
    candidates = generate_fake_candidates(job_desc, 10)
    
    print("Sample Generated Candidates:")
    for i, candidate in enumerate(candidates, 1):
        print(f"\n{i}. {candidate['name']}")
        print(f"   {candidate['headline']}")
        print(f"   {candidate['location']}")
        print(f"   Experience: {candidate['experience']}")
        print(f"   Education: {candidate['education']}")
        print(f"   Skills: {candidate['skills']}")
        print(f"   LinkedIn: {candidate['linkedin_url']}") 