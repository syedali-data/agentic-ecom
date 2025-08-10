import json
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
from event_bus import event_bus, EventType

logger = logging.getLogger(__name__)

class TaskType(str, Enum):
    # SalesGenie tasks
    PRODUCT_RESEARCH = "product_research"
    LISTING_GENERATION = "listing_generation"
    AD_CREATION = "ad_creation"
    COMPLIANCE_REVIEW = "compliance_review"
    
    # LogiBot tasks
    ORDER_FULFILLMENT = "order_fulfillment"
    TRACKING_UPDATE = "tracking_update"
    SUPPORT_HANDLING = "support_handling"
    FRAUD_ANALYSIS = "fraud_analysis"
    
    # BuyBot tasks
    CUSTOMER_QUERY = "customer_query"
    PRODUCT_RECOMMENDATION = "product_recommendation"
    
    # System tasks
    DATA_SYNC = "data_sync"
    ERROR_HANDLING = "error_handling"

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class Task:
    id: str
    type: TaskType
    status: TaskStatus
    priority: TaskPriority
    source_agent: str
    target_agent: str
    data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class MCPProtocol:
    """Model Context Protocol for agent collaboration and task handoffs"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.agent_capabilities: Dict[str, List[TaskType]] = {
            "sales_genie": [
                TaskType.PRODUCT_RESEARCH,
                TaskType.LISTING_GENERATION,
                TaskType.AD_CREATION,
                TaskType.COMPLIANCE_REVIEW
            ],
            "logibot": [
                TaskType.ORDER_FULFILLMENT,
                TaskType.TRACKING_UPDATE,
                TaskType.SUPPORT_HANDLING,
                TaskType.FRAUD_ANALYSIS
            ],
            "buybot": [
                TaskType.CUSTOMER_QUERY,
                TaskType.PRODUCT_RECOMMENDATION
            ]
        }
        logger.info("MCP Protocol initialized")
    
    def create_task(
        self,
        task_type: TaskType,
        source_agent: str,
        target_agent: str,
        data: Dict[str, Any],
        priority: TaskPriority = TaskPriority.MEDIUM,
        session_id: Optional[str] = None
    ) -> str:
        """Create a new task for agent handoff"""
        import uuid
        
        task_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        task = Task(
            id=task_id,
            type=task_type,
            status=TaskStatus.PENDING,
            priority=priority,
            source_agent=source_agent,
            target_agent=target_agent,
            data=data,
            created_at=now,
            updated_at=now,
            session_id=session_id
        )
        
        self.tasks[task_id] = task
        
        # Publish task creation event
        event_bus.publish_simple(
            EventType.AGENT_STARTED,
            source_agent,
            {
                "task_id": task_id,
                "task_type": task_type.value,
                "target_agent": target_agent,
                "priority": priority.value
            },
            session_id
        )
        
        logger.info(f"Created task {task_id}: {task_type} from {source_agent} to {target_agent}")
        return task_id
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID"""
        return self.tasks.get(task_id)
    
    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ):
        """Update task status and result"""
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found")
            return
        
        task = self.tasks[task_id]
        task.status = status
        task.updated_at = datetime.utcnow()
        
        if status == TaskStatus.COMPLETED:
            task.completed_at = datetime.utcnow()
            task.result = result
        elif status == TaskStatus.FAILED:
            task.error = error
        
        logger.info(f"Updated task {task_id} status to {status}")
    
    def get_pending_tasks(self, agent: str) -> List[Task]:
        """Get pending tasks for a specific agent"""
        return [
            task for task in self.tasks.values()
            if task.target_agent == agent and task.status == TaskStatus.PENDING
        ]
    
    def get_tasks_by_type(self, task_type: TaskType) -> List[Task]:
        """Get all tasks of a specific type"""
        return [task for task in self.tasks.values() if task.type == task_type]
    
    def get_tasks_by_session(self, session_id: str) -> List[Task]:
        """Get all tasks for a specific session"""
        return [task for task in self.tasks.values() if task.session_id == session_id]
    
    def can_handle_task(self, agent: str, task_type: TaskType) -> bool:
        """Check if an agent can handle a specific task type"""
        return task_type in self.agent_capabilities.get(agent, [])
    
    def handoff_task(
        self,
        task_type: TaskType,
        source_agent: str,
        target_agent: str,
        data: Dict[str, Any],
        priority: TaskPriority = TaskPriority.MEDIUM,
        session_id: Optional[str] = None
    ) -> str:
        """Handoff a task from one agent to another"""
        if not self.can_handle_task(target_agent, task_type):
            raise ValueError(f"Agent {target_agent} cannot handle task type {task_type}")
        
        task_id = self.create_task(task_type, source_agent, target_agent, data, priority, session_id)
        
        logger.info(f"Task handoff: {task_type} from {source_agent} to {target_agent}")
        return task_id
    
    def complete_task(self, task_id: str, result: Dict[str, Any]):
        """Mark a task as completed with results"""
        self.update_task_status(task_id, TaskStatus.COMPLETED, result=result)
        
        task = self.get_task(task_id)
        if task:
            # Publish task completion event
            event_bus.publish_simple(
                EventType.AGENT_STOPPED,
                task.target_agent,
                {
                    "task_id": task_id,
                    "task_type": task.type.value,
                    "result": result
                },
                task.session_id
            )
    
    def fail_task(self, task_id: str, error: str):
        """Mark a task as failed with error"""
        self.update_task_status(task_id, TaskStatus.FAILED, error=error)
        
        task = self.get_task(task_id)
        if task:
            # Publish error event
            event_bus.publish_simple(
                EventType.ERROR_OCCURRED,
                task.target_agent,
                {
                    "task_id": task_id,
                    "task_type": task.type.value,
                    "error": error
                },
                task.session_id
            )
    
    def get_task_statistics(self) -> Dict[str, Any]:
        """Get task statistics"""
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
        failed_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.FAILED])
        pending_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING])
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "pending_tasks": pending_tasks,
            "success_rate": completed_tasks / total_tasks if total_tasks > 0 else 0
        }

