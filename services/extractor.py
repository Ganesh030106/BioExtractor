"""
Extractor Service
-----------------
Core NLP / regex-based extraction logic.
Each public function takes raw text and returns the extracted value (or None).
"""

import re
from datetime import datetime


# ------------------------------------------------------------------ #
#  Individual field extractors
# ------------------------------------------------------------------ #

def extract_name(text):
    """Extract name from text using pattern matching."""
    patterns = [
        r"(?:my name is|i am|i'm|this is|name is|myself)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        r"(?:my name is|i am|i'm|this is|name is|myself)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)*?)(?:\s*[,.]|\s+and\b|\s+i\b|\s+with\b|\s+from\b|\s+working\b|\s+currently\b|\s+a\s|\s+an\s)",
        r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s+here",
        r"(?:hi|hello|hey),?\s+(?:i am|i'm)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)?)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            stop_words = {
                "a", "an", "the", "working", "currently", "have", "having",
                "been", "doing", "passionate", "experienced", "skilled",
                "dedicated", "enthusiastic", "motivated", "highly", "very",
            }
            name_parts = name.split()
            cleaned = [p for p in name_parts if p.lower() not in stop_words]
            if cleaned:
                return " ".join(cleaned).title()
    return None


def extract_experience(text):
    """Extract years of experience."""
    patterns = [
        r"(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp|work)",
        r"(?:experience|exp)\s*(?:of\s+)?(\d+)\+?\s*(?:years?|yrs?)",
        r"(?:worked|working)\s+(?:for\s+)?(\d+)\+?\s*(?:years?|yrs?)",
        r"(\d+)\+?\s*(?:years?|yrs?)\s+(?:in\s+)?(?:the\s+)?(?:industry|field|domain|sector)",
        r"over\s+(\d+)\s*(?:years?|yrs?)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return f"{match.group(1)} years"
    return None


def extract_company(text):
    """Extract company name."""
    patterns = [
        r"(?:working|worked|work)\s+(?:at|in|for|with)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*(?:\s+(?:Inc|Corp|Ltd|LLC|Technologies|Tech|Solutions|Systems|Services|Software|Consulting|Labs|Group|Digital|Global|India|Pvt)\.?)?)",
        r"(?:company|organization|firm|employer)\s+(?:is|called|named)?\s*:?\s*([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)",
        r"(?:at|in|for|with)\s+([A-Z][a-zA-Z]+(?:\s+(?:Technologies|Tech|Solutions|Systems|Services|Software|Consulting|Labs|Group|Digital|Global|India|Pvt|Inc|Corp|Ltd|LLC)\.?)+)",
        r"(?:joined|join)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)",
    ]
    stop_companies = {"IT", "An", "The", "My", "This"}
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            company = match.group(1).strip()
            if company not in stop_companies and len(company) > 1:
                return company
    return None


def extract_tech_stacks(text):
    """Extract technology stacks and programming languages."""
    known_techs = [
        "Python", "Java", "JavaScript", "TypeScript", "C\\+\\+", "C#", "C",
        "Ruby", "PHP", "Swift", "Kotlin", "Go", "Golang", "Rust", "Scala",
        "R", "MATLAB", "Perl", "Dart", "Lua", "Haskell", "Elixir", "Clojure",
        "React", "React.js", "ReactJS", "Angular", "AngularJS", "Vue", "Vue.js",
        "VueJS", "Next.js", "NextJS", "Nuxt.js", "Svelte", "jQuery",
        "Node.js", "NodeJS", "Express", "Express.js", "Django", "Flask",
        "Spring", "Spring Boot", "SpringBoot", "FastAPI", "Rails",
        "Ruby on Rails", "Laravel", "ASP.NET", ".NET", "NestJS",
        "HTML", "HTML5", "CSS", "CSS3", "SASS", "SCSS", "Tailwind",
        "TailwindCSS", "Bootstrap", "Material UI", "MUI",
        "MySQL", "PostgreSQL", "Postgres", "MongoDB", "Redis", "SQLite",
        "Oracle", "SQL Server", "DynamoDB", "Cassandra", "Firebase",
        "Firestore", "MariaDB", "Elasticsearch",
        "AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes",
        "K8s", "Jenkins", "Git", "GitHub", "GitLab", "Bitbucket",
        "Terraform", "Ansible", "CI/CD", "CircleCI", "Travis CI",
        "Nginx", "Apache", "Linux", "Ubuntu",
        "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Sklearn",
        "Pandas", "NumPy", "Matplotlib", "OpenCV", "NLP", "NLTK",
        "SpaCy", "Hugging Face",
        "REST", "RESTful", "GraphQL", "gRPC", "WebSocket",
        "Microservices", "Serverless", "Lambda",
        "Jira", "Confluence", "Slack", "VS Code", "IntelliJ",
        "Android", "iOS", "Flutter", "React Native", "Xamarin",
        "Selenium", "Jest", "Mocha", "Cypress", "Pytest",
        "Figma", "Adobe XD", "Photoshop", "Illustrator",
        "Power BI", "Tableau", "Excel", "VBA",
        "Blockchain", "Solidity", "Web3", "Ethereum",
        "RabbitMQ", "Kafka", "Apache Kafka",
        "Hadoop", "Spark", "Apache Spark", "Airflow",
        "Unity", "Unreal Engine",
        "SAP", "Salesforce", "ServiceNow",
    ]

    found_techs = set()
    for tech in known_techs:
        pattern = r'\b' + tech.replace('.', r'\.').replace('+', r'\+') + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            found_techs.add(tech.replace("\\+", "+").replace("\\.", "."))

    return sorted(list(found_techs)) if found_techs else None


def extract_role(text):
    """Extract job role/title."""
    roles = [
        "Software Engineer", "Software Developer", "Web Developer",
        "Full Stack Developer", "Full-Stack Developer", "Fullstack Developer",
        "Frontend Developer", "Front-End Developer", "Front End Developer",
        "Backend Developer", "Back-End Developer", "Back End Developer",
        "DevOps Engineer", "Data Scientist", "Data Analyst", "Data Engineer",
        "Machine Learning Engineer", "ML Engineer", "AI Engineer",
        "Cloud Engineer", "Cloud Architect", "Solutions Architect",
        "System Administrator", "SysAdmin", "Database Administrator", "DBA",
        "QA Engineer", "Test Engineer", "SDET", "QA Analyst",
        "Product Manager", "Project Manager", "Scrum Master",
        "Technical Lead", "Tech Lead", "Team Lead", "Engineering Manager",
        "CTO", "VP Engineering", "Director of Engineering",
        "UI Developer", "UX Designer", "UI/UX Designer", "Product Designer",
        "Mobile Developer", "Android Developer", "iOS Developer",
        "Security Engineer", "Cybersecurity Analyst", "Penetration Tester",
        "Network Engineer", "System Engineer", "IT Administrator",
        "Business Analyst", "Consultant", "Technical Consultant",
        "Fresher", "Intern", "Trainee", "Graduate",
        "Architect", "Principal Engineer", "Staff Engineer", "Senior Engineer",
    ]

    for role in roles:
        if re.search(r'\b' + re.escape(role) + r'\b', text, re.IGNORECASE):
            return role

    # Fallback: pattern-based extraction
    patterns = [
        r"(?:work|working|worked)\s+as\s+(?:a\s+)?(.+?)(?:\s+at|\s+in|\s+for|\s+with|\.|,|$)",
        r"(?:i am|i'm)\s+(?:a\s+)?(.+?)(?:\s+at|\s+in|\s+for|\s+with|\.|,|\s+and\b)",
        r"(?:role|position|designation|title)\s+(?:is|as|:)\s*(.+?)(?:\.|,|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            role = match.group(1).strip()
            if 3 < len(role) < 50:
                return role.title()

    return None


def extract_education(text):
    """Extract education information."""
    degrees = []
    degree_patterns = [
        r"\b(B\.?Tech|B\.?E|B\.?Sc|B\.?S|B\.?A|B\.?Com|B\.?C\.?A|BCA|BBA)\b",
        r"\b(M\.?Tech|M\.?E|M\.?Sc|M\.?S|M\.?A|M\.?Com|M\.?C\.?A|MCA|MBA)\b",
        r"\b(Ph\.?D|Doctorate|M\.?Phil)\b",
        r"\b(Diploma|Certificate)\b",
        r"\b(Computer Science|Information Technology|Electronics|Mechanical|Civil|Electrical|ECE|CSE|IT|EEE)\b",
    ]
    for pattern in degree_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        degrees.extend(matches)

    return list(set(degrees)) if degrees else None


def extract_location(text):
    """Extract location/city information."""
    patterns = [
        r"(?:from|based in|located in|live in|living in|residing in|resident of|based at|based out of|city|location)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        r"(?:Chennai|Bangalore|Bengaluru|Mumbai|Delhi|Hyderabad|Pune|Kolkata|Ahmedabad|Jaipur|Lucknow|Kanpur|Nagpur|Visakhapatnam|Bhopal|Patna|Ludhiana|Agra|Vadodara|Coimbatore|Kochi|Indore|Chandigarh|Surat|Thiruvananthapuram|New York|San Francisco|London|Berlin|Tokyo|Singapore|Dubai|Toronto|Sydney|Austin|Seattle|Boston|Chicago)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip() if match.lastindex is None else match.group(1).strip()
    return None


def extract_email(text):
    """Extract email address."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_phone(text):
    """Extract phone number."""
    patterns = [
        r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'(?:\+?\d{1,3}[-.\s]?)?\d{10}',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0).strip()
    return None


def extract_linkedin(text):
    """Extract LinkedIn profile URL."""
    pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0) if match else None


def extract_github(text):
    """Extract GitHub profile URL."""
    pattern = r'(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0) if match else None


def extract_interests(text):
    """Extract hobbies and interests."""
    patterns = [
        r"(?:hobbies|interests|passionate about|love|enjoy|like)\s+(?:are|include|:)?\s*(.+?)(?:\.|$)",
        r"(?:interested in|keen on|fascinated by)\s+(.+?)(?:\.|,|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            interests_text = match.group(1).strip()
            interests = [
                i.strip()
                for i in re.split(r'[,]|(?:\s+and\s+)', interests_text)
                if i.strip()
            ]
            return interests if interests else None
    return None


# ------------------------------------------------------------------ #
#  Orchestrator
# ------------------------------------------------------------------ #

def extract_info(text):
    """
    Main extraction function.
    Runs every individual extractor and returns a unified dict with timestamp.
    """
    return {
        "name": extract_name(text),
        "role": extract_role(text),
        "experience": extract_experience(text),
        "company": extract_company(text),
        "tech_stacks": extract_tech_stacks(text),
        "education": extract_education(text),
        "location": extract_location(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": extract_linkedin(text),
        "github": extract_github(text),
        "interests": extract_interests(text),
        "raw_text": text,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
