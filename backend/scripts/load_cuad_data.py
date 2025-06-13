#!/usr/bin/env python3
"""
Script to download and process CUAD (Contract Understanding Atticus Dataset)
for integration into our legal search system.
"""

import asyncio
import json
import uuid
from datasets import load_dataset
from typing import List, Dict, Any
import logging
from pathlib import Path

# Import our services
import sys
sys.path.append('..')
from app.services.qdrant_service import QdrantService
from app.services.openai_service import OpenAIService
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CUADProcessor:
    def __init__(self):
        self.qdrant_service = QdrantService()
        self.openai_service = OpenAIService()
        
    def load_cuad_dataset(self):
        """Download CUAD dataset from Hugging Face"""
        logger.info("Loading CUAD dataset from Hugging Face...")
        
        # Load the dataset
        dataset = load_dataset("theatticusproject/cuad", split="train")
        logger.info(f"Loaded {len(dataset)} contract entries")
        
        return dataset
    
    def process_cuad_to_cases(self, dataset) -> List[Dict[str, Any]]:
        """Convert CUAD dataset entries to our case format"""
        cases = []
        
        # Group by contract - CUAD has multiple entries per contract
        contracts = {}
        
        for entry in dataset:
            text = entry.get('text', '')
            if not text.strip():
                continue
                
            # Extract contract info from text
            # CUAD entries contain contract text fragments
            contract_id = f"cuad_{len(contracts)}"
            
            if contract_id not in contracts:
                contracts[contract_id] = {
                    'id': str(uuid.uuid4()),
                    'case_name': f"Commercial Contract {len(contracts) + 1}",
                    'citation': f"CUAD Contract {len(contracts) + 1}",
                    'court': "Commercial Transaction",
                    'jurisdiction': "commercial",
                    'court_level': "contract",
                    'case_type': "contract",
                    'date_filed': "2021-01-01",  # CUAD publication year
                    'summary': "Commercial contract with various legal clauses and provisions.",
                    'full_text': "",
                    'url': f"https://huggingface.co/datasets/theatricusproject/cuad",
                    'categories': [],
                    'clauses': []
                }
            
            # Add this text fragment to the contract
            contracts[contract_id]['full_text'] += f"\n\n{text.strip()}"
            contracts[contract_id]['clauses'].append(text.strip())
        
        # Convert to our case format
        for contract_id, contract_data in contracts.items():
            # Clean up full text
            contract_data['full_text'] = contract_data['full_text'].strip()
            
            # Create summary from first 500 characters
            if len(contract_data['full_text']) > 500:
                contract_data['summary'] = contract_data['full_text'][:500] + "..."
            else:
                contract_data['summary'] = contract_data['full_text']
            
            # Update case name based on content
            full_text_lower = contract_data['full_text'].lower()
            if 'employment' in full_text_lower:
                contract_data['case_name'] = f"Employment Contract {len(cases) + 1}"
            elif 'lease' in full_text_lower or 'rental' in full_text_lower:
                contract_data['case_name'] = f"Lease Agreement {len(cases) + 1}"
            elif 'license' in full_text_lower:
                contract_data['case_name'] = f"License Agreement {len(cases) + 1}"
            elif 'merger' in full_text_lower or 'acquisition' in full_text_lower:
                contract_data['case_name'] = f"M&A Agreement {len(cases) + 1}"
            elif 'service' in full_text_lower:
                contract_data['case_name'] = f"Service Agreement {len(cases) + 1}"
            
            # Remove internal processing fields
            del contract_data['categories']
            del contract_data['clauses']
            
            cases.append(contract_data)
            
            if len(cases) >= 100:  # Limit for testing
                break
        
        logger.info(f"Processed {len(cases)} contracts from CUAD dataset")
        return cases
    
    async def generate_embeddings_and_upload(self, cases: List[Dict[str, Any]]):
        """Generate embeddings and upload to Qdrant"""
        logger.info("Generating embeddings for CUAD contracts...")
        
        # Create collection for CUAD data
        cuad_collection = "cuad_contracts"
        
        try:
            # Initialize collection
            await self.qdrant_service.initialize_collection()
            logger.info(f"Collection {cuad_collection} ready")
            
            # Process in batches
            batch_size = 10
            total_uploaded = 0
            
            for i in range(0, len(cases), batch_size):
                batch_cases = cases[i:i + batch_size]
                
                # Generate embeddings for this batch
                texts_to_embed = []
                for case in batch_cases:
                    # Combine relevant fields for embedding
                    embed_text = f"{case['case_name']} {case['summary']} {case['full_text'][:2000]}"
                    texts_to_embed.append(embed_text)
                
                try:
                    embeddings = await self.openai_service.get_embeddings_batch(texts_to_embed)
                    
                    # Upload to Qdrant
                    await self.qdrant_service.add_points(batch_cases, embeddings)
                    
                    total_uploaded += len(batch_cases)
                    logger.info(f"Uploaded batch {i//batch_size + 1}: {len(batch_cases)} contracts (Total: {total_uploaded})")
                    
                except Exception as e:
                    logger.error(f"Error processing batch {i//batch_size + 1}: {str(e)}")
                    continue
            
            logger.info(f"Successfully uploaded {total_uploaded} CUAD contracts")
            
        except Exception as e:
            logger.error(f"Error in upload process: {str(e)}")
            raise
    
    async def run(self):
        """Main execution function"""
        try:
            # Load CUAD dataset
            dataset = self.load_cuad_dataset()
            
            # Process to our format
            cases = self.process_cuad_to_cases(dataset)
            
            # Save processed data
            output_file = Path("cuad_processed_data.json")
            with open(output_file, 'w') as f:
                json.dump(cases, f, indent=2)
            logger.info(f"Saved processed CUAD data to {output_file}")
            
            # Generate embeddings and upload
            await self.generate_embeddings_and_upload(cases)
            
            logger.info("CUAD dataset integration completed successfully!")
            
        except Exception as e:
            logger.error(f"Error in CUAD processing: {str(e)}")
            raise

if __name__ == "__main__":
    processor = CUADProcessor()
    asyncio.run(processor.run()) 