from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class EscalationType(str, Enum):
    FULFILLMENT_DELAY = "fulfillment_delay"
    PAYMENT_ISSUE = "payment_issue"
    FRAUD_ALERT = "fraud_alert"
    COMPLIANCE_VIOLATION = "compliance_violation"
    SYSTEM_ERROR = "system_error"
    BUDGET_EXCEEDED = "budget_exceeded"
    RATE_LIMIT_HIT = "rate_limit_hit"
    INVENTORY_SHORTAGE = "inventory_shortage"
    CUSTOMER_COMPLAINT = "customer_complaint"
    AD_REJECTION = "ad_rejection"

class EscalationSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class EscalationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    CANCELLED = "cancelled"

class EscalationEvent(BaseModel):
    id: Optional[str] = None
    escalation_type: EscalationType
    severity: EscalationSeverity
    status: EscalationStatus = EscalationStatus.PENDING
    title: str
    description: str
    data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    triggered_by: str
    assigned_to: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    session_id: Optional[str] = None
    agent: Optional[str] = None
    n8n_workflow_id: Optional[str] = None
    n8n_execution_id: Optional[str] = None

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class EscalationEventCreate(BaseModel):
    escalation_type: EscalationType
    severity: EscalationSeverity
    title: str
    description: str
    data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    triggered_by: str
    session_id: Optional[str] = None
    agent: Optional[str] = None
    n8n_workflow_id: Optional[str] = None

class EscalationEventUpdate(BaseModel):
    status: Optional[EscalationStatus] = None
    severity: Optional[EscalationSeverity] = None
    title: Optional[str] = None
    description: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    assigned_to: Optional[str] = None
    n8n_execution_id: Optional[str] = None

class EscalationEventResponse(BaseModel):
    id: str
    escalation_type: EscalationType
    severity: EscalationSeverity
    status: EscalationStatus
    title: str
    description: str
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    triggered_by: str
    assigned_to: Optional[str]
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]
    session_id: Optional[str]
    agent: Optional[str]
    n8n_workflow_id: Optional[str]
    n8n_execution_id: Optional[str]

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class EscalationEventSearch(BaseModel):
    escalation_type: Optional[EscalationType] = None
    severity: Optional[EscalationSeverity] = None
    status: Optional[EscalationStatus] = None
    triggered_by: Optional[str] = None
    assigned_to: Optional[str] = None
    agent: Optional[str] = None
    session_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(50, ge=1, le=100)
    offset: int = Field(0, ge=0)

class N8nWorkflowTrigger(BaseModel):
    workflow_id: str
    event_data: Dict[str, Any]
    escalation_event_id: Optional[str] = None
    priority: str = "normal"
    metadata: Dict[str, Any] = Field(default_factory=dict)

class N8nWorkflowResponse(BaseModel):
    execution_id: str
    workflow_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 