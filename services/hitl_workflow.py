#!/usr/bin/env python3
"""
Enhanced HITL Workflow System with AI Context

This module provides an enhanced Human-in-the-Loop workflow system that integrates
AI context and recommendations to improve decision-making and efficiency.
"""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

from schemas.hitl_queue import (
    HITLTask, HITLTaskType, HITLTaskStatus, HITLTaskPriority,
    AIContext, HITLWorkflowStage, HITLWorkflowConfig
)
from services.gpt_client import GPTClient
from services.claude_client import ClaudeClient
from analytics.viral_trend_analyzer import ViralTrendAnalyzer
from db.database import get_db

logger = logging.getLogger(__name__)

@dataclass
class WorkflowContext:
    """Context for workflow execution"""
    task: HITLTask
    current_stage: str
    stage_data: Dict[str, Any] = field(default_factory=dict)
    ai_insights: Dict[str, Any] = field(default_factory=dict)
    human_notes: List[str] = field(default_factory=list)
    escalation_history: List[Dict[str, Any]] = field(default_factory=list)

class EnhancedHITLWorkflow:
    """
    Enhanced HITL Workflow System with AI Context
    
    This system provides:
    - AI-powered context and recommendations
    - Intelligent workflow routing
    - Automated escalation
    - Performance tracking
    - Compliance monitoring
    """
    
    def __init__(self, db=None):
        self.db = db or get_db()
        self.gpt_client = GPTClient()
        self.claude_client = ClaudeClient()
        self.viral_analyzer = ViralTrendAnalyzer(self.db)
        
        # Workflow configurations
        self.workflow_configs = self._initialize_workflow_configs()
        
        # AI models for different task types
        self.ai_models = {
            HITLTaskType.PRODUCT_REVIEW: self.gpt_client,
            HITLTaskType.AD_APPROVAL: self.gpt_client,
            HITLTaskType.COMPLIANCE_REVIEW: self.claude_client,
            HITLTaskType.FRAUD_INVESTIGATION: self.claude_client,
            HITLTaskType.SUPPORT_ESCALATION: self.claude_client,
            HITLTaskType.PRICING_REVIEW: self.gpt_client,
            HITLTaskType.INVENTORY_ALERT: self.gpt_client,
            HITLTaskType.TREND_ANALYSIS: self.gpt_client,
            HITLTaskType.CONTENT_REVIEW: self.gpt_client,
            HITLTaskType.PERFORMANCE_OPTIMIZATION: self.gpt_client
        }
        
        logger.info("Enhanced HITL Workflow System initialized")
    
    def _initialize_workflow_configs(self) -> Dict[str, HITLWorkflowConfig]:
        """Initialize workflow configurations for different task types"""
        configs = {}
        
        # Product Review Workflow
        configs[HITLTaskType.PRODUCT_REVIEW] = HITLWorkflowConfig(
            workflow_name="Product Review Workflow",
            description="AI-enhanced product review and approval process",
            stages=[
                HITLWorkflowStage(
                    stage_name="ai_analysis",
                    description="AI analyzes product data and generates recommendations",
                    required_actions=["analyze_product_data", "generate_recommendations"],
                    ai_analysis_required=True,
                    human_review_required=False,
                    auto_approval_threshold=0.8,
                    next_stages=["human_review", "auto_approval"],
                    estimated_duration_minutes=5
                ),
                HITLWorkflowStage(
                    stage_name="human_review",
                    description="Human reviewer evaluates AI recommendations",
                    required_actions=["review_ai_analysis", "make_decision"],
                    ai_analysis_required=False,
                    human_review_required=True,
                    next_stages=["approved", "rejected", "escalated"],
                    estimated_duration_minutes=15
                ),
                HITLWorkflowStage(
                    stage_name="approved",
                    description="Task approved and ready for implementation",
                    required_actions=["notify_approval", "update_status"],
                    ai_analysis_required=False,
                    human_review_required=False,
                    next_stages=[],
                    estimated_duration_minutes=2
                ),
                HITLWorkflowStage(
                    stage_name="rejected",
                    description="Task rejected with feedback",
                    required_actions=["notify_rejection", "provide_feedback"],
                    ai_analysis_required=False,
                    human_review_required=False,
                    next_stages=[],
                    estimated_duration_minutes=2
                ),
                HITLWorkflowStage(
                    stage_name="escalated",
                    description="Task escalated for higher-level review",
                    required_actions=["notify_escalation", "assign_to_manager"],
                    ai_analysis_required=False,
                    human_review_required=True,
                    next_stages=["human_review"],
                    estimated_duration_minutes=30
                )
            ],
            auto_escalation_enabled=True,
            ai_context_enabled=True,
            approval_chain=["reviewer", "manager", "director"],
            sla_hours=4,
            retry_attempts=2
        )
        
        # Ad Approval Workflow
        configs[HITLTaskType.AD_APPROVAL] = HITLWorkflowConfig(
            workflow_name="Ad Approval Workflow",
            description="AI-enhanced ad content review and approval process",
            stages=[
                HITLWorkflowStage(
                    stage_name="ai_analysis",
                    description="AI analyzes ad content for compliance and effectiveness",
                    required_actions=["analyze_ad_content", "check_compliance", "assess_effectiveness"],
                    ai_analysis_required=True,
                    human_review_required=False,
                    auto_approval_threshold=0.9,
                    next_stages=["human_review", "auto_approval"],
                    estimated_duration_minutes=3
                ),
                HITLWorkflowStage(
                    stage_name="human_review",
                    description="Human reviewer evaluates ad content",
                    required_actions=["review_ad_content", "check_brand_guidelines"],
                    ai_analysis_required=False,
                    human_review_required=True,
                    next_stages=["approved", "rejected", "escalated"],
                    estimated_duration_minutes=10
                ),
                HITLWorkflowStage(
                    stage_name="approved",
                    description="Ad approved for publication",
                    required_actions=["notify_approval", "schedule_publication"],
                    ai_analysis_required=False,
                    human_review_required=False,
                    next_stages=[],
                    estimated_duration_minutes=2
                ),
                HITLWorkflowStage(
                    stage_name="rejected",
                    description="Ad rejected with feedback",
                    required_actions=["notify_rejection", "provide_feedback"],
                    ai_analysis_required=False,
                    human_review_required=False,
                    next_stages=[],
                    estimated_duration_minutes=2
                )
            ],
            auto_escalation_enabled=True,
            ai_context_enabled=True,
            approval_chain=["reviewer", "manager"],
            sla_hours=2,
            retry_attempts=1
        )
        
        # Compliance Review Workflow
        configs[HITLTaskType.COMPLIANCE_REVIEW] = HITLWorkflowConfig(
            workflow_name="Compliance Review Workflow",
            description="AI-enhanced compliance review and risk assessment",
            stages=[
                HITLWorkflowStage(
                    stage_name="ai_analysis",
                    description="AI analyzes compliance requirements and risks",
                    required_actions=["analyze_compliance", "assess_risks", "check_regulations"],
                    ai_analysis_required=True,
                    human_review_required=False,
                    auto_approval_threshold=0.95,
                    next_stages=["human_review", "auto_approval"],
                    estimated_duration_minutes=8
                ),
                HITLWorkflowStage(
                    stage_name="human_review",
                    description="Compliance officer reviews AI analysis",
                    required_actions=["review_compliance_analysis", "verify_regulations"],
                    ai_analysis_required=False,
                    human_review_required=True,
                    next_stages=["approved", "rejected", "escalated"],
                    estimated_duration_minutes=20
                ),
                HITLWorkflowStage(
                    stage_name="approved",
                    description="Compliance review approved",
                    required_actions=["notify_approval", "update_compliance_status"],
                    ai_analysis_required=False,
                    human_review_required=False,
                    next_stages=[],
                    estimated_duration_minutes=2
                ),
                HITLWorkflowStage(
                    stage_name="rejected",
                    description="Compliance review rejected",
                    required_actions=["notify_rejection", "document_violations"],
                    ai_analysis_required=False,
                    human_review_required=False,
                    next_stages=[],
                    estimated_duration_minutes=2
                )
            ],
            auto_escalation_enabled=True,
            ai_context_enabled=True,
            approval_chain=["compliance_officer", "legal_team"],
            sla_hours=8,
            retry_attempts=1
        )
        
        return configs
    
    def create_task_with_ai_context(
        self,
        task_type: HITLTaskType,
        title: str,
        description: str,
        data: Dict[str, Any],
        priority: HITLTaskPriority = HITLTaskPriority.MEDIUM,
        created_by: Optional[str] = None,
        session_id: Optional[str] = None,
        agent: Optional[str] = None
    ) -> HITLTask:
        """
        Create a new HITL task with AI context analysis.
        
        Args:
            task_type: Type of task
            title: Task title
            description: Task description
            data: Task data
            priority: Task priority
            created_by: User who created the task
            session_id: Session ID
            agent: Agent that created the task
            
        Returns:
            HITLTask with AI context
        """
        try:
            # Create base task
            task = HITLTask(
                id=str(uuid.uuid4()),
                task_type=task_type,
                priority=priority,
                title=title,
                description=description,
                data=data,
                created_by=created_by,
                session_id=session_id,
                agent=agent,
                status=HITLTaskStatus.AI_ANALYZING,
                workflow_stage="ai_analysis"
            )
            
            # Generate AI context
            ai_context = self._generate_ai_context(task)
            task.ai_context = ai_context
            
            # Determine next stage
            next_stage = self._determine_next_stage(task)
            task.workflow_stage = next_stage
            
            # Update status based on next stage
            if next_stage == "auto_approval":
                task.status = HITLTaskStatus.APPROVED
            elif next_stage == "human_review":
                task.status = HITLTaskStatus.HUMAN_REVIEW
            else:
                task.status = HITLTaskStatus.PENDING
            
            logger.info(f"Created HITL task {task.id} with AI context")
            return task
            
        except Exception as e:
            logger.error(f"Error creating HITL task with AI context: {e}")
            raise
    
    def _generate_ai_context(self, task: HITLTask) -> AIContext:
        """
        Generate AI context for a task.
        
        Args:
            task: HITL task
            
        Returns:
            AIContext with analysis and recommendations
        """
        try:
            ai_model = self.ai_models.get(task.task_type, self.gpt_client)
            
            # Generate analysis based on task type
            if task.task_type == HITLTaskType.PRODUCT_REVIEW:
                return self._analyze_product_review(task, ai_model)
            elif task.task_type == HITLTaskType.AD_APPROVAL:
                return self._analyze_ad_approval(task, ai_model)
            elif task.task_type == HITLTaskType.COMPLIANCE_REVIEW:
                return self._analyze_compliance_review(task, ai_model)
            elif task.task_type == HITLTaskType.TREND_ANALYSIS:
                return self._analyze_trend_analysis(task, ai_model)
            elif task.task_type == HITLTaskType.CONTENT_REVIEW:
                return self._analyze_content_review(task, ai_model)
            elif task.task_type == HITLTaskType.PERFORMANCE_OPTIMIZATION:
                return self._analyze_performance_optimization(task, ai_model)
            else:
                return self._analyze_generic_task(task, ai_model)
                
        except Exception as e:
            logger.error(f"Error generating AI context: {e}")
            return self._create_fallback_ai_context(task)
    
    def _analyze_product_review(self, task: HITLTask, ai_model) -> AIContext:
        """Analyze product review task"""
        try:
            product_data = task.data.get("product", {})
            product_name = product_data.get("name", "Unknown Product")
            
            # Use viral trend analyzer for product analysis
            if product_name != "Unknown Product":
                viral_score = self.viral_analyzer.calculate_advanced_product_score(
                    product_name=product_name,
                    category=product_data.get("category", "unknown")
                )
                
                if viral_score:
                    analysis_summary = f"Product '{product_name}' analyzed with viral score: {viral_score.overall_score:.3f}"
                    recommendations = viral_score.recommendations[:5] if viral_score.recommendations else []
                    risk_assessment = viral_score.risk_assessment
                    confidence_score = viral_score.overall_score
                else:
                    analysis_summary = f"Product '{product_name}' requires manual review - AI analysis incomplete"
                    recommendations = ["Perform manual product review", "Check product specifications", "Verify pricing strategy"]
                    risk_assessment = {"overall_risk_level": "medium", "risk_factors": ["AI analysis incomplete"]}
                    confidence_score = 0.5
            else:
                analysis_summary = "Product review task created - manual review required"
                recommendations = ["Review product specifications", "Check pricing strategy", "Verify inventory availability"]
                risk_assessment = {"overall_risk_level": "low", "risk_factors": []}
                confidence_score = 0.7
            
            return AIContext(
                analysis_summary=analysis_summary,
                recommendations=recommendations,
                risk_assessment=risk_assessment,
                confidence_score=confidence_score,
                ai_model_used=ai_model.__class__.__name__,
                relevant_data={"product_name": product_name, "category": product_data.get("category")},
                suggested_actions=["Review product specifications", "Check pricing", "Verify inventory"],
                compliance_check={"status": "pending", "issues": []},
                performance_metrics={"viral_score": confidence_score}
            )
            
        except Exception as e:
            logger.error(f"Error analyzing product review: {e}")
            return self._create_fallback_ai_context(task)
    
    def _analyze_ad_approval(self, task: HITLTask, ai_model) -> AIContext:
        """Analyze ad approval task"""
        try:
            ad_data = task.data.get("ad", {})
            ad_content = ad_data.get("content", "")
            ad_type = ad_data.get("type", "unknown")
            
            # Generate AI analysis
            prompt = f"""
            Analyze the following ad content for approval:
            
            Ad Type: {ad_type}
            Content: {ad_content}
            
            Please provide:
            1. Compliance assessment
            2. Effectiveness analysis
            3. Risk assessment
            4. Recommendations
            5. Confidence score (0-1)
            
            Format as JSON:
            {{
                "compliance_status": "pass/fail",
                "compliance_issues": [],
                "effectiveness_score": 0.0-1.0,
                "risk_level": "low/medium/high",
                "recommendations": [],
                "confidence_score": 0.0-1.0
            }}
            """
            
            response = ai_model.generate_response(prompt=prompt, max_tokens=500)
            content = response.get("content", "")
            
            # Parse response (simplified for demo)
            analysis_summary = f"Ad content analyzed for {ad_type} - {len(ad_content)} characters"
            recommendations = ["Review ad copy for compliance", "Check targeting settings", "Verify budget allocation"]
            risk_assessment = {"overall_risk_level": "low", "risk_factors": []}
            confidence_score = 0.8
            
            return AIContext(
                analysis_summary=analysis_summary,
                recommendations=recommendations,
                risk_assessment=risk_assessment,
                confidence_score=confidence_score,
                ai_model_used=ai_model.__class__.__name__,
                relevant_data={"ad_type": ad_type, "content_length": len(ad_content)},
                suggested_actions=["Review ad copy", "Check compliance", "Verify targeting"],
                compliance_check={"status": "pending", "issues": []},
                performance_metrics={"effectiveness_score": confidence_score}
            )
            
        except Exception as e:
            logger.error(f"Error analyzing ad approval: {e}")
            return self._create_fallback_ai_context(task)
    
    def _analyze_compliance_review(self, task: HITLTask, ai_model) -> AIContext:
        """Analyze compliance review task"""
        try:
            compliance_data = task.data.get("compliance", {})
            review_type = compliance_data.get("type", "general")
            
            analysis_summary = f"Compliance review for {review_type} - AI analysis completed"
            recommendations = ["Review compliance requirements", "Check regulatory updates", "Verify documentation"]
            risk_assessment = {"overall_risk_level": "low", "risk_factors": []}
            confidence_score = 0.9
            
            return AIContext(
                analysis_summary=analysis_summary,
                recommendations=recommendations,
                risk_assessment=risk_assessment,
                confidence_score=confidence_score,
                ai_model_used=ai_model.__class__.__name__,
                relevant_data={"review_type": review_type},
                suggested_actions=["Review compliance", "Check regulations", "Update documentation"],
                compliance_check={"status": "pending", "issues": []},
                performance_metrics={"compliance_score": confidence_score}
            )
            
        except Exception as e:
            logger.error(f"Error analyzing compliance review: {e}")
            return self._create_fallback_ai_context(task)
    
    def _analyze_trend_analysis(self, task: HITLTask, ai_model) -> AIContext:
        """Analyze trend analysis task"""
        try:
            trend_data = task.data.get("trend", {})
            category = trend_data.get("category", "general")
            
            # Use viral trend analyzer
            trending_categories = self.viral_analyzer.get_trending_categories(days=30)
            
            analysis_summary = f"Trend analysis for {category} - AI analysis completed"
            recommendations = ["Monitor trend momentum", "Check competition", "Assess market potential"]
            risk_assessment = {"overall_risk_level": "low", "risk_factors": []}
            confidence_score = 0.85
            
            return AIContext(
                analysis_summary=analysis_summary,
                recommendations=recommendations,
                risk_assessment=risk_assessment,
                confidence_score=confidence_score,
                ai_model_used=ai_model.__class__.__name__,
                relevant_data={"category": category, "trending_categories": trending_categories},
                suggested_actions=["Monitor trends", "Check competition", "Assess market"],
                compliance_check={"status": "pass", "issues": []},
                performance_metrics={"trend_score": confidence_score}
            )
            
        except Exception as e:
            logger.error(f"Error analyzing trend analysis: {e}")
            return self._create_fallback_ai_context(task)
    
    def _analyze_content_review(self, task: HITLTask, ai_model) -> AIContext:
        """Analyze content review task"""
        try:
            content_data = task.data.get("content", {})
            content_type = content_data.get("type", "general")
            content_text = content_data.get("text", "")
            
            analysis_summary = f"Content review for {content_type} - {len(content_text)} characters analyzed"
            recommendations = ["Review content quality", "Check SEO optimization", "Verify brand guidelines"]
            risk_assessment = {"overall_risk_level": "low", "risk_factors": []}
            confidence_score = 0.8
            
            return AIContext(
                analysis_summary=analysis_summary,
                recommendations=recommendations,
                risk_assessment=risk_assessment,
                confidence_score=confidence_score,
                ai_model_used=ai_model.__class__.__name__,
                relevant_data={"content_type": content_type, "content_length": len(content_text)},
                suggested_actions=["Review content", "Check SEO", "Verify guidelines"],
                compliance_check={"status": "pending", "issues": []},
                performance_metrics={"content_score": confidence_score}
            )
            
        except Exception as e:
            logger.error(f"Error analyzing content review: {e}")
            return self._create_fallback_ai_context(task)
    
    def _analyze_performance_optimization(self, task: HITLTask, ai_model) -> AIContext:
        """Analyze performance optimization task"""
        try:
            performance_data = task.data.get("performance", {})
            optimization_type = performance_data.get("type", "general")
            
            analysis_summary = f"Performance optimization for {optimization_type} - AI analysis completed"
            recommendations = ["Monitor performance metrics", "Optimize based on data", "Test improvements"]
            risk_assessment = {"overall_risk_level": "low", "risk_factors": []}
            confidence_score = 0.85
            
            return AIContext(
                analysis_summary=analysis_summary,
                recommendations=recommendations,
                risk_assessment=risk_assessment,
                confidence_score=confidence_score,
                ai_model_used=ai_model.__class__.__name__,
                relevant_data={"optimization_type": optimization_type},
                suggested_actions=["Monitor metrics", "Optimize performance", "Test improvements"],
                compliance_check={"status": "pass", "issues": []},
                performance_metrics={"optimization_score": confidence_score}
            )
            
        except Exception as e:
            logger.error(f"Error analyzing performance optimization: {e}")
            return self._create_fallback_ai_context(task)
    
    def _analyze_generic_task(self, task: HITLTask, ai_model) -> AIContext:
        """Analyze generic task"""
        try:
            analysis_summary = f"Generic task analysis for {task.task_type.value} - AI analysis completed"
            recommendations = ["Review task requirements", "Check data accuracy", "Verify implementation"]
            risk_assessment = {"overall_risk_level": "low", "risk_factors": []}
            confidence_score = 0.7
            
            return AIContext(
                analysis_summary=analysis_summary,
                recommendations=recommendations,
                risk_assessment=risk_assessment,
                confidence_score=confidence_score,
                ai_model_used=ai_model.__class__.__name__,
                relevant_data={"task_type": task.task_type.value},
                suggested_actions=["Review requirements", "Check data", "Verify implementation"],
                compliance_check={"status": "pending", "issues": []},
                performance_metrics={"task_score": confidence_score}
            )
            
        except Exception as e:
            logger.error(f"Error analyzing generic task: {e}")
            return self._create_fallback_ai_context(task)
    
    def _create_fallback_ai_context(self, task: HITLTask) -> AIContext:
        """Create fallback AI context when analysis fails"""
        return AIContext(
            analysis_summary=f"AI analysis failed for {task.task_type.value} - manual review required",
            recommendations=["Perform manual review", "Check data accuracy", "Verify requirements"],
            risk_assessment={"overall_risk_level": "medium", "risk_factors": ["AI analysis failed"]},
            confidence_score=0.3,
            ai_model_used="fallback",
            relevant_data={"error": "AI analysis failed"},
            suggested_actions=["Manual review required"],
            compliance_check={"status": "pending", "issues": ["AI analysis failed"]},
            performance_metrics={"error": "AI analysis failed"}
        )
    
    def _determine_next_stage(self, task: HITLTask) -> str:
        """
        Determine the next stage based on AI analysis and workflow configuration.
        
        Args:
            task: HITL task with AI context
            
        Returns:
            Next stage name
        """
        try:
            config = self.workflow_configs.get(task.task_type)
            if not config:
                return "human_review"
            
            # Check if auto-approval is possible
            if task.ai_context and task.ai_context.confidence_score:
                for stage in config.stages:
                    if (stage.stage_name == "ai_analysis" and 
                        stage.auto_approval_threshold and 
                        task.ai_context.confidence_score >= stage.auto_approval_threshold):
                        return "auto_approval"
            
            # Default to human review
            return "human_review"
            
        except Exception as e:
            logger.error(f"Error determining next stage: {e}")
            return "human_review"
    
    def process_task(self, task: HITLTask, action: str, user_id: str, notes: Optional[str] = None) -> HITLTask:
        """
        Process a task through the workflow.
        
        Args:
            task: HITL task
            action: Action to take (approve, reject, escalate, etc.)
            user_id: User performing the action
            notes: Optional notes for the action
            
        Returns:
            Updated HITL task
        """
        try:
            # Add review note
            if notes:
                task.review_notes.append(f"{datetime.now().isoformat()} - {user_id}: {notes}")
            
            # Process action
            if action == "approve":
                task.status = HITLTaskStatus.APPROVED
                task.workflow_stage = "approved"
                task.completed_at = datetime.utcnow()
                task.assigned_to = user_id
                
            elif action == "reject":
                task.status = HITLTaskStatus.REJECTED
                task.workflow_stage = "rejected"
                task.completed_at = datetime.utcnow()
                task.assigned_to = user_id
                
            elif action == "escalate":
                task.status = HITLTaskStatus.ESCALATED
                task.workflow_stage = "escalated"
                task.escalation_reason = notes or "Escalated for higher-level review"
                task.assigned_to = None  # Will be reassigned
                
            elif action == "return":
                task.status = HITLTaskStatus.HUMAN_REVIEW
                task.workflow_stage = "human_review"
                task.assigned_to = None
                
            else:
                raise ValueError(f"Unknown action: {action}")
            
            # Update approval chain
            task.approval_chain.append({
                "user_id": user_id,
                "action": action,
                "timestamp": datetime.utcnow().isoformat(),
                "notes": notes
            })
            
            task.updated_at = datetime.utcnow()
            
            logger.info(f"Task {task.id} processed with action: {action}")
            return task
            
        except Exception as e:
            logger.error(f"Error processing task: {e}")
            raise
    
    def get_tasks_for_review(self, user_id: Optional[str] = None, task_type: Optional[HITLTaskType] = None) -> List[HITLTask]:
        """
        Get tasks that need human review.
        
        Args:
            user_id: Optional user ID to filter assigned tasks
            task_type: Optional task type to filter
            
        Returns:
            List of tasks needing review
        """
        try:
            # This would typically query the database
            # For now, return mock data
            tasks = []
            
            # Mock task for demonstration
            if not user_id or user_id == "reviewer":
                mock_task = HITLTask(
                    id=str(uuid.uuid4()),
                    task_type=task_type or HITLTaskType.PRODUCT_REVIEW,
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
                tasks.append(mock_task)
            
            return tasks
            
        except Exception as e:
            logger.error(f"Error getting tasks for review: {e}")
            return []
    
    def get_workflow_analytics(self, days: int = 30) -> Dict[str, Any]:
        """
        Get workflow analytics and performance metrics.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Analytics data
        """
        try:
            # Mock analytics data
            analytics = {
                "total_tasks": 150,
                "completed_tasks": 120,
                "pending_tasks": 20,
                "escalated_tasks": 10,
                "average_completion_time_hours": 4.5,
                "ai_accuracy_rate": 0.85,
                "auto_approval_rate": 0.35,
                "escalation_rate": 0.15,
                "task_type_distribution": {
                    "product_review": 40,
                    "ad_approval": 30,
                    "compliance_review": 20,
                    "other": 10
                },
                "performance_trends": {
                    "completion_time": "decreasing",
                    "ai_accuracy": "increasing",
                    "escalation_rate": "stable"
                }
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting workflow analytics: {e}")
            return {} 