#!/usr/bin/env python3
"""
Create a new clean collection with only CUAD commercial contracts.
This removes all Supreme Court cases and generated data.
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

class CUADCollectionBuilder:
    def __init__(self, collection_name: str = "commercial_contracts"):
        self.qdrant_service = QdrantService()
        self.openai_service = OpenAIService()
        self.collection_name = collection_name
        
        # Override the collection name in qdrant service
        self.qdrant_service.collection_name = collection_name
        
    def load_cuad_dataset(self):
        """Download CUAD dataset from Hugging Face"""
        logger.info("Loading CUAD dataset from Hugging Face...")
        dataset = load_dataset("theatticusproject/cuad", split="train")
        logger.info(f"Loaded {len(dataset)} contract text entries")
        return dataset
    
    def process_cuad_to_contracts(self, dataset, max_contracts: int = 200) -> List[Dict[str, Any]]:
        """Convert CUAD dataset entries to commercial contract format"""
        contracts = []
        contract_texts = {}
        
        logger.info(f"Processing CUAD dataset into contracts (max: {max_contracts})...")
        
        # Group text entries - CUAD contains individual text passages
        for i, entry in enumerate(dataset):
            # Extract text from dictionary entry
            text = entry.get('text', '') if isinstance(entry, dict) else str(entry)
            if text and text.strip() and len(text) > 50:  # Skip short/empty texts
                # Use every 200th entry to create diverse contracts  
                if i % 200 == 0 and len(contracts) < max_contracts:
                    contract_id = f"contract_{len(contracts) + 1:03d}"
                    
                    # Determine contract type from content
                    text_lower = text.lower()
                    if 'employment' in text_lower or 'employee' in text_lower:
                        contract_type = "Employment Agreement"
                    elif 'license' in text_lower or 'licensing' in text_lower:
                        contract_type = "License Agreement"
                    elif 'merger' in text_lower or 'acquisition' in text_lower:
                        contract_type = "M&A Agreement"
                    elif 'service' in text_lower or 'consulting' in text_lower:
                        contract_type = "Service Agreement"
                    elif 'lease' in text_lower or 'rental' in text_lower:
                        contract_type = "Lease Agreement"
                    elif 'confidential' in text_lower or 'nda' in text_lower:
                        contract_type = "Non-Disclosure Agreement"
                    elif 'supply' in text_lower or 'vendor' in text_lower:
                        contract_type = "Supply Agreement"
                    elif 'partnership' in text_lower or 'joint venture' in text_lower:
                        contract_type = "Partnership Agreement"
                    else:
                        contract_type = "Commercial Contract"
                    
                    # Create contract entry
                    contract = {
                        'id': str(uuid.uuid4()),
                        'case_name': f"{contract_type} {len(contracts) + 1}",
                        'citation': f"CUAD-{len(contracts) + 1:03d}",
                        'court': "Commercial Transaction",
                        'jurisdiction': "commercial",
                        'court_level': "contract",
                        'case_type': "contract",
                        'date_filed': "2021-01-01",
                        'summary': text[:500] + "..." if len(text) > 500 else text,
                        'full_text': text,
                        'url': "https://huggingface.co/datasets/theatticusproject/cuad",
                    }
                    
                    contracts.append(contract)
        
        logger.info(f"Created {len(contracts)} commercial contracts from CUAD dataset")
        return contracts
    
    async def create_new_collection(self):
        """Create a fresh collection for commercial contracts"""
        try:
            # Check if collection exists and delete it
            collections = self.qdrant_service.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            if self.collection_name in collection_names:
                logger.info(f"Deleting existing collection: {self.collection_name}")
                self.qdrant_service.client.delete_collection(self.collection_name)
            
            # Create new collection
            logger.info(f"Creating new collection: {self.collection_name}")
            await self.qdrant_service.initialize_collection()
            
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            raise
    
    async def upload_contracts(self, contracts: List[Dict[str, Any]]):
        """Generate embeddings and upload contracts to new collection"""
        logger.info(f"Uploading {len(contracts)} contracts to collection '{self.collection_name}'...")
        
        try:
            batch_size = 10
            total_uploaded = 0
            
            for i in range(0, len(contracts), batch_size):
                batch_contracts = contracts[i:i + batch_size]
                
                # Generate embeddings for this batch
                texts_to_embed = []
                for contract in batch_contracts:
                    # Combine relevant fields for embedding
                    embed_text = f"{contract['case_name']} {contract['summary']} {contract['full_text'][:1500]}"
                    texts_to_embed.append(embed_text)
                
                try:
                    embeddings = await self.openai_service.get_embeddings_batch(texts_to_embed)
                    await self.qdrant_service.add_points(batch_contracts, embeddings)
                    
                    total_uploaded += len(batch_contracts)
                    logger.info(f"Uploaded batch {i//batch_size + 1}: {len(batch_contracts)} contracts (Total: {total_uploaded})")
                    
                except Exception as e:
                    logger.error(f"Error processing batch {i//batch_size + 1}: {str(e)}")
                    continue
            
            logger.info(f"Successfully uploaded {total_uploaded} commercial contracts!")
            
        except Exception as e:
            logger.error(f"Error in upload process: {str(e)}")
            raise
    
    async def run(self, max_contracts: int = 200):
        """Main execution function"""
        try:
            logger.info(f"🏗️  Building new commercial contracts collection: '{self.collection_name}'")
            
            # Load CUAD dataset
            dataset = self.load_cuad_dataset()
            
            # Process to commercial contracts
            contracts = self.process_cuad_to_contracts(dataset, max_contracts)
            
            # Save processed data
            output_file = Path(f"{self.collection_name}_data.json")
            with open(output_file, 'w') as f:
                json.dump(contracts, f, indent=2)
            logger.info(f"Saved processed data to {output_file}")
            
            # Create new collection
            await self.create_new_collection()
            
            # Upload contracts
            await self.upload_contracts(contracts)
            
            logger.info("🎉 Commercial contracts collection created successfully!")
            logger.info(f"📊 Collection: {self.collection_name}")
            logger.info(f"📄 Total contracts: {len(contracts)}")
            logger.info(f"🔍 Ready for business contract searches!")
            
        except Exception as e:
            logger.error(f"Error building collection: {str(e)}")
            raise

async def main():
    """Main function with user input"""
    print("🏢 Creating new CUAD Commercial Contracts Collection")
    print("-" * 50)
    
    collection_name = input("Enter collection name [commercial_contracts]: ").strip()
    if not collection_name:
        collection_name = "commercial_contracts"
    
    max_contracts_input = input("Number of contracts to process [200]: ").strip()
    try:
        max_contracts = int(max_contracts_input) if max_contracts_input else 200
    except ValueError:
        max_contracts = 200
    
    print(f"Creating collection '{collection_name}' with {max_contracts} contracts...")
    
    builder = CUADCollectionBuilder(collection_name)
    await builder.run(max_contracts)

if __name__ == "__main__":
    asyncio.run(main()) 