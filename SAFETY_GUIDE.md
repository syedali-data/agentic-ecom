# 🛡️ Agentic-Ecom Safety Guide

## ⚠️ **CRITICAL: Production API Keys in Development**

Your system is currently configured with **REAL PRODUCTION API KEYS** for Meta Ads, Pinterest Ads, and Shopify. This guide ensures safe development and testing.

## 🚨 **Immediate Safety Status**

- ✅ **Kill Switch**: ACTIVE (system paused)
- ✅ **Environment**: Development mode
- ✅ **Dry Run Mode**: ENABLED
- ✅ **Max Daily Spend**: $0.01
- ✅ **Safety Manager**: ACTIVE

## 🔒 **Safety Measures Implemented**

### 1. **Environment-Based Safety**
- **Development**: Mock APIs, $0.01 budget, dry run mode
- **Staging**: Sandbox APIs, $10 budget, approval required
- **Production**: Live APIs, $1000 budget, monitoring only

### 2. **Kill Switch System**
```bash
# Pause all operations
echo "STOP" > status.lock

# Resume operations
echo "RUN" > status.lock
```

### 3. **Budget Limits**
- **Daily Spend Tracking**: Automatic monitoring
- **Campaign Budget Limits**: Per-environment configuration
- **Automatic Pausing**: When limits exceeded

### 4. **Dry Run Mode**
- **Development**: All actions simulated
- **No Real Money Spent**: Even with production keys
- **Full Logging**: All actions logged for review

## 🧪 **Safe Testing Procedures**

### **Step 1: Verify Safety System**
```bash
python test_safety.py
```

### **Step 2: Test with Kill Switch Active**
```bash
# Keep kill switch active during development
echo "STOP" > status.lock

# Run tests (will be blocked)
python agents/sales_genie.py
```

### **Step 3: Test in Dry Run Mode**
```bash
# Remove kill switch for dry run testing
echo "RUN" > status.lock

# Run in development mode (dry run)
python agents/sales_genie.py
```

### **Step 4: Gradual Testing**
1. **Mock APIs Only**: Test without any real API calls
2. **Sandbox APIs**: Test with sandbox environments
3. **Production APIs**: Only after thorough testing

## 🔧 **Environment Configuration**

### **Development Mode (Current)**
```yaml
current_environment: "development"
features:
  dry_run: true
  budget_limits: 0.01
  require_confirmation: true
```

### **Staging Mode**
```yaml
current_environment: "staging"
features:
  dry_run: false
  budget_limits: 10.00
  require_confirmation: true
```

### **Production Mode**
```yaml
current_environment: "production"
features:
  dry_run: false
  budget_limits: 1000.00
  require_confirmation: false
```

## 📋 **Best Practices**

### **1. Always Use Kill Switch During Development**
```bash
# Before starting development
echo "STOP" > status.lock

# Only remove when ready to test
echo "RUN" > status.lock
```

### **2. Test with Mock APIs First**
- All APIs have mock mode fallback
- Mock mode is automatic when keys are missing
- Test all functionality before using real APIs

### **3. Use Low Budget Limits**
- Development: $0.01 maximum
- Staging: $10 maximum
- Production: $1000 maximum

### **4. Monitor All Actions**
- All API calls are logged
- Budget tracking is automatic
- Anomaly detection is enabled

### **5. Gradual Rollout**
1. **Development**: Mock APIs only
2. **Staging**: Sandbox APIs with low budgets
3. **Production**: Live APIs with monitoring

## 🚨 **Risk Mitigation**

### **What's Protected:**
- ✅ **Ad Spend**: Limited by environment budgets
- ✅ **Product Creation**: Blocked in development mode
- ✅ **Campaign Launch**: Requires approval in staging
- ✅ **API Rate Limits**: Automatic throttling
- ✅ **Data Loss**: All actions logged and reversible

### **What's NOT Protected:**
- ❌ **Manual API Calls**: Direct API usage bypasses safety
- ❌ **External Tools**: Third-party tools not integrated
- ❌ **Human Error**: Manual configuration mistakes

## 🔍 **Monitoring & Alerts**

### **Safety Status Check**
```bash
python test_safety.py
```

### **Budget Monitoring**
- Daily spend tracking
- Campaign budget limits
- Automatic pausing on anomalies

### **Log Monitoring**
- All API calls logged
- Safety events tracked
- Error conditions flagged

## 🛠️ **Emergency Procedures**

### **Immediate Stop**
```bash
# Emergency stop
echo "STOP" > status.lock

# Kill all Python processes
taskkill /F /IM python.exe
```

### **Budget Reset**
```bash
# Reset daily counters
python -c "from utils.safety_manager import safety_manager; safety_manager.daily_spend = 0"
```

### **Environment Switch**
```bash
# Switch to development mode
# Edit config/environments.yaml
current_environment: "development"
```

## 📞 **Support & Troubleshooting**

### **Common Issues:**

1. **"Kill switch is active"**
   - Solution: `echo "RUN" > status.lock`

2. **"Budget limit exceeded"**
   - Solution: Wait for daily reset or increase limit

3. **"API key not found"**
   - Solution: Check `.env` file configuration

4. **"Dry run mode enabled"**
   - Solution: Change environment to staging/production

### **Safety Verification:**
```bash
# Run safety test
python test_safety.py

# Check environment
python -c "from utils.safety_manager import safety_manager; print(safety_manager.get_safety_status())"
```

## ✅ **Safety Checklist**

Before running any operations:

- [ ] Kill switch is set appropriately
- [ ] Environment is configured correctly
- [ ] Budget limits are set
- [ ] Dry run mode is enabled (for development)
- [ ] Safety test passes
- [ ] API keys are configured
- [ ] Monitoring is active

## 🎯 **Next Steps**

1. **Keep kill switch active** during development
2. **Test with mock APIs** first
3. **Gradually increase budgets** as you test
4. **Monitor all actions** carefully
5. **Use staging environment** before production

---

**Remember**: Your production API keys are active. Always test safely! 🛡️ 