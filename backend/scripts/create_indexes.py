#!/usr/bin/env python3
"""
Script to create filter indexes for the commercial contracts collection.
"""

import asyncio
from app.services.qdrant_service import QdrantService

async def main():
    print("🔧 Adding filter indexes to commercial contracts collection...")
    
    qdrant_service = QdrantService()
    
    try:
        await qdrant_service._create_filter_indexes()
        print("✅ Successfully created filter indexes!")
        print("🔍 Filtering is now enabled for:")
        print("  - jurisdiction")
        print("  - court_level")  
        print("  - case_type")
        print("  - date_filed")
        
    except Exception as e:
        print(f"❌ Error creating indexes: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 