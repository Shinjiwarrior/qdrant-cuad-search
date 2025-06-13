#!/usr/bin/env python3
"""
Quick setup script to create a clean CUAD commercial contracts collection.
"""

import asyncio
from create_cuad_collection import CUADCollectionBuilder

async def main():
    print("🚀 Setting up clean CUAD Commercial Contracts collection...")
    print("=" * 60)
    
    # Create collection with default settings
    builder = CUADCollectionBuilder("commercial_contracts")
    await builder.run(max_contracts=200)
    
    print("\n🎉 Setup complete!")
    print("Your system now has:")
    print("  📄 200 real commercial contracts from CUAD")
    print("  🏢 Employment, License, M&A, Service agreements")
    print("  🔍 Ready for business contract searches")
    print("  ✨ No Supreme Court cases or generated data")

if __name__ == "__main__":
    asyncio.run(main()) 