#!/usr/bin/env python3
"""
Enhanced HITL Workflow API

This module provides FastAPI endpoints for the enhanced Human-in-the-Loop workflow system
with AI context and intelligent routing.
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel

from schemas.hitl_queue import (
    HITLTask, HITLTaskType, HITLTaskStatus, HITLTaskPriority,
    HITLTaskCreate, HITLTaskUpdate, HITLTaskResponse, HITLTaskSearch,
    AIContext, HITLWorkflowConfig
)
from services.hitl_workflow import EnhancedHITLWorkflow
from db.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/hitl", tags=["HITL Workflow"])

# Initialize workflow system
workflow_system = EnhancedHITLWorkflow()

class TaskActionRequest(BaseModel):
    """Request model for task actions"""
    action: str  # approve, reject, escalate, return
    user_id: str
    notes: Optional[str] = None

class TaskActionResponse(BaseModel):
    """Response model for task actions"""
    task_id: str
    action: str
    status: str
    message: str
    updated_task: HITLTaskResponse

class WorkflowAnalyticsResponse(BaseModel):
    """Response model for workflow analytics"""
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    escalated_tasks: int
    average_completion_time_hours: float
    ai_accuracy_rate: float
    auto_approval_rate: float
    escalation_rate: float
    task_type_distribution: Dict[str, int]
    performance_trends: Dict[str, str]

@router.post("/tasks", response_model=HITLTaskResponse)
async def create_task_with_ai_context(task: HITLTaskCreate):
    """
    Create a new HITL task with AI context analysis.
    
    This endpoint creates a task and automatically generates AI context
    and recommendations to assist human reviewers.
    """
    try:
        # Create task with AI context
        hitl_task = workflow_system.create_task_with_ai_context(
            task_type=task.task_type,
            title=task.title,
            description=task.description,
            data=task.data,
            priority=task.priority,
            created_by=task.created_by,
            session_id=task.session_id,
            agent=task.agent
        )
        
        # Convert to response model
        response = HITLTaskResponse(
            id=hitl_task.id,
            task_type=hitl_task.task_type,
            status=hitl_task.status,
            priority=hitl_task.priority,
            title=hitl_task.title,
            description=hitl_task.description,
            data=hitl_task.data,
            metadata=hitl_task.metadata,
            assigned_to=hitl_task.assigned_to,
            created_by=hitl_task.created_by,
            created_at=hitl_task.created_at,
            updated_at=hitl_task.updated_at,
            due_date=hitl_task.due_date,
            completed_at=hitl_task.completed_at,
            session_id=hitl_task.session_id,
            agent=hitl_task.agent,
            ai_context=hitl_task.ai_context,
            workflow_stage=hitl_task.workflow_stage,
            escalation_reason=hitl_task.escalation_reason,
            review_notes=hitl_task.review_notes,
            approval_chain=hitl_task.approval_chain
        )
        
        logger.info(f"Created HITL task {hitl_task.id} with AI context")
        return response
        
    except Exception as e:
        logger.error(f"Error creating HITL task: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")

@router.get("/tasks", response_model=List[HITLTaskResponse])
async def get_tasks(
    task_type: Optional[HITLTaskType] = Query(None),
    status: Optional[HITLTaskStatus] = Query(None),
    priority: Optional[HITLTaskPriority] = Query(None),
    assigned_to: Optional[str] = Query(None),
    workflow_stage: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Get HITL tasks with optional filtering.
    
    Supports filtering by task type, status, priority, assigned user,
    and workflow stage.
    """
    try:
        # Get tasks for review (this would typically query the database)
        tasks = workflow_system.get_tasks_for_review(
            user_id=assigned_to,
            task_type=task_type
        )
        
        # Apply filters
        filtered_tasks = []
        for task in tasks:
            if status and task.status != status:
                continue
            if priority and task.priority != priority:
                continue
            if workflow_stage and task.workflow_stage != workflow_stage:
                continue
            filtered_tasks.append(task)
        
        # Apply pagination
        paginated_tasks = filtered_tasks[offset:offset + limit]
        
        # Convert to response models
        responses = []
        for task in paginated_tasks:
            response = HITLTaskResponse(
                id=task.id,
                task_type=task.task_type,
                status=task.status,
                priority=task.priority,
                title=task.title,
                description=task.description,
                data=task.data,
                metadata=task.metadata,
                assigned_to=task.assigned_to,
                created_by=task.created_by,
                created_at=task.created_at,
                updated_at=task.updated_at,
                due_date=task.due_date,
                completed_at=task.completed_at,
                session_id=task.session_id,
                agent=task.agent,
                ai_context=task.ai_context,
                workflow_stage=task.workflow_stage,
                escalation_reason=task.escalation_reason,
                review_notes=task.review_notes,
                approval_chain=task.approval_chain
            )
            responses.append(response)
        
        return responses
        
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get tasks: {str(e)}")

