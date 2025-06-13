#!/usr/bin/env python3
"""
Non-interactive script to migrate to the full CUAD dataset.
Run this from the backend/scripts directory.
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from load_full_cuad_data import FullCUADProcessor

async def main():
    print("🚀 Starting Full CUAD Dataset Migration (Auto Mode)")
    print("=" * 50)
    print("This will:")
    print("• Download the complete CUAD dataset (510 contracts)")
    print("• Process with rich metadata extraction")
    print("• Generate embeddings for all contracts")
    print("• Upload to vector database")
    print("=" * 50)
    
    try:
        processor = FullCUADProcessor()
        await processor.run()
        
        print("\n✅ SUCCESS!")
        print("Your application now has access to:")
        print("• 510 real commercial contracts")
        print("• Rich industry and metadata filtering")
        print("• Professional-grade legal content")
        print("• Enhanced search capabilities")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Check the logs for more details.")

if __name__ == "__main__":
    asyncio.run(main()) 