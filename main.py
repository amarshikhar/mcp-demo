"""
Simple Vendor Risk Assessment MCP Server
Based on krishnaik06 MCP-CRASH-Course pattern
Uses AWS Titan for AI-powered risk analysis
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
import os
import boto3
import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging for Google Colab compatibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("vendor-risk-assessment")

# AWS Configuration
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
BEDROCK_MODEL_ID = os.getenv('BEDROCK_MODEL_ID', 'amazon.titan-text-express-v1')

def get_bedrock_client():
    """Get AWS Bedrock client"""
    try:
        return boto3.client(
            'bedrock-runtime',
            region_name=AWS_REGION,
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
    except Exception as e:
        logger.error(f"Failed to create Bedrock client: {e}")
        return None

async def call_titan_model(prompt: str, max_tokens: int = 1000) -> str:
    """Call AWS Titan model for AI analysis"""
    try:
        bedrock_client = get_bedrock_client()
        if not bedrock_client:
            return "Error: Could not connect to AWS Bedrock. Please check credentials."

        body = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": max_tokens,
                "temperature": 0.1,
                "topP": 0.9,
                "stopSequences": []
            }
        }

        response = bedrock_client.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )

        response_body = json.loads(response['body'].read())
        return response_body.get('results', [{}])[0].get('outputText', 'No response generated')

    except Exception as e:
        logger.error(f"Titan API call failed: {e}")
        return f"Error calling Titan model: {str(e)}"

def get_mock_company_data(company_name: str) -> Dict[str, Any]:
    """Generate realistic mock company data for demo"""
    import random

    industries = {
        "microsoft": "Technology", "google": "Technology", "amazon": "Technology",
        "apple": "Technology", "meta": "Technology", "salesforce": "Technology",
        "jpmorgan": "Financial Services", "goldman": "Financial Services", 
        "mastercard": "Financial Services", "visa": "Financial Services",
        "johnson": "Healthcare", "pfizer": "Healthcare", "merck": "Healthcare"
    }

    company_lower = company_name.lower()
    industry = next((v for k, v in industries.items() if k in company_lower), "General Services")

    # Generate realistic data based on company type
    if industry == "Technology":
        base_score = random.uniform(2.5, 4.5)
        financial_health = random.choice(["Excellent", "Good", "Good"])
        security_rating = random.choice(["A", "A-", "B+"])
        reputation = random.uniform(7.5, 9.2)
    elif industry == "Financial Services":
        base_score = random.uniform(3.0, 5.0)
        financial_health = random.choice(["Excellent", "Good"])
        security_rating = random.choice(["A+", "A", "A-"])
        reputation = random.uniform(7.0, 8.5)
    else:
        base_score = random.uniform(3.5, 6.0)
        financial_health = random.choice(["Good", "Fair", "Good"])
        security_rating = random.choice(["B+", "B", "A-"])
        reputation = random.uniform(6.5, 8.0)

    return {
        "name": company_name,
        "industry": industry,
        "founded": random.randint(1980, 2015),
        "size": random.choice(["Large (1000+)", "Medium (201-1000)", "Large (1000+)"]),
        "location": random.choice(["United States", "Europe", "Global"]),
        "financial_health": financial_health,
        "reputation_score": round(reputation, 1),
        "security_rating": security_rating,
        "compliance_status": random.sample(
            ["ISO 27001", "SOC 2", "GDPR", "HIPAA", "PCI DSS", "ISO 9001"], 
            random.randint(3, 5)
        ),
        "base_risk_score": round(base_score, 1)
    }

@mcp.tool()
async def assess_vendor_risk(vendor_name: str) -> str:
    """Assess comprehensive risk for a vendor using AI analysis.

    Args:
        vendor_name: Name of the vendor company to assess
    """
    try:
        logger.info(f"Starting risk assessment for vendor: {vendor_name}")

        # Get company data
        company_data = get_mock_company_data(vendor_name)

        # Create AI prompt for analysis
        ai_prompt = f"""
        Analyze the following vendor for comprehensive risk assessment:

        Company: {company_data['name']}
        Industry: {company_data['industry']}
        Size: {company_data['size']}
        Financial Health: {company_data['financial_health']}
        Security Rating: {company_data['security_rating']}
        Reputation Score: {company_data['reputation_score']}/10
        Compliance: {', '.join(company_data['compliance_status'])}

        Provide a detailed risk assessment including:
        1. Executive Summary (2-3 sentences)
        2. Key Risk Factors (top 3 risks)
        3. Risk Mitigation Recommendations (3-4 specific actions)
        4. Overall Risk Level (Low/Medium/High)

        Format as actionable business recommendations.
        """

        # Get AI analysis
        ai_analysis = await call_titan_model(ai_prompt, max_tokens=800)

        # Format final result
        result = f"""
