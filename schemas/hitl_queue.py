from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class HITLTaskType(str, Enum):
    PRODUCT_REVIEW = "product_review"
    AD_APPROVAL = "ad_approval"
    COMPLIANCE_REVIEW = "compliance_review"
    FRAUD_INVESTIGATION = "fraud_investigation"
    SUPPORT_ESCALATION = "support_escalation"
    PRICING_REVIEW = "pricing_review"
    INVENTORY_ALERT = "inventory_alert"
    TREND_ANALYSIS = "trend_analysis"
    CONTENT_REVIEW = "content_review"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"

class HITLTaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"
    CANCELLED = "cancelled"
    AI_ANALYZING = "ai_analyzing"
    HUMAN_REVIEW = "human_review"

class HITLTaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class AIContext(BaseModel):
    """AI-generated context for HITL tasks"""
    analysis_summary: str
    recommendations: List[str] = Field(default_factory=list)
    risk_assessment: Dict[str, Any] = Field(default_factory=dict)
    confidence_score: float = Field(ge=0.0, le=1.0)
    ai_model_used: str
    analysis_timestamp: datetime = Field(default_factory=datetime.utcnow)
    relevant_data: Dict[str, Any] = Field(default_factory=dict)
    suggested_actions: List[str] = Field(default_factory=list)
    compliance_check: Dict[str, Any] = Field(default_factory=dict)
    performance_metrics: Dict[str, Any] = Field(default_factory=dict)

class HITLTask(BaseModel):
    id: Optional[str] = None
    task_type: HITLTaskType
    status: HITLTaskStatus = HITLTaskStatus.PENDING
    priority: HITLTaskPriority = HITLTaskPriority.MEDIUM
    title: str
    description: str
    data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    assigned_to: Optional[str] = None
    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    session_id: Optional[str] = None
    agent: Optional[str] = None
    ai_context: Optional[AIContext] = None
    workflow_stage: str = "initial"
    escalation_reason: Optional[str] = None
    review_notes: List[str] = Field(default_factory=list)
    approval_chain: List[Dict[str, Any]] = Field(default_factory=list)

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class HITLTaskCreate(BaseModel):
    task_type: HITLTaskType
    priority: HITLTaskPriority = HITLTaskPriority.MEDIUM
    title: str
    description: str
    data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_by: Optional[str] = None
    due_date: Optional[datetime] = None
    session_id: Optional[str] = None
    agent: Optional[str] = None
    ai_context: Optional[AIContext] = None

class HITLTaskUpdate(BaseModel):
    status: Optional[HITLTaskStatus] = None
    priority: Optional[HITLTaskPriority] = None
    title: Optional[str] = None
    description: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None
    ai_context: Optional[AIContext] = None
    workflow_stage: Optional[str] = None
    escalation_reason: Optional[str] = None
    review_notes: Optional[List[str]] = None

class HITLTaskResponse(BaseModel):
    id: str
    task_type: HITLTaskType
    status: HITLTaskStatus
    priority: HITLTaskPriority
    title: str
    description: str
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    assigned_to: Optional[str]
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
    session_id: Optional[str]
    agent: Optional[str]
    ai_context: Optional[AIContext]
    workflow_stage: str
    escalation_reason: Optional[str]
    review_notes: List[str]
    approval_chain: List[Dict[str, Any]]

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class HITLTaskSearch(BaseModel):
    task_type: Optional[HITLTaskType] = None
    priority: Optional[HITLTaskPriority] = None
    assigned_to: Optional[str] = None
    created_by: Optional[str] = None
    agent: Optional[str] = None
    session_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[HITLTaskStatus] = None
    workflow_stage: Optional[str] = None
    limit: int = Field(50, ge=1, le=100)
    offset: int = Field(0, ge=0)

class HITLTaskComment(BaseModel):
    id: Optional[str] = None
    task_id: str
    user_id: str
    comment: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    ai_generated: bool = False
    ai_context: Optional[Dict[str, Any]] = None

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class HITLWorkflowStage(BaseModel):
    """Workflow stage definition for HITL tasks"""
    stage_name: str
    description: str
    required_actions: List[str]
    ai_analysis_required: bool = False
    human_review_required: bool = True
    auto_approval_threshold: Optional[float] = None
    escalation_conditions: List[Dict[str, Any]] = Field(default_factory=list)
    next_stages: List[str] = Field(default_factory=list)
    estimated_duration_minutes: int = 30

class HITLWorkflowConfig(BaseModel):
    """Configuration for HITL workflows"""
    workflow_name: str
    description: str
    stages: List[HITLWorkflowStage]
    auto_escalation_enabled: bool = True
    ai_context_enabled: bool = True
    approval_chain: List[str] = Field(default_factory=list)
    sla_hours: int = 24
    retry_attempts: int = 3 