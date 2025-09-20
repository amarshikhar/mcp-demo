# 🚀 QUICK START

## 1. Setup
```bash
cd vendor-risk-mcp
python setup.py
```

## 2. Configure
```bash
cp .env.example .env
# Edit .env with AWS credentials
```

## 3. Test
```bash
python test_client.py
```

## 4. Run
```bash
python main.py
```

## 5. Claude Desktop
Add to claude_desktop_config.json:
```json
{
  "mcpServers": {
    "vendor-risk": {
      "command": "python",
      "args": ["/absolute/path/to/main.py"],
      "env": {
        "AWS_ACCESS_KEY_ID": "your_key",
        "AWS_SECRET_ACCESS_KEY": "your_secret"
      }
    }
  }
}
```

That's it! ✅