VENDOR RISK ASSESSMENT: {vendor_name.upper()}

=== COMPANY OVERVIEW ===
Industry: {company_data['industry']}
Size: {company_data['size']}
Location: {company_data['location']}
Founded: {company_data['founded']}

=== RISK METRICS ===
Financial Health: {company_data['financial_health']}
Security Rating: {company_data['security_rating']}
Reputation Score: {company_data['reputation_score']}/10
Compliance: {', '.join(company_data['compliance_status'])}

=== AI RISK ANALYSIS ===
{ai_analysis}

=== ASSESSMENT INFO ===
Assessment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Analysis Model: AWS Titan
        """

        return result.strip()

    except Exception as e:
        logger.error(f"Risk assessment failed: {e}")
        return f"Error: Risk assessment failed - {str(e)}"

@mcp.tool()
async def compare_vendors(vendor_list: str) -> str:
    """Compare multiple vendors and rank them by risk level.

    Args:
        vendor_list: Comma-separated list of vendor names
    """
    try:
        vendors = [v.strip() for v in vendor_list.split(',') if v.strip()]

        if len(vendors) < 2:
            return "Error: Please provide at least 2 vendors to compare"

        if len(vendors) > 5:
            return "Error: Maximum 5 vendors allowed"

        logger.info(f"Comparing {len(vendors)} vendors")

        # Assess each vendor
        vendor_data = []
        for vendor in vendors:
            data = get_mock_company_data(vendor)
            vendor_data.append({
                "name": vendor,
                "industry": data["industry"],
                "risk_score": data["base_risk_score"],
                "financial_health": data["financial_health"],
                "security_rating": data["security_rating"],
                "reputation": data["reputation_score"]
            })

        # Sort by risk score (lower is better)
        vendor_data.sort(key=lambda x: x["risk_score"])

        # Create comparison prompt
        comparison_prompt = f"""
        Compare these {len(vendor_data)} vendors for risk assessment:

        {json.dumps(vendor_data, indent=2)}

        Provide:
        1. Ranking explanation with key differentiators
        2. Recommended vendor selection strategy
        3. Risk considerations for each vendor
        4. Implementation recommendations

        Format as executive summary for decision making.
        """

        ai_comparison = await call_titan_model(comparison_prompt, max_tokens=1000)

        # Format results
        result = f"""
VENDOR RISK COMPARISON

=== RANKING (Best to Worst Risk) ===
"""

        for i, vendor in enumerate(vendor_data, 1):
            risk_level = "Low" if vendor["risk_score"] <= 3 else "Medium" if vendor["risk_score"] <= 5 else "High"
            result += f"{i}. {vendor['name']} - Score: {vendor['risk_score']}/10 ({risk_level})\n"
            result += f"   Industry: {vendor['industry']}, Security: {vendor['security_rating']}\n"

        result += f"""
=== AI COMPARISON ANALYSIS ===
{ai_comparison}

