# Agentic-Ecom: Dual-Agent AI E-Commerce Automation System

This project automates the entire dropshipping business lifecycle for the Canadian (and global) market using three specialized AI agents:

- **SalesGenie (GPT-4o)**: Handles product research, listing generation, ad creative, campaign launch, and optimization
- **LogiBot (Claude Sonnet 4)**: Manages fulfillment, customer tracking, returns, customer support, and fraud detection
- **BuyBot (GPT-4o)**: Customer-facing product Q&A and recommendations

## 🚀 Key Features

- **AI-Powered Product Research**: Automated product discovery and trend analysis
- **Intelligent Listing Generation**: GPT-4o creates compelling, SEO-optimized product descriptions
- **Multi-Platform Ad Automation**: Meta (Facebook/Instagram) & Pinterest ad creation and optimization
- **Smart Customer Support**: Claude Sonnet 4 handles customer queries with contextual understanding
- **Fraud Detection & Prevention**: AI-powered order analysis and risk assessment
- **Real-time Analytics Dashboard**: Human-in-the-loop oversight and control
- **Event-Driven Architecture**: Cross-agent communication and task handoffs
- **Comprehensive Logging**: Full audit trail and performance monitoring

## 🏗️ Project Structure

```
agentic-ecom/
├── agents/                      # Core AI agents
│   ├── sales_genie.py          # 🚀 GPT-4o-powered: Product research & marketing
│   ├── logibot.py              # 🧠 Claude Sonnet 4-powered: Operations & support
│   └── buybot.py               # 💬 GPT-4o-powered: Customer Q&A
├── api/                        # FastAPI endpoints
│   └── fastapi_api.py          # REST API for external integrations
├── schemas/                    # Pydantic data models
│   ├── product.py              # Product schemas
│   ├── audit_log.py            # Audit logging
│   ├── hitl_queue.py           # Human-in-the-loop tasks
│   └── escalation_event.py     # Escalation events
├── services/                   # Core services & integrations
│   ├── claude_client.py        # Claude API abstraction
│   ├── gpt_client.py           # GPT API abstraction
│   ├── shopify_api.py          # Shopify integration
│   ├── meta_ads_api.py         # Meta Ads integration
│   ├── pinterest_ads_api.py    # Pinterest Ads integration
│   ├── cj_api.py               # CJ Dropshipping API
│   ├── compliance.py           # Compliance checking
│   └── ad_optimizer.py         # Ad optimization logic
├── dashboard/                  # Analytics dashboard
│   └── app.py                  # Dash-based monitoring interface
├── config/                     # Configuration files
│   ├── agent_settings.yaml     # AI model configurations
│   ├── api_keys.yaml           # API credentials
│   ├── budget_limits.yaml      # Budget controls
│   └── compliance_rules.yaml   # Compliance rules
├── prompts/                    # AI prompt templates
│   ├── product_copy.txt        # Product description prompts
│   ├── ad_copy.txt             # Ad creation prompts
│   └── refund_email.txt        # Support response prompts
├── logs/                       # System logs
├── tests/                      # Test suite
├── event_bus.py                # Cross-agent communication
├── mcp_protocol.py             # Agent collaboration protocol
├── run.py                      # Main controller
└── status.lock                 # Emergency kill switch
```

## 🎯 AI Model Strategy

### **SalesGenie + GPT-4o**
- **Creative Excellence**: Superior ad copy and product descriptions
- **Market Research**: Trend analysis and competitive insights
- **Multi-modal**: Image analysis and visual content generation
- **Cost**: ~$5-15/1M input tokens, ~$15-60/1M output tokens

### **LogiBot + Claude Sonnet 4**
- **Analytical Power**: Complex reasoning for fraud detection
- **Customer Support**: Nuanced understanding of customer issues
- **Process Optimization**: Workflow analysis and improvement
- **Cost**: ~$3-15/1M input tokens, ~$15-75/1M output tokens

### **BuyBot + GPT-4o**
- **Conversational AI**: Natural customer interactions
- **Product Recommendations**: Intelligent product matching
- **Real-time Responses**: Fast, accurate customer support

## ⚡ Quick Start

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Configure Environment**
```bash
# Copy and edit .env file
cp config/api_keys.yaml .env

# Add your API keys:
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
SHOPIFY_ACCESS_TOKEN=your-shopify-token
META_ACCESS_TOKEN=your-meta-token
```

### 3. **Start the System**
```bash
# Start main controller
python run.py --start

# Start API server (optional)
python api/fastapi_api.py

# Start dashboard (optional)
python dashboard/app.py
```

### 4. **Access Dashboard**
Open http://localhost:8050 for real-time monitoring and control.

## 🔧 Configuration

### **Agent Settings** (`config/agent_settings.yaml`)
```yaml
sales_genie:
  ai_model: "gpt-4o"
  max_tokens: 1000
  temperature: 0.7

logibot:
  ai_model: "claude-3-5-sonnet-20241022"
  max_tokens: 500
  temperature: 0.5
```

### **Budget Limits** (`config/budget_limits.yaml`)
```yaml
meta_ads:
  default:
    daily_budget_usd: 200
    min_roas: 2.5

pinterest_ads:
  default:
    daily_budget_usd: 100
    min_roas: 2.0
```

## 📊 Monitoring & Control

### **Dashboard Features**
- Real-time agent status monitoring
- Task completion tracking
- Event log visualization
- Manual emergency controls
- Performance analytics

### **Emergency Controls**
- **Emergency Stop**: Creates `status.lock` file to pause all operations
- **Resume System**: Removes `status.lock` to resume operations
- **Manual Task Generation**: Test system functionality

## 🔄 Agent Communication

### **Event Bus System**
- Cross-agent event publishing and subscription
- Real-time task handoffs
- Centralized logging and monitoring

### **MCP Protocol**
- Structured task management
- Agent capability mapping
- Priority-based task routing

## 🛡️ Safety & Compliance

### **Built-in Safeguards**
- Kill switch mechanism (`status.lock`)
- Rate limiting and budget controls
- Compliance checking for all content
- Comprehensive audit logging

### **Compliance Rules**
- Banned keywords and product categories
- Regional compliance (Canada-specific)
- Automated content review

## 📈 Performance & ROI

### **Expected Costs**
- **Small Scale** (100 products/month): $50-150
- **Medium Scale** (500 products/month): $200-500
- **Large Scale** (1000+ products/month): $400-1000

### **Expected ROI**
- **SalesGenie**: 300-500% ROI (better ads = more sales)
- **LogiBot**: 200-400% ROI (reduced support costs + fraud prevention)
- **BuyBot**: 150-300% ROI (improved customer experience)

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test suites
pytest tests/agents/
pytest tests/services/
pytest tests/integration/
```

## 🚀 Deployment

### **Docker Deployment**
```bash
# Build and run with Docker
docker build -t agentic-ecom .
docker run -p 8000:8000 -p 8050:8050 agentic-ecom
```

### **Production Considerations**
- Use environment variables for all secrets
- Set up proper logging and monitoring
- Configure rate limits and budgets
- Implement backup and recovery procedures

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

Built by ADS. AI powered by OpenAI, Anthropic, Shopify, Meta, and CJ Dropshipping APIs.

## 🆘 Support

For issues and questions:
- Check the logs in `logs/` directory
- Review the dashboard for system status
- Check configuration files for proper setup
- Ensure all API keys are valid and have sufficient credits
