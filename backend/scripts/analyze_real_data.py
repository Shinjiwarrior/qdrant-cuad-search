#!/usr/bin/env python3
"""
Analyze the actual data in the commercial_contracts collection to ensure
filter options match reality.
"""

from qdrant_client import QdrantClient
from app.core.config import settings
from collections import defaultdict

def main():
    print("🔍 Analyzing actual data in commercial_contracts collection...")
    
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
    )
    
    collection_name = "commercial_contracts"
    
    try:
        # Get all points to analyze
        scroll_result = client.scroll(
            collection_name=collection_name,
            limit=200,  # Get all points
            with_payload=True
        )
        
        points = scroll_result[0]
        print(f"📊 Found {len(points)} total contracts")
        
        # Analyze filter field values
        jurisdictions = set()
        court_levels = set()
        case_types = set()
        case_names = []
        
        for point in points:
            payload = point.payload
            
            if payload.get('jurisdiction'):
                jurisdictions.add(payload['jurisdiction'])
            if payload.get('court_level'):
                court_levels.add(payload['court_level'])
            if payload.get('case_type'):
                case_types.add(payload['case_type'])
            if payload.get('case_name'):
                case_names.append(payload['case_name'])
        
        print("\n🎯 ACTUAL DATA ANALYSIS:")
        print("=" * 50)
        
        print(f"📍 Jurisdictions found ({len(jurisdictions)}):")
        for j in sorted(jurisdictions):
            print(f"  - {j}")
        
        print(f"\n🏛️  Court levels found ({len(court_levels)}):")
        for c in sorted(court_levels):
            print(f"  - {c}")
        
        print(f"\n📋 Case types found ({len(case_types)}):")
        for ct in sorted(case_types):
            print(f"  - {ct}")
        
        print(f"\n📄 Sample case names:")
        for name in case_names[:10]:
            print(f"  - {name}")
        
        # Compare with current filter options
        print("\n🔍 COMPARISON WITH CURRENT FILTER OPTIONS:")
        print("=" * 50)
        
        current_jurisdictions = ["california", "commercial", "delaware", "federal", "new_york", "texas"]
        current_court_levels = ["commercial_transaction", "contract", "federal_district", "state_court"]
        current_case_types = ["commercial_contract", "contract", "employment_agreement", "lease_agreement", "license_agreement", "merger_agreement", "nda", "partnership_agreement", "service_agreement", "supply_agreement"]
        
        print("📍 Jurisdictions:")
        print(f"  Current options: {current_jurisdictions}")
        print(f"  Actual data: {sorted(list(jurisdictions))}")
        missing_j = jurisdictions - set(current_jurisdictions)
        extra_j = set(current_jurisdictions) - jurisdictions
        if missing_j: print(f"  ❌ Missing: {list(missing_j)}")
        if extra_j: print(f"  ⚠️  Extra: {list(extra_j)}")
        
        print("\n🏛️  Court levels:")
        print(f"  Current options: {current_court_levels}")
        print(f"  Actual data: {sorted(list(court_levels))}")
        missing_c = court_levels - set(current_court_levels)
        extra_c = set(current_court_levels) - court_levels
        if missing_c: print(f"  ❌ Missing: {list(missing_c)}")
        if extra_c: print(f"  ⚠️  Extra: {list(extra_c)}")
        
        print("\n📋 Case types:")
        print(f"  Current options: {current_case_types}")
        print(f"  Actual data: {sorted(list(case_types))}")
        missing_ct = case_types - set(current_case_types)
        extra_ct = set(current_case_types) - case_types
        if missing_ct: print(f"  ❌ Missing: {list(missing_ct)}")
        if extra_ct: print(f"  ⚠️  Extra: {list(extra_ct)}")
        
    except Exception as e:
        print(f"❌ Error analyzing data: {str(e)}")

if __name__ == "__main__":
    main() 