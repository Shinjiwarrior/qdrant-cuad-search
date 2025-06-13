#!/usr/bin/env python3
"""
Script to download and process the full CUAD (Contract Understanding Atticus Dataset)
for integration into our legal search system.

This processes all 510 real commercial contracts with proper metadata extraction.
"""

import asyncio
import json
import uuid
import logging
import re
from datasets import load_dataset
from typing import List, Dict, Any, Set
from pathlib import Path
from collections import defaultdict

# Import our services
import sys
sys.path.append('..')
from app.services.qdrant_service import QdrantService
from app.services.openai_service import OpenAIService
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FullCUADProcessor:
    def __init__(self):
        self.qdrant_service = QdrantService()
        self.openai_service = OpenAIService()
        
        # Industry mapping based on contract content
        self.industry_keywords = {
            'Technology': ['software', 'technology', 'tech', 'data', 'platform', 'digital', 'internet', 'cloud', 'saas'],
            'Healthcare': ['health', 'medical', 'pharma', 'pharmaceutical', 'clinical', 'hospital', 'patient'],
            'Financial Services': ['financial', 'bank', 'investment', 'securities', 'fund', 'credit', 'loan'],
            'Manufacturing': ['manufacturing', 'production', 'industrial', 'factory', 'equipment', 'machinery'],
            'Real Estate': ['real estate', 'property', 'land', 'building', 'lease', 'rental', 'premises'],
            'Entertainment': ['entertainment', 'media', 'film', 'music', 'content', 'publishing', 'broadcast'],
            'Energy': ['energy', 'oil', 'gas', 'renewable', 'power', 'utilities', 'solar', 'wind'],
            'Retail': ['retail', 'consumer', 'sales', 'marketing', 'distribution', 'merchandise'],
            'Transportation': ['transportation', 'logistics', 'shipping', 'delivery', 'fleet', 'automotive'],
            'Telecommunications': ['telecom', 'communications', 'wireless', 'network', 'mobile', 'phone'],
            'Education': ['education', 'university', 'school', 'training', 'academic', 'learning'],
            'Government': ['government', 'public', 'municipal', 'federal', 'state', 'agency'],
            'Other': []  # Default fallback
        }
        
        # Contract type keywords
        self.contract_type_keywords = {
            'employment_contract': ['employment', 'employee', 'work', 'job', 'salary', 'compensation'],
            'license_agreement': ['license', 'licensing', 'intellectual property', 'copyright', 'patent'],
            'service_agreement': ['service', 'services', 'professional', 'consulting', 'advisory'],
            'supply_agreement': ['supply', 'supplier', 'vendor', 'procurement', 'purchase'],
            'merger_agreement': ['merger', 'acquisition', 'purchase', 'buyout', 'consolidation'],
            'lease_agreement': ['lease', 'rent', 'rental', 'premises', 'property', 'space'],
            'partnership_agreement': ['partnership', 'joint venture', 'collaboration', 'alliance'],
            'non_disclosure_agreement': ['non-disclosure', 'nda', 'confidentiality', 'confidential'],
            'distribution_agreement': ['distribution', 'distributor', 'reseller', 'sales'],
            'loan_agreement': ['loan', 'credit', 'financing', 'debt', 'borrower', 'lender'],
            'other_contract': []  # Default fallback
        }
        
        # Company size indicators
        self.company_size_keywords = {
            'Startup': ['startup', 'llc', 'inc.', 'corporation', 'small business'],
            'SMB': ['company', 'business', 'firm', 'enterprises'],
            'Enterprise': ['corporation', 'corp', 'international', 'global', 'holdings'],
            'Fortune 500': ['international', 'global', 'worldwide', 'multinational']
        }
        
        # Jurisdictions
        self.jurisdiction_keywords = {
            'California': ['california', 'ca', 'san francisco', 'los angeles', 'silicon valley'],
            'New York': ['new york', 'ny', 'manhattan', 'nyc'],
            'Delaware': ['delaware', 'de', 'wilmington'],
            'Texas': ['texas', 'tx', 'houston', 'dallas', 'austin'],
            'Florida': ['florida', 'fl', 'miami', 'tampa'],
            'Illinois': ['illinois', 'il', 'chicago'],
            'Massachusetts': ['massachusetts', 'ma', 'boston'],
            'Washington': ['washington', 'wa', 'seattle'],
            'United Kingdom': ['uk', 'united kingdom', 'england', 'london'],
            'Canada': ['canada', 'canadian', 'toronto', 'vancouver'],
            'International': ['international', 'global', 'worldwide']
        }
        
    def load_cuad_dataset(self):
        """Download full CUAD dataset from Hugging Face"""
        logger.info("Loading full CUAD dataset from Hugging Face...")
        
        # Load the complete dataset
        dataset = load_dataset("theatticusproject/cuad", split="train")
        logger.info(f"Loaded {len(dataset)} total entries from CUAD")
        
        return dataset
    
    def extract_keywords(self, text: str, keyword_dict: Dict[str, List[str]]) -> str:
        """Extract the best matching category based on keywords in text"""
        text_lower = text.lower()
        scores = defaultdict(int)
        
        for category, keywords in keyword_dict.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[category] += 1
        
        # Return category with highest score, or default
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        # Return default category
        return list(keyword_dict.keys())[-1]  # Usually 'Other' or similar
    
    def process_cuad_to_contracts(self, dataset) -> List[Dict[str, Any]]:
        """Convert CUAD dataset entries to our contract format with rich metadata"""
        contracts = []
        
        # Group entries by document to get complete contracts
        document_groups = defaultdict(list)
        
        logger.info("Grouping CUAD entries by document...")
        for entry in dataset:
            # Skip empty or invalid entries
            if not entry.get('context') or not entry.get('context').strip():
                continue
                
            # Use title as document identifier, fallback to index
            doc_id = entry.get('title', f'document_{len(document_groups)}')
            document_groups[doc_id].append(entry)
        
        logger.info(f"Found {len(document_groups)} unique documents")
        
        # Process each document group into a contract
        for doc_idx, (doc_id, entries) in enumerate(document_groups.items()):
            if doc_idx >= 510:  # CUAD has 510 contracts max
                break
                
            # Combine all context from entries for this document
            full_text_parts = []
            questions_answered = set()
            
            for entry in entries:
                context = entry.get('context', '').strip()
                question = entry.get('question', '').strip()
                
                if context and context not in full_text_parts:
                    full_text_parts.append(context)
                
                if question:
                    questions_answered.add(question)
            
            # Skip if no meaningful content
            if not full_text_parts:
                continue
                
            full_text = '\n\n'.join(full_text_parts)
            
            # Skip very short contracts
            if len(full_text) < 500:
                continue
            
            # Extract metadata using our keyword matching
            industry = self.extract_keywords(full_text, self.industry_keywords)
            contract_type = self.extract_keywords(full_text, self.contract_type_keywords)
            company_size = self.extract_keywords(full_text, self.company_size_keywords)
            jurisdiction = self.extract_keywords(full_text, self.jurisdiction_keywords)
            
            # Create contract name based on type and content
            contract_name = self.generate_contract_name(full_text, contract_type, doc_idx + 1)
            
            # Generate summary from first meaningful paragraph
            summary = self.generate_summary(full_text)
            
            # Determine complexity and risk levels
            complexity_level = self.assess_complexity(full_text)
            risk_level = self.assess_risk(full_text)
            
            # Create contract entry
            contract = {
                'id': str(uuid.uuid4()),
                'case_name': contract_name,
                'citation': f"CUAD-{doc_idx + 1:03d}",
                'court': 'Commercial Transaction',
                'jurisdiction': jurisdiction,
                'court_level': 'contract',
                'case_type': contract_type,
                'date_filed': '2021-01-01',  # CUAD dataset publication year
                'summary': summary,
                'full_text': full_text,
                'url': f"https://huggingface.co/datasets/theatricusproject/cuad",
                
                # Rich metadata for filtering
                'industry': industry,
                'company_size': company_size,
                'complexity_level': complexity_level,
                'risk_level': risk_level,
                'contract_status': 'Active',  # Default assumption
                'renewal_terms': 'Standard',  # Default assumption
                
                # CUAD-specific metadata
                'cuad_document_id': doc_id,
                'questions_covered': len(questions_answered),
                'contract_length': len(full_text),
                'clause_count': len(full_text_parts)
            }
            
            contracts.append(contract)
            
            if len(contracts) % 50 == 0:
                logger.info(f"Processed {len(contracts)} contracts...")
        
        logger.info(f"Successfully processed {len(contracts)} complete contracts from CUAD dataset")
        return contracts
    
    def generate_contract_name(self, text: str, contract_type: str, index: int) -> str:
        """Generate a descriptive contract name"""
        text_lower = text.lower()
        
        # Try to extract company names (simple heuristic)
        company_patterns = [
            r'\b([A-Z][a-z]+ (?:Inc|Corp|LLC|Ltd|Corporation|Company)\.?)\b',
            r'\b([A-Z][a-z]+ [A-Z][a-z]+) (?:Inc|Corp|LLC|Ltd)\b'
        ]
        
        companies = set()
        for pattern in company_patterns:
            matches = re.findall(pattern, text[:1000])  # Check first 1000 chars
            companies.update(matches)
        
        # Create name based on contract type and companies found
        type_names = {
            'employment_contract': 'Employment Agreement',
            'license_agreement': 'License Agreement', 
            'service_agreement': 'Service Agreement',
            'supply_agreement': 'Supply Agreement',
            'merger_agreement': 'M&A Agreement',
            'lease_agreement': 'Lease Agreement',
            'partnership_agreement': 'Partnership Agreement',
            'non_disclosure_agreement': 'Non-Disclosure Agreement',
            'distribution_agreement': 'Distribution Agreement',
            'loan_agreement': 'Loan Agreement',
            'other_contract': 'Commercial Contract'
        }
        
        base_name = type_names.get(contract_type, 'Commercial Contract')
        
        if companies:
            # Use first company found
            company = list(companies)[0]
            return f"{base_name} - {company}"
        
        return f"{base_name} {index}"
    
    def generate_summary(self, text: str) -> str:
        """Generate a meaningful summary from contract text"""
        # Find first substantial paragraph
        paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 100]
        
        if paragraphs:
            # Use first meaningful paragraph as summary, truncated
            summary = paragraphs[0]
            if len(summary) > 500:
                summary = summary[:500] + "..."
            return summary
        
        # Fallback to first 500 characters
        return text[:500] + "..." if len(text) > 500 else text
    
    def assess_complexity(self, text: str) -> str:
        """Assess contract complexity based on content"""
        word_count = len(text.split())
        clause_indicators = len(re.findall(r'\b(?:shall|must|may|agrees|acknowledges|represents|warrants)\b', text, re.IGNORECASE))
        
        if word_count > 10000 or clause_indicators > 50:
            return 'High'
        elif word_count > 5000 or clause_indicators > 25:
            return 'Medium'
        else:
            return 'Low'
    
    def assess_risk(self, text: str) -> str:
        """Assess contract risk level based on content"""
        text_lower = text.lower()
        
        high_risk_terms = ['liability', 'indemnification', 'penalty', 'damages', 'termination', 'breach']
        medium_risk_terms = ['confidential', 'non-compete', 'exclusive', 'assignment']
        
        high_risk_count = sum(1 for term in high_risk_terms if term in text_lower)
        medium_risk_count = sum(1 for term in medium_risk_terms if term in text_lower)
        
        if high_risk_count >= 3:
            return 'High'
        elif high_risk_count >= 1 or medium_risk_count >= 3:
            return 'Medium'
        else:
            return 'Low'
    
    async def generate_embeddings_and_upload(self, contracts: List[Dict[str, Any]]):
        """Generate embeddings and upload to Qdrant"""
        logger.info(f"Generating embeddings for {len(contracts)} CUAD contracts...")
        
        try:
            # Initialize collection
            await self.qdrant_service.initialize_collection()
            logger.info("Collection ready for CUAD contracts")
            
            # Process in batches
            batch_size = 10
            total_uploaded = 0
            
            for i in range(0, len(contracts), batch_size):
                batch_contracts = contracts[i:i + batch_size]
                
                # Generate embeddings for this batch
                texts_to_embed = []
                for contract in batch_contracts:
                    # Combine relevant fields for better search
                    embed_text = f"{contract['case_name']} {contract['industry']} {contract['summary']} {contract['full_text'][:3000]}"
                    texts_to_embed.append(embed_text)
                
                try:
                    embeddings = await self.openai_service.get_embeddings_batch(texts_to_embed)
                    
                    # Upload to Qdrant
                    await self.qdrant_service.add_points(batch_contracts, embeddings)
                    
                    total_uploaded += len(batch_contracts)
                    logger.info(f"Uploaded batch {i//batch_size + 1}/{(len(contracts) + batch_size - 1)//batch_size}: {len(batch_contracts)} contracts (Total: {total_uploaded})")
                    
                except Exception as e:
                    logger.error(f"Error processing batch {i//batch_size + 1}: {str(e)}")
                    continue
            
            logger.info(f"Successfully uploaded {total_uploaded} CUAD contracts to vector database")
            
        except Exception as e:
            logger.error(f"Error in upload process: {str(e)}")
            raise
    
    async def run(self):
        """Main execution function"""
        try:
            # Load full CUAD dataset
            dataset = self.load_cuad_dataset()
            
            # Process to our contract format with rich metadata
            contracts = self.process_cuad_to_contracts(dataset)
            
            # Save processed data
            output_file = Path("full_cuad_processed_data.json")
            with open(output_file, 'w') as f:
                json.dump(contracts, f, indent=2)
            logger.info(f"Saved {len(contracts)} processed CUAD contracts to {output_file}")
            
            # Generate embeddings and upload
            await self.generate_embeddings_and_upload(contracts)
            
            # Print summary statistics
            self.print_dataset_summary(contracts)
            
            logger.info("Full CUAD dataset integration completed successfully!")
            
        except Exception as e:
            logger.error(f"Error in CUAD processing: {str(e)}")
            raise
    
    def print_dataset_summary(self, contracts: List[Dict[str, Any]]):
        """Print summary statistics of the processed dataset"""
        logger.info("\n" + "="*50)
        logger.info("CUAD DATASET SUMMARY")
        logger.info("="*50)
        
        # Count by industry
        industries = defaultdict(int)
        contract_types = defaultdict(int)
        jurisdictions = defaultdict(int)
        complexity_levels = defaultdict(int)
        
        for contract in contracts:
            industries[contract['industry']] += 1
            contract_types[contract['case_type']] += 1
            jurisdictions[contract['jurisdiction']] += 1
            complexity_levels[contract['complexity_level']] += 1
        
        logger.info(f"Total Contracts: {len(contracts)}")
        logger.info(f"\nIndustries:")
        for industry, count in sorted(industries.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  {industry}: {count}")
        
        logger.info(f"\nContract Types:")
        for contract_type, count in sorted(contract_types.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  {contract_type}: {count}")
        
        logger.info(f"\nJurisdictions:")
        for jurisdiction, count in sorted(jurisdictions.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  {jurisdiction}: {count}")
        
        logger.info(f"\nComplexity Levels:")
        for level, count in sorted(complexity_levels.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  {level}: {count}")
        
        logger.info("="*50)

if __name__ == "__main__":
    processor = FullCUADProcessor()
    asyncio.run(processor.run()) 