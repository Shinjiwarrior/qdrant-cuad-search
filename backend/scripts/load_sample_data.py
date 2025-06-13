#!/usr/bin/env python3
"""
Script to load sample legal cases into the Qdrant vector database.
This creates a small dataset (~500 cases) for demonstration purposes.
"""

import asyncio
import json
import uuid
import sys
import os
from datetime import datetime, timedelta
import random

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.services.search_service import search_service

# Sample legal cases data
SAMPLE_CASES = [
    {
        "case_name": "Miranda v. Arizona",
        "citation": "384 U.S. 436 (1966)",
        "court": "Supreme Court of the United States",
        "jurisdiction": "federal",
        "court_level": "supreme",
        "case_type": "criminal",
        "date_filed": "1966-06-13",
        "summary": "The Supreme Court held that criminal suspects must be informed of their rights before interrogation.",
        "full_text": "Prior to any questioning, the person must be warned that he has a right to remain silent, that any statement he does make may be used as evidence against him, and that he has a right to the presence of an attorney...",
        "url": "https://supreme.justia.com/cases/federal/us/384/436/"
    },
    {
        "case_name": "Brown v. Board of Education",
        "citation": "347 U.S. 483 (1954)",
        "court": "Supreme Court of the United States", 
        "jurisdiction": "federal",
        "court_level": "supreme",
        "case_type": "constitutional",
        "date_filed": "1954-05-17",
        "summary": "Landmark decision declaring racial segregation in public schools unconstitutional.",
        "full_text": "We conclude that in the field of public education the doctrine of 'separate but equal' has no place. Separate educational facilities are inherently unequal...",
        "url": "https://supreme.justia.com/cases/federal/us/347/483/"
    },
    {
        "case_name": "Roe v. Wade",
        "citation": "410 U.S. 113 (1973)",
        "court": "Supreme Court of the United States",
        "jurisdiction": "federal", 
        "court_level": "supreme",
        "case_type": "constitutional",
        "date_filed": "1973-01-22",
        "summary": "Established constitutional right to abortion under the Due Process Clause.",
        "full_text": "This right of privacy, whether it be founded in the Fourteenth Amendment's concept of personal liberty... is broad enough to encompass a woman's decision whether or not to terminate her pregnancy...",
        "url": "https://supreme.justia.com/cases/federal/us/410/113/"
    },
    {
        "case_name": "Marbury v. Madison",
        "citation": "5 U.S. 137 (1803)",
        "court": "Supreme Court of the United States",
        "jurisdiction": "federal",
        "court_level": "supreme", 
        "case_type": "constitutional",
        "date_filed": "1803-02-24",
        "summary": "Established the principle of judicial review in American constitutional law.",
        "full_text": "It is emphatically the province and duty of the judicial department to say what the law is. Those who apply the rule to particular cases, must of necessity expound and interpret that rule...",
        "url": "https://supreme.justia.com/cases/federal/us/5/137/"
    },
    {
        "case_name": "Gideon v. Wainwright",
        "citation": "372 U.S. 335 (1963)",
        "court": "Supreme Court of the United States",
        "jurisdiction": "federal",
        "court_level": "supreme",
        "case_type": "criminal", 
        "date_filed": "1963-03-18",
        "summary": "Established right to counsel for defendants in criminal cases who cannot afford an attorney.",
        "full_text": "The right of one charged with crime to counsel may not be deemed fundamental and essential to fair trials in some countries, but it is in ours...",
        "url": "https://supreme.justia.com/cases/federal/us/372/335/"
    }
]

# Additional case templates for generating more data
CASE_TEMPLATES = [
    {
        "case_types": ["criminal", "civil", "constitutional", "administrative"],
        "courts": ["Supreme Court", "Court of Appeals", "District Court", "State Supreme Court"],
        "jurisdictions": ["federal", "california", "new_york", "texas", "florida", "illinois"],
        "court_levels": ["supreme", "appellate", "district", "trial"]
    }
]

