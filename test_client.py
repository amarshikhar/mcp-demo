"""
Simple test client for Vendor Risk Assessment MCP Server
"""
import asyncio
import sys
import os

# Add current directory to path
sys.path.append('.')

async def test_functions():
    """Test all functions"""
    print("🧪 TESTING VENDOR RISK ASSESSMENT")
    print("=" * 50)

    # Set environment if not already set
    os.environ.setdefault('AWS_ACCESS_KEY_ID', 'enter')
    os.environ.setdefault('AWS_SECRET_ACCESS_KEY', 'enter')
    os.environ.setdefault('AWS_REGION', 'us-east-1')

    try:
        from main import assess_vendor_risk, compare_vendors, get_industry_risk_benchmark, health_check

        print("1️⃣ Health Check")
        print(await health_check())
        print("\n" + "="*50)

        print("2️⃣ Vendor Assessment")
        print(await assess_vendor_risk("Microsoft"))
        print("\n" + "="*50)

        print("3️⃣ Vendor Comparison")  
        print(await compare_vendors("Google, Amazon"))
        print("\n" + "="*50)

        print("4️⃣ Industry Benchmark")
        print(await get_industry_risk_benchmark("Technology"))

        print("\n✅ ALL TESTS COMPLETED!")

    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_functions())