=== COMPARISON INFO ===
Vendors Analyzed: {len(vendor_data)}
Assessment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """

        return result.strip()

    except Exception as e:
        logger.error(f"Vendor comparison failed: {e}")
        return f"Error: Vendor comparison failed - {str(e)}"

@mcp.tool()
async def get_industry_risk_benchmark(industry: str) -> str:
    """Get risk benchmarks for a specific industry.

    Args:
        industry: Industry name (Technology, Healthcare, Financial Services, etc.)
    """
    try:
        logger.info(f"Getting industry benchmark for: {industry}")

        # Industry benchmarks
        benchmarks = {
            "technology": {
                "avg_risk": 3.8, "volatility": "High",
                "key_risks": ["Data breaches", "IP theft", "Rapid tech changes", "Regulatory shifts"],
                "compliance": ["SOC 2", "ISO 27001", "GDPR"]
            },
            "financial services": {
                "avg_risk": 3.2, "volatility": "Medium", 
                "key_risks": ["Regulatory violations", "Cyber attacks", "Market volatility"],
                "compliance": ["SOX", "PCI DSS", "Basel III"]
            },
            "healthcare": {
                "avg_risk": 3.5, "volatility": "Medium",
                "key_risks": ["HIPAA violations", "Patient data breaches", "Compliance failures"],
                "compliance": ["HIPAA", "FDA", "SOC 2"]
            }
        }

        industry_key = industry.lower().replace(' ', '').replace('-', '')
        if 'tech' in industry_key or 'software' in industry_key:
            industry_key = 'technology'
        elif 'financial' in industry_key or 'bank' in industry_key:
            industry_key = 'financial services'
        elif 'health' in industry_key or 'medical' in industry_key:
            industry_key = 'healthcare'

        benchmark = benchmarks.get(industry_key, {
            "avg_risk": 4.0, "volatility": "Medium",
            "key_risks": ["Operational risks", "Compliance issues", "Market changes"],
            "compliance": ["ISO 9001", "SOC 2"]
        })

        # AI analysis prompt
        analysis_prompt = f"""
        Provide industry risk insights for {industry}:

        Industry Metrics:
        - Average Risk Score: {benchmark['avg_risk']}/10
        - Market Volatility: {benchmark['volatility']}
        - Key Risks: {', '.join(benchmark['key_risks'])}
        - Common Compliance: {', '.join(benchmark['compliance'])}

        Provide:
        1. Industry risk landscape overview
        2. Current market trends affecting risk
        3. Vendor selection best practices for this industry
        4. Red flags to watch for
        5. Due diligence recommendations

        Format for procurement and risk management teams.
        """

        ai_analysis = await call_titan_model(analysis_prompt, max_tokens=1000)

        result = f"""
INDUSTRY RISK BENCHMARK: {industry.upper()}

=== BENCHMARK METRICS ===
Average Industry Risk Score: {benchmark['avg_risk']}/10
Market Volatility: {benchmark['volatility']}

=== KEY RISK AREAS ===
{chr(10).join(f'• {risk}' for risk in benchmark['key_risks'])}

=== COMPLIANCE REQUIREMENTS ===
{chr(10).join(f'• {comp}' for comp in benchmark['compliance'])}

=== AI INDUSTRY ANALYSIS ===
{ai_analysis}

=== BENCHMARK INFO ===
Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Industry Category: {industry}
        """

        return result.strip()

    except Exception as e:
        logger.error(f"Industry benchmark failed: {e}")
        return f"Error: Industry benchmark failed - {str(e)}"

@mcp.tool()
async def health_check() -> str:
    """Check system health and configuration."""
    try:
        aws_configured = bool(os.getenv('AWS_ACCESS_KEY_ID'))

        # Test Bedrock if configured
        bedrock_status = "Not configured"
        if aws_configured:
            try:
                test_response = await call_titan_model("Test", max_tokens=10)
                bedrock_status = "Connected" if "Error" not in test_response else "Error"
            except:
                bedrock_status = "Connection failed"

        result = f"""
VENDOR RISK ASSESSMENT - SYSTEM HEALTH

=== STATUS ===
Server: Running ✅
AWS Configured: {aws_configured}
Bedrock Status: {bedrock_status}
Model: {BEDROCK_MODEL_ID}
Region: {AWS_REGION}

=== AVAILABLE TOOLS ===
• assess_vendor_risk(vendor_name)
• compare_vendors(vendor_list)
• get_industry_risk_benchmark(industry)  
• health_check()

=== HEALTH CHECK ===
Timestamp: {datetime.now().isoformat()}
Status: {"Healthy" if aws_configured else "Configuration needed"}
        """

        return result.strip()

    except Exception as e:
        return f"Health Check Error: {str(e)}"

if __name__ == "__main__":
    logger.info("Starting Vendor Risk Assessment MCP Server...")
    logger.info(f"AWS Region: {AWS_REGION}")
    logger.info(f"Bedrock Model: {BEDROCK_MODEL_ID}")

    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("Server stopped")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise
