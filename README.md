# Simple Vendor Risk Assessment MCP Server

🎯 **Simplest possible vendor risk assessment using AWS Titan and MCP**

Following krishnaik06 MCP-CRASH-Course pattern with function-only implementation.

## 🚀 Quick Start

### Google Colab (Easiest)
1. Open `Vendor_Risk_Assessment_MCP.ipynb` in Google Colab
2. Add your AWS credentials
3. Run all cells

### Local Setup
```bash
# Extract and setup
unzip simple_vendor_risk_mcp.zip
cd vendor-risk-mcp
python setup.py

# Configure AWS
cp .env.example .env
# Edit .env with your AWS credentials

# Test
python test_client.py

# Run MCP server
python main.py
```

## 🔧 MCP Tools

| Tool | Description |
|------|-------------|
| `assess_vendor_risk(vendor_name)` | Single vendor risk assessment |
| `compare_vendors(vendor_list)` | Compare multiple vendors |
| `get_industry_risk_benchmark(industry)` | Industry risk insights |
| `health_check()` | System status check |

## ⚙️ Claude Desktop Config

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vendor-risk": {
      "command": "python",
      "args": ["/path/to/main.py"],
      "env": {
        "AWS_ACCESS_KEY_ID": "your_key",
        "AWS_SECRET_ACCESS_KEY": "your_secret"
      }
    }
  }
}
```

## 💡 Example Usage

**Single Assessment:**
```
"Assess the risk of using Salesforce"
→ assess_vendor_risk("Salesforce")
```

**Comparison:**
```  
"Compare Microsoft vs Google vs Amazon"
→ compare_vendors("Microsoft, Google, Amazon")
```

**Industry Benchmark:**
```
"What are typical risks in Healthcare?"
→ get_industry_risk_benchmark("Healthcare")
```

## 📊 How It Works

1. **Mock Data Generation**: Creates realistic vendor profiles
2. **AWS Titan Analysis**: AI-powered risk insights  
3. **Risk Scoring**: 1-10 scale (lower = better)
4. **Comprehensive Reports**: Executive summaries with recommendations

## 🛠️ Architecture

- **Function-only implementation** (no classes)
- **FastMCP server** for MCP protocol
- **AWS Bedrock Titan** for AI analysis
- **Realistic mock data** for demonstrations
- **Google Colab compatible**

## 🔒 Requirements

- Python 3.9+
- AWS account with Bedrock access
- AWS credentials configured

## 📱 Files Included

- `main.py` - Main MCP server
- `test_client.py` - Simple testing
- `setup.py` - Easy installation
- `Vendor_Risk_Assessment_MCP.ipynb` - Google Colab notebook
- Configuration and documentation files

Built following **krishnaik06 MCP-CRASH-Course** patterns! 🚀