# Global MCP protocol instance
mcp_protocol = MCPProtocol()

# Convenience functions for common handoffs
def handoff_product_research(product_data: Dict[str, Any], session_id: Optional[str] = None) -> str:
    """Handoff product research task to SalesGenie"""
    return mcp_protocol.handoff_task(
        TaskType.PRODUCT_RESEARCH,
        "system",
        "sales_genie",
        {"product_data": product_data},
        TaskPriority.MEDIUM,
        session_id
    )

def handoff_listing_generation(product_data: Dict[str, Any], session_id: Optional[str] = None) -> str:
    """Handoff listing generation task to SalesGenie"""
    return mcp_protocol.handoff_task(
        TaskType.LISTING_GENERATION,
        "system",
        "sales_genie",
        {"product_data": product_data},
        TaskPriority.MEDIUM,
        session_id
    )

def handoff_order_fulfillment(order_data: Dict[str, Any], session_id: Optional[str] = None) -> str:
    """Handoff order fulfillment task to LogiBot"""
    return mcp_protocol.handoff_task(
        TaskType.ORDER_FULFILLMENT,
        "system",
        "logibot",
        {"order_data": order_data},
        TaskPriority.HIGH,
        session_id
    )

def handoff_support_ticket(ticket_data: Dict[str, Any], session_id: Optional[str] = None) -> str:
    """Handoff support ticket task to LogiBot"""
    return mcp_protocol.handoff_task(
        TaskType.SUPPORT_HANDLING,
        "system",
        "logibot",
        {"ticket_data": ticket_data},
        TaskPriority.MEDIUM,
        session_id
    )

def handoff_customer_query(query_data: Dict[str, Any], session_id: Optional[str] = None) -> str:
    """Handoff customer query task to BuyBot"""
    return mcp_protocol.handoff_task(
        TaskType.CUSTOMER_QUERY,
        "system",
        "buybot",
        {"query_data": query_data},
        TaskPriority.MEDIUM,
        session_id
    ) 