def generate_random_cases(num_cases: int = 500) -> list:
    """Generate random legal cases for testing."""
    cases = SAMPLE_CASES.copy()
    
    # Common legal topics for case generation
    topics = [
        "contract dispute", "personal injury", "employment discrimination", 
        "intellectual property", "environmental law", "tax law", "immigration",
        "family law", "bankruptcy", "securities fraud", "medical malpractice",
        "civil rights", "labor law", "antitrust", "criminal procedure",
        "search and seizure", "due process", "equal protection", "free speech",
        "property rights", "corporate law", "insurance claims", "real estate"
    ]
    
    case_name_templates = [
        "{plaintiff} v. {defendant}",
        "State v. {defendant}",
        "United States v. {defendant}",
        "In re {subject}",
        "{company} Corp. v. {plaintiff}"
    ]
    
    for i in range(num_cases - len(SAMPLE_CASES)):
        # Generate random case data
        topic = random.choice(topics)
        case_type = random.choice(["criminal", "civil", "constitutional", "administrative", "contract", "tort"])
        jurisdiction = random.choice(["federal", "california", "new_york", "texas", "florida", "illinois"])
        court_level = random.choice(["supreme", "appellate", "district", "trial"])
        
        # Generate case name
        if case_type == "criminal":
            case_name = f"State v. {random.choice(['Johnson', 'Smith', 'Williams', 'Brown', 'Davis'])}"
        else:
            plaintiff = random.choice(['Johnson', 'Smith', 'Williams', 'Brown', 'Davis', 'Miller', 'Wilson'])
            defendant = random.choice(['Corp Inc.', 'LLC', 'City of Springfield', 'County Hospital', 'University'])
            case_name = f"{plaintiff} v. {defendant}"
        
        # Generate date within last 50 years
        start_date = datetime.now() - timedelta(days=365*50)
        random_date = start_date + timedelta(days=random.randint(0, 365*50))
        
        case = {
            "id": str(uuid.uuid4()),
            "case_name": case_name,
            "citation": f"{random.randint(100, 999)} F.{random.randint(2,3)}d {random.randint(1, 999)} ({random.randint(1970, 2023)})",
            "court": f"{random.choice(['U.S. District Court', 'Court of Appeals', 'State Supreme Court', 'Superior Court'])} for {jurisdiction.title()}",
            "jurisdiction": jurisdiction,
            "court_level": court_level,
            "case_type": case_type,
            "date_filed": random_date.strftime("%Y-%m-%d"),
            "summary": f"This case involves {topic} and addresses important legal questions regarding {random.choice(['constitutional rights', 'statutory interpretation', 'common law principles', 'procedural requirements'])}.",
            "full_text": f"This {case_type} case centers on {topic}. The court must determine whether the defendant's actions constitute a violation of applicable law. The plaintiff argues that established precedent supports their position, while the defendant contends that the circumstances warrant a different legal analysis. After careful consideration of the evidence and legal arguments presented, the court finds that the relevant statutes and case law support the conclusion that...",
            "url": f"https://example.com/cases/{str(uuid.uuid4())[:8]}"
        }
        
        cases.append(case)
    
    return cases

async def load_data():
    """Load sample data into the vector database."""
    print("🚀 Starting sample data loading...")
    
    try:
        # Initialize Qdrant collection first
        print("🔧 Initializing Qdrant collection...")
        await search_service.qdrant_service.initialize_collection()
        
        # Generate sample cases
        print("📝 Generating sample legal cases...")
        cases = generate_random_cases(500)
        
        # Add unique IDs to cases that don't have them
        for case in cases:
            if 'id' not in case:
                case['id'] = str(uuid.uuid4())
        
        print(f"📊 Generated {len(cases)} sample cases")
        
        # Load cases into the search index
        print("🔄 Adding cases to search index...")
        await search_service.add_cases_to_index(cases)
        
        print("✅ Sample data loaded successfully!")
        print(f"📈 Total cases in database: {len(cases)}")
        
        # Save sample data to JSON file for reference
        print("💾 Saving sample data to JSON file...")
        with open('sample_data.json', 'w') as f:
            json.dump(cases, f, indent=2, default=str)
        
        print("🎉 All done! You can now start searching.")
        
    except Exception as e:
        print(f"❌ Error loading sample data: {str(e)}")
        raise

if __name__ == "__main__":
    print("🔍 Baby Caselaw AI - Sample Data Loader")
    print("=" * 50)
    
    # Run the async function
    asyncio.run(load_data()) 