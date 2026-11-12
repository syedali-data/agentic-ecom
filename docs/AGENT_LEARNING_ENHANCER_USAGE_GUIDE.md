# 🧠 Agent Learning Enhancer - Usage Guide

## 🎯 **Overview**

The `AgentLearningEnhancer` is a powerful tool that accelerates your agents' intelligence improvement through data enrichment, training dataset creation, and prompt optimization.

---

## 🚀 **Quick Start**

### **Step 1: Import and Initialize**
```python
from agents.agent_learning_enhancer import AgentLearningEnhancer
from db.database import get_db

# Get database session
db = get_db()

# Initialize the enhancer
enhancer = AgentLearningEnhancer(db)
```

### **Step 2: Basic Usage**
```python
# Enrich training data for an agent
enriched_data = enhancer.enrich_agent_training_data("sales_genie")

# Create training dataset
dataset = enhancer.create_agent_training_dataset("sales_genie", days=30)

# Optimize prompts
optimized_prompts = enhancer.optimize_agent_prompts("sales_genie")
```

---

## 📊 **Detailed Usage Examples**

### **1. Enrich Agent Training Data**

#### **Basic Enrichment**
```python
# Enrich with performance data (default)
enriched_data = enhancer.enrich_agent_training_data("sales_genie")
print(f"✅ Enriched {enriched_data['agent_type']}")
print(f"📊 Data sources: {enriched_data['data_sources']}")
print(f"🔍 Insights: {len(enriched_data['insights'])}")
print(f"💡 Recommendations: {enriched_data['recommendations']}")
```

#### **Advanced Enrichment**
```python
# Enrich with specific data sources
enriched_data = enhancer.enrich_agent_training_data(
    agent_type="logibot",
    data_source="all"  # performance, decisions, interactions, all
)

# Check what data was enriched
for source in enriched_data['data_sources']:
    print(f"📈 Enriched {source} data")
```

#### **Multiple Agents**
```python
# Enrich all agent types
agents = ["sales_genie", "logibot", "buybot"]
for agent_type in agents:
    enriched_data = enhancer.enrich_agent_training_data(agent_type)
    print(f"✅ {agent_type}: {len(enriched_data['insights'])} insights")
```

### **2. Create Training Datasets**

#### **Basic Dataset Creation**
```python
# Create dataset for last 30 days
dataset = enhancer.create_agent_training_dataset("sales_genie")
print(f"📊 Dataset created: {len(dataset['training_examples'])} examples")
print(f"🎯 Optimization targets: {dataset['optimization_targets']}")
```

#### **Custom Timeframe**
```python
# Create dataset for last 90 days
dataset = enhancer.create_agent_training_dataset("sales_genie", days=90)
print(f"📈 {dataset['timeframe_days']} days of data")
print(f"📊 Performance metrics: {dataset['performance_metrics']}")
```

#### **Analyze Dataset**
```python
dataset = enhancer.create_agent_training_dataset("sales_genie")

# Check performance metrics
metrics = dataset['performance_metrics']
print(f"📊 Total views: {metrics.get('total_views', 0)}")
print(f"🎯 Engagement rate: {metrics.get('overall_engagement_rate', 0):.2%}")
print(f"💰 Conversion rate: {metrics.get('conversion_rate', 0):.2%}")

# Check optimization targets
targets = dataset['optimization_targets']
for target in targets:
    print(f"🎯 Target: {target}")
```

### **3. Optimize Agent Prompts**

#### **Basic Prompt Optimization**
```python
# Optimize for performance
optimized_prompts = enhancer.optimize_agent_prompts("sales_genie")
print(f"🎯 Optimized prompts for {optimized_prompts['agent_type']}")
print(f"📊 Optimization goal: {optimized_prompts['optimization_goal']}")
```

#### **Custom Optimization Goals**
```python
# Optimize for different goals
goals = ["performance", "accuracy", "efficiency"]
for goal in goals:
    optimized = enhancer.optimize_agent_prompts("sales_genie", goal)
    print(f"🎯 {goal.upper()}: {optimized['prompts']}")
```

---

## 🔍 **Advanced Usage**

