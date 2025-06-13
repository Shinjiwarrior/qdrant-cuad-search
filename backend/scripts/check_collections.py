#!/usr/bin/env python3
"""
Check what collections exist in Qdrant
"""

from qdrant_client import QdrantClient
from app.core.config import settings

def main():
    print("🔍 Checking Qdrant collections...")
    
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
    )
    
    try:
        collections = client.get_collections()
        print(f"📊 Found {len(collections.collections)} collections:")
        
        for collection in collections.collections:
            print(f"  - {collection.name}")
            
            # Get collection info
            try:
                info = client.get_collection(collection.name)
                print(f"    Points: {info.points_count}")
                print(f"    Status: {info.status}")
            except Exception as e:
                print(f"    Error getting info: {str(e)}")
        
        print(f"\n🎯 Current config is set to use: '{settings.qdrant_collection_name}'")
        
        # Check if our target collection exists
        collection_names = [col.name for col in collections.collections]
        if settings.qdrant_collection_name in collection_names:
            print("✅ Target collection exists!")
        else:
            print("❌ Target collection does not exist!")
            print("Available collections:", collection_names)
            
    except Exception as e:
        print(f"❌ Error connecting to Qdrant: {str(e)}")

if __name__ == "__main__":
    main() 