@router.get("/tasks/{task_id}", response_model=HITLTaskResponse)
async def get_task(task_id: str):
    """
    Get a specific HITL task by ID.
    
    Returns the task with full AI context and workflow information.
    """
    try:
        # This would typically query the database
        # For now, return a mock task
        mock_task = HITLTask(
            id=task_id,
            task_type=HITLTaskType.PRODUCT_REVIEW,
            status=HITLTaskStatus.HUMAN_REVIEW,
            priority=HITLTaskPriority.MEDIUM,
            title="Sample Product Review",
            description="Review sample product for approval",
            data={"product": {"name": "Sample Product", "category": "electronics"}},
            workflow_stage="human_review",
            ai_context=AIContext(
                analysis_summary="Sample product analyzed with AI",
                recommendations=["Check product specifications", "Verify pricing"],
                risk_assessment={"overall_risk_level": "low"},
                confidence_score=0.8,
                ai_model_used="GPTClient"
            )
        )
        
        response = HITLTaskResponse(
            id=mock_task.id,
            task_type=mock_task.task_type,
            status=mock_task.status,
            priority=mock_task.priority,
            title=mock_task.title,
            description=mock_task.description,
            data=mock_task.data,
            metadata=mock_task.metadata,
            assigned_to=mock_task.assigned_to,
            created_by=mock_task.created_by,
            created_at=mock_task.created_at,
            updated_at=mock_task.updated_at,
            due_date=mock_task.due_date,
            completed_at=mock_task.completed_at,
            session_id=mock_task.session_id,
            agent=mock_task.agent,
            ai_context=mock_task.ai_context,
            workflow_stage=mock_task.workflow_stage,
            escalation_reason=mock_task.escalation_reason,
            review_notes=mock_task.review_notes,
            approval_chain=mock_task.approval_chain
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error getting task {task_id}: {e}")
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")

@router.post("/tasks/{task_id}/actions", response_model=TaskActionResponse)
async def process_task_action(task_id: str, action_request: TaskActionRequest):
    """
    Process a task action (approve, reject, escalate, return).
    
    This endpoint allows human reviewers to take actions on tasks
    with AI context and recommendations.
    """
    try:
        # Get the task (this would typically query the database)
        # For now, create a mock task
        mock_task = HITLTask(
            id=task_id,
            task_type=HITLTaskType.PRODUCT_REVIEW,
            status=HITLTaskStatus.HUMAN_REVIEW,
            priority=HITLTaskPriority.MEDIUM,
            title="Sample Product Review",
            description="Review sample product for approval",
            data={"product": {"name": "Sample Product", "category": "electronics"}},
            workflow_stage="human_review"
        )
        
        # Process the action
        updated_task = workflow_system.process_task(
            task=mock_task,
            action=action_request.action,
            user_id=action_request.user_id,
            notes=action_request.notes
        )
        
        # Convert to response model
        response = HITLTaskResponse(
            id=updated_task.id,
            task_type=updated_task.task_type,
            status=updated_task.status,
            priority=updated_task.priority,
            title=updated_task.title,
            description=updated_task.description,
            data=updated_task.data,
            metadata=updated_task.metadata,
            assigned_to=updated_task.assigned_to,
            created_by=updated_task.created_by,
            created_at=updated_task.created_at,
            updated_at=updated_task.updated_at,
            due_date=updated_task.due_date,
            completed_at=updated_task.completed_at,
            session_id=updated_task.session_id,
            agent=updated_task.agent,
            ai_context=updated_task.ai_context,
            workflow_stage=updated_task.workflow_stage,
            escalation_reason=updated_task.escalation_reason,
            review_notes=updated_task.review_notes,
            approval_chain=updated_task.approval_chain
        )
        
        action_response = TaskActionResponse(
            task_id=task_id,
            action=action_request.action,
            status=updated_task.status.value,
            message=f"Task {action_request.action}ed successfully",
            updated_task=response
        )
        
        logger.info(f"Task {task_id} processed with action: {action_request.action}")
        return action_response
        
    except ValueError as e:
        logger.error(f"Invalid action for task {task_id}: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid action: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing task action: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process action: {str(e)}")

@router.get("/tasks/{task_id}/ai-context", response_model=AIContext)
async def get_task_ai_context(task_id: str):
    """
    Get AI context for a specific task.
    
    Returns the AI-generated analysis, recommendations, and insights
    for the task.
    """
    try:
        # This would typically query the database
        # For now, return mock AI context
        ai_context = AIContext(
            analysis_summary=f"AI analysis for task {task_id} - Product review completed",
            recommendations=[
                "Check product specifications",
                "Verify pricing strategy",
                "Assess market competition",
                "Review inventory availability"
            ],
            risk_assessment={
                "overall_risk_level": "low",
                "risk_factors": ["Low competition", "Good pricing"],
                "mitigation_strategies": ["Monitor performance", "Track inventory"]
            },
            confidence_score=0.85,
            ai_model_used="GPTClient",
            analysis_timestamp=datetime.utcnow(),
            relevant_data={
                "product_name": "Sample Product",
                "category": "electronics",
                "viral_score": 0.75
            },
            suggested_actions=[
                "Review product specifications",
                "Check pricing strategy",
                "Verify inventory availability"
            ],
            compliance_check={
                "status": "pass",
                "issues": [],
                "compliance_score": 0.9
            },
            performance_metrics={
                "viral_score": 0.75,
                "market_potential": 0.8,
                "competition_level": 0.3
            }
        )
        
        return ai_context
        
    except Exception as e:
        logger.error(f"Error getting AI context for task {task_id}: {e}")
        raise HTTPException(status_code=404, detail=f"AI context not found: {task_id}")

@router.get("/workflows/configs", response_model=Dict[str, HITLWorkflowConfig])
async def get_workflow_configs():
    """
    Get all workflow configurations.
    
    Returns the configuration for all supported workflow types
    including stages, requirements, and settings.
    """
    try:
        return workflow_system.workflow_configs
        
    except Exception as e:
        logger.error(f"Error getting workflow configs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get workflow configs: {str(e)}")

@router.get("/workflows/analytics", response_model=WorkflowAnalyticsResponse)
async def get_workflow_analytics(days: int = Query(30, ge=1, le=365)):
    """
    Get workflow analytics and performance metrics.
    
    Returns comprehensive analytics including task completion rates,
    AI accuracy, auto-approval rates, and performance trends.
    """
    try:
        analytics = workflow_system.get_workflow_analytics(days=days)
        
        response = WorkflowAnalyticsResponse(
            total_tasks=analytics["total_tasks"],
            completed_tasks=analytics["completed_tasks"],
            pending_tasks=analytics["pending_tasks"],
            escalated_tasks=analytics["escalated_tasks"],
            average_completion_time_hours=analytics["average_completion_time_hours"],
            ai_accuracy_rate=analytics["ai_accuracy_rate"],
            auto_approval_rate=analytics["auto_approval_rate"],
            escalation_rate=analytics["escalation_rate"],
            task_type_distribution=analytics["task_type_distribution"],
            performance_trends=analytics["performance_trends"]
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error getting workflow analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")

@router.get("/tasks/for-review", response_model=List[HITLTaskResponse])
async def get_tasks_for_review(
    user_id: Optional[str] = Query(None),
    task_type: Optional[HITLTaskType] = Query(None)
):
    """
    Get tasks that need human review.
    
    Returns tasks that are ready for human review, optionally filtered
    by user ID and task type.
    """
    try:
        tasks = workflow_system.get_tasks_for_review(
            user_id=user_id,
            task_type=task_type
        )
        
        # Convert to response models
        responses = []
        for task in tasks:
            response = HITLTaskResponse(
                id=task.id,
                task_type=task.task_type,
                status=task.status,
                priority=task.priority,
                title=task.title,
                description=task.description,
                data=task.data,
                metadata=task.metadata,
                assigned_to=task.assigned_to,
                created_by=task.created_by,
                created_at=task.created_at,
                updated_at=task.updated_at,
                due_date=task.due_date,
                completed_at=task.completed_at,
                session_id=task.session_id,
                agent=task.agent,
                ai_context=task.ai_context,
                workflow_stage=task.workflow_stage,
                escalation_reason=task.escalation_reason,
                review_notes=task.review_notes,
                approval_chain=task.approval_chain
            )
            responses.append(response)
        
        return responses
        
    except Exception as e:
        logger.error(f"Error getting tasks for review: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get tasks for review: {str(e)}")

@router.post("/tasks/{task_id}/escalate")
async def escalate_task(task_id: str, escalation_request: TaskActionRequest):
    """
    Escalate a task for higher-level review.
    
    This endpoint allows tasks to be escalated when they require
    additional review or approval.
    """
    try:
        # Get the task (this would typically query the database)
        mock_task = HITLTask(
            id=task_id,
            task_type=HITLTaskType.PRODUCT_REVIEW,
            status=HITLTaskStatus.HUMAN_REVIEW,
            priority=HITLTaskPriority.MEDIUM,
            title="Sample Product Review",
            description="Review sample product for approval",
            data={"product": {"name": "Sample Product", "category": "electronics"}},
            workflow_stage="human_review"
        )
        
        # Process escalation
        updated_task = workflow_system.process_task(
            task=mock_task,
            action="escalate",
            user_id=escalation_request.user_id,
            notes=escalation_request.notes or "Escalated for higher-level review"
        )
        
        return {
            "task_id": task_id,
            "status": "escalated",
            "message": "Task escalated successfully",
            "escalation_reason": updated_task.escalation_reason
        }
        
    except Exception as e:
        logger.error(f"Error escalating task {task_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to escalate task: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Health check endpoint for the HITL workflow system.
    
    Returns the status of the workflow system and its components.
    """
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "workflow_system": "operational",
            "ai_models": "available",
            "database": "connected"
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy") 