### **1. Analyze Decision Patterns**
```python
# Get agent insights
insights = enhancer.memory_store.get_agent_insights("sales_genie")

# Analyze patterns manually
success_patterns = []
failure_patterns = []

for insight in insights:
    if insight.get("success_patterns"):
        success_patterns.extend(insight["success_patterns"])
    if insight.get("failure_patterns"):
        failure_patterns.extend(insight["failure_patterns"])

print(f"✅ Success patterns: {len(success_patterns)}")
print(f"❌ Failure patterns: {len(failure_patterns)}")
```

### **2. Performance Analysis**
```python
# Get performance data
performance = enhancer.performance_tracker.get_content_analytics(days=30)

# Analyze performance trends
high_performing = []
low_performing = []

for metric in performance:
    if metric.get("engagement_rate", 0) > 0.05:
        high_performing.append(metric.get("content_type"))
    else:
        low_performing.append(metric.get("content_type"))

print(f"🚀 High-performing content: {high_performing}")
print(f"📉 Low-performing content: {low_performing}")
```

### **3. Custom Training Examples**
```python
# Create custom training examples
dataset = enhancer.create_agent_training_dataset("sales_genie")

for example in dataset['training_examples']:
    print(f"📝 Input: {example['input'][:100]}...")
    print(f"🎯 Output: {example['output']}")
    print(f"📊 Score: {example['performance_score']}")
    print("---")
```

---

## 🎯 **Practical Use Cases**

### **Use Case 1: Weekly Agent Review**
```python
def weekly_agent_review():
    """Run weekly agent performance review and optimization."""
    enhancer = AgentLearningEnhancer(db)
    
    agents = ["sales_genie", "logibot", "buybot"]
    
    for agent_type in agents:
        print(f"\n🔍 Reviewing {agent_type}...")
        
        # Enrich training data
        enriched = enhancer.enrich_agent_training_data(agent_type)
        print(f"📊 {len(enriched['insights'])} insights found")
        
        # Create training dataset
        dataset = enhancer.create_agent_training_dataset(agent_type, days=7)
        print(f"📈 {len(dataset['training_examples'])} training examples")
        
        # Optimize prompts
        optimized = enhancer.optimize_agent_prompts(agent_type)
        print(f"🎯 Prompts optimized for {optimized['optimization_goal']}")
        
        # Print recommendations
        for rec in enriched['recommendations']:
            print(f"💡 Recommendation: {rec}")

# Run weekly review
weekly_agent_review()
```

### **Use Case 2: Performance Monitoring**
```python
def monitor_agent_performance():
    """Monitor agent performance and identify issues."""
    enhancer = AgentLearningEnhancer(db)
    
    for agent_type in ["sales_genie", "logibot", "buybot"]:
        dataset = enhancer.create_agent_training_dataset(agent_type, days=30)
        metrics = dataset['performance_metrics']
        
        print(f"\n📊 {agent_type.upper()} Performance:")
        print(f"   Views: {metrics.get('total_views', 0):,}")
        print(f"   Engagement: {metrics.get('overall_engagement_rate', 0):.2%}")
        print(f"   Conversion: {metrics.get('conversion_rate', 0):.2%}")
        
        # Check for issues
        if metrics.get('overall_engagement_rate', 0) < 0.05:
            print(f"   ⚠️  Low engagement detected")
        
        if metrics.get('conversion_rate', 0) < 0.02:
            print(f"   ⚠️  Low conversion rate detected")

# Run performance monitoring
monitor_agent_performance()
```

### **Use Case 3: Automated Optimization**
```python
def auto_optimize_agents():
    """Automatically optimize agents based on performance."""
    enhancer = AgentLearningEnhancer(db)
    
    for agent_type in ["sales_genie", "logibot", "buybot"]:
        print(f"\n🤖 Optimizing {agent_type}...")
        
        # Get current performance
        dataset = enhancer.create_agent_training_dataset(agent_type, days=7)
        targets = dataset['optimization_targets']
        
        if targets:
            print(f"🎯 Optimization targets: {targets}")
            
            # Optimize prompts based on targets
            optimized = enhancer.optimize_agent_prompts(agent_type, "performance")
            print(f"✅ Prompts optimized")
        else:
            print(f"✅ No optimization needed")

# Run automated optimization
auto_optimize_agents()
```

---

## 📈 **Monitoring and Analytics**

### **1. Track Learning Progress**
```python
def track_learning_progress():
    """Track how agents are learning over time."""
    enhancer = AgentLearningEnhancer(db)
    
    # Compare weekly progress
    for week in range(1, 5):
        days = week * 7
        dataset = enhancer.create_agent_training_dataset("sales_genie", days=days)
        
        print(f"Week {week}:")
        print(f"  Training examples: {len(dataset['training_examples'])}")
        print(f"  Engagement rate: {dataset['performance_metrics'].get('overall_engagement_rate', 0):.2%}")
        print(f"  Optimization targets: {len(dataset['optimization_targets'])}")

# Track progress
track_learning_progress()
```

### **2. Generate Learning Reports**
```python
def generate_learning_report():
    """Generate comprehensive learning report."""
    enhancer = AgentLearningEnhancer(db)
    
    report = {
        "generated_at": datetime.now().isoformat(),
        "agents": {}
    }
    
    for agent_type in ["sales_genie", "logibot", "buybot"]:
        # Enrich data
        enriched = enhancer.enrich_agent_training_data(agent_type)
        
        # Create dataset
        dataset = enhancer.create_agent_training_dataset(agent_type)
        
        # Optimize prompts
        optimized = enhancer.optimize_agent_prompts(agent_type)
        
        report["agents"][agent_type] = {
            "insights_count": len(enriched['insights']),
            "training_examples": len(dataset['training_examples']),
            "performance_metrics": dataset['performance_metrics'],
            "optimization_targets": dataset['optimization_targets'],
            "recommendations": enriched['recommendations']
        }
    
    return report

# Generate report
report = generate_learning_report()
print(json.dumps(report, indent=2))
```

---

## 🎯 **Best Practices**

### **1. Regular Usage**
- **Weekly**: Run `enrich_agent_training_data()` for all agents
- **Monthly**: Create comprehensive training datasets
- **Quarterly**: Review and optimize prompts

### **2. Data Quality**
- Ensure agents are storing decisions properly
- Monitor performance tracking accuracy
- Validate training data quality

### **3. Optimization Strategy**
- Focus on high-impact optimization targets
- Test optimized prompts before deployment
- Monitor results after optimization

### **4. Performance Monitoring**
- Set up automated performance alerts
- Track learning progress over time
- Document successful optimization strategies

---

## 🚀 **Integration Examples**

### **Integration with Dashboard**
```python
# Add to your dashboard
def get_agent_learning_dashboard():
    enhancer = AgentLearningEnhancer(db)
    
    dashboard_data = {}
    for agent_type in ["sales_genie", "logibot", "buybot"]:
        enriched = enhancer.enrich_agent_training_data(agent_type)
        dataset = enhancer.create_agent_training_dataset(agent_type)
        
        dashboard_data[agent_type] = {
            "insights_count": len(enriched['insights']),
            "training_examples": len(dataset['training_examples']),
            "performance_metrics": dataset['performance_metrics'],
            "optimization_targets": dataset['optimization_targets']
        }
    
    return dashboard_data
```

### **Integration with API**
```python
# Add to your FastAPI endpoints
@app.get("/api/agent-learning/{agent_type}")
async def get_agent_learning_data(agent_type: str):
    enhancer = AgentLearningEnhancer(db)
    
    enriched = enhancer.enrich_agent_training_data(agent_type)
    dataset = enhancer.create_agent_training_dataset(agent_type)
    optimized = enhancer.optimize_agent_prompts(agent_type)
    
    return {
        "agent_type": agent_type,
        "enriched_data": enriched,
        "training_dataset": dataset,
        "optimized_prompts": optimized
    }
```

---

## 🎉 **Conclusion**

The `AgentLearningEnhancer` provides powerful tools to accelerate your agents' intelligence improvement. Use it regularly to:

1. **Enrich training data** with performance insights
2. **Create comprehensive datasets** for learning
3. **Optimize prompts** based on historical performance
4. **Monitor learning progress** over time
5. **Generate actionable recommendations** for improvement

Your agents will become increasingly intelligent with systematic use of these tools! 🚀 