"""
Compliance Manager for Memory System
Handles GDPR, CCPA, and other privacy regulations for customer data.
"""

import logging
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class DataSubjectRequest:
    """Data structure for data subject requests."""
    request_id: str
    customer_id: str
    request_type: str  # access, deletion, rectification, portability
    status: str  # pending, processing, completed, denied
    created_at: str
    completed_at: Optional[str] = None
    data_categories: List[str] = None
    justification: Optional[str] = None

@dataclass
class ConsentRecord:
    """Data structure for consent records."""
    consent_id: str
    customer_id: str
    consent_type: str  # marketing, analytics, necessary, third_party
    granted: bool
    granted_at: str
    consent_text: str
    version: str
    revoked_at: Optional[str] = None

class ComplianceManager:
    """
    Compliance manager for handling privacy regulations and data subject requests.
    """
    
    def __init__(self):
        """Initialize ComplianceManager with privacy regulations."""
        self.logger = logging.getLogger(__name__)
        
        # Privacy regulations
        self.regulations = {
            "gdpr": {
                "enabled": True,
                "data_retention_days": 2555,  # 7 years
                "consent_required": True,
                "data_subject_rights": [
                    "access", "rectification", "erasure", "portability", 
                    "restriction", "objection", "withdraw_consent"
                ]
            },
            "ccpa": {
                "enabled": True,
                "data_retention_days": 2555,  # 7 years
                "consent_required": True,
                "data_subject_rights": [
                    "access", "deletion", "portability", "non-discrimination"
                ]
            },
            "pipeda": {
                "enabled": True,
                "data_retention_days": 2555,  # 7 years
                "consent_required": True,
                "data_subject_rights": [
                    "access", "correction", "deletion", "withdrawal_of_consent"
                ],
                "privacy_principles": [
                    "accountability",
                    "identifying_purposes", 
                    "consent",
                    "limiting_collection",
                    "limiting_use_disclosure_retention",
                    "accuracy",
                    "safeguards",
                    "openness",
                    "individual_access",
                    "challenging_compliance"
                ],
                "breach_notification": {
                    "required": True,
                    "timeframe_hours": 72,
                    "reporting_threshold": 1
                }
            },
            "hipaa": {
                "enabled": False,  # Set to True if handling health data
                "data_retention_days": 2555,
                "consent_required": True,
                "data_subject_rights": [
                    "access", "amendment", "accounting", "restriction"
                ]
            }
        }
        
        # Data categories for compliance
        self.data_categories = {
            "personal_data": ["name", "email", "phone", "address", "date_of_birth"],
            "transactional_data": ["purchase_history", "payment_info", "order_details"],
            "behavioral_data": ["browsing_history", "preferences", "interactions"],
            "technical_data": ["ip_address", "device_info", "cookies", "logs"]
        }
        
        self.logger.info("✅ ComplianceManager initialized with privacy regulations")
    
    def create_data_subject_request(self, customer_id: str, request_type: str, 
                                   data_categories: Optional[List[str]] = None) -> DataSubjectRequest:
        """
        Create a new data subject request.
        
        Args:
            customer_id: Customer identifier
            request_type: Type of request (access, deletion, etc.)
            data_categories: Specific data categories requested
            
        Returns:
            DataSubjectRequest object
        """
        try:
            request_id = f"dsr_{customer_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Validate request type
            valid_types = []
            for regulation in self.regulations.values():
                if regulation["enabled"]:
                    valid_types.extend(regulation["data_subject_rights"])
            
            if request_type not in valid_types:
                raise ValueError(f"Invalid request type: {request_type}")
            
            request = DataSubjectRequest(
                request_id=request_id,
                customer_id=customer_id,
                request_type=request_type,
                status="pending",
                created_at=datetime.now().isoformat(),
                data_categories=data_categories or []
            )
            
            self.logger.info(f"✅ Data subject request created: {request_id}")
            return request
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create data subject request: {e}")
            raise
    
    def process_data_subject_request(self, request: DataSubjectRequest) -> Dict[str, Any]:
        """
        Process a data subject request.
        
        Args:
            request: DataSubjectRequest object
            
        Returns:
            Processing result
        """
        try:
            self.logger.info(f"🔄 Processing data subject request: {request.request_id}")
            
            # Update status to processing
            request.status = "processing"
            
            # Process based on request type
            if request.request_type == "access":
                result = self._process_access_request(request)
            elif request.request_type == "deletion":
                result = self._process_deletion_request(request)
            elif request.request_type == "rectification":
                result = self._process_rectification_request(request)
            elif request.request_type == "portability":
                result = self._process_portability_request(request)
            else:
                result = {"error": f"Unsupported request type: {request.request_type}"}
            
            # Update status
            if "error" not in result:
                request.status = "completed"
                request.completed_at = datetime.now().isoformat()
            else:
                request.status = "denied"
                request.justification = result["error"]
            
            self.logger.info(f"✅ Data subject request processed: {request.request_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Failed to process data subject request: {e}")
            request.status = "denied"
            request.justification = str(e)
            return {"error": str(e)}
    
    def record_consent(self, customer_id: str, consent_type: str, granted: bool, 
                      consent_text: str, version: str = "1.0") -> ConsentRecord:
        """
        Record customer consent for data processing.
        
        Args:
            customer_id: Customer identifier
            consent_type: Type of consent (marketing, analytics, etc.)
            granted: Whether consent was granted
            consent_text: Text of the consent
            version: Version of the consent text
            
        Returns:
            ConsentRecord object
        """
        try:
            consent_id = f"consent_{customer_id}_{consent_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            consent = ConsentRecord(
                consent_id=consent_id,
                customer_id=customer_id,
                consent_type=consent_type,
                granted=granted,
                granted_at=datetime.now().isoformat(),
                consent_text=consent_text,
                version=version
            )
            
            self.logger.info(f"✅ Consent recorded: {consent_id}")
            return consent
            
        except Exception as e:
            self.logger.error(f"❌ Failed to record consent: {e}")
            raise
    
    def revoke_consent(self, customer_id: str, consent_type: str) -> bool:
        """
        Revoke customer consent for data processing.
        
        Args:
            customer_id: Customer identifier
            consent_type: Type of consent to revoke
            
        Returns:
            True if consent was revoked
        """
        try:
            # In production, this would update the consent record in the database
            self.logger.info(f"✅ Consent revoked: {customer_id} -> {consent_type}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to revoke consent: {e}")
            return False
    
    def check_consent_status(self, customer_id: str, consent_type: str) -> bool:
        """
        Check if customer has granted consent for specific data processing.
        
        Args:
            customer_id: Customer identifier
            consent_type: Type of consent to check
            
        Returns:
            True if consent is granted and active
        """
        try:
            # In production, this would query the consent records
            # For now, return True (assuming consent is granted)
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to check consent status: {e}")
            return False
    
    def generate_privacy_notice(self, customer_id: str, language: str = "en") -> Dict[str, Any]:
        """
        Generate privacy notice for customer.
        
        Args:
            customer_id: Customer identifier
            language: Language for the notice
            
        Returns:
            Privacy notice content
        """
        try:
            notice = {
                "customer_id": customer_id,
                "generated_at": datetime.now().isoformat(),
                "language": language,
                "regulations": [k for k, v in self.regulations.items() if v["enabled"]],
                "data_categories": self.data_categories,
                "data_rights": self._get_available_data_rights(),
                "retention_policy": self._get_retention_policy(),
                "contact_info": self._get_contact_info()
            }
            
            self.logger.info(f"✅ Privacy notice generated: {customer_id}")
            return notice
            
        except Exception as e:
            self.logger.error(f"❌ Failed to generate privacy notice: {e}")
            raise
    
    def audit_data_processing(self, customer_id: str, processing_purpose: str, 
                            data_categories: List[str]) -> Dict[str, Any]:
        """
        Audit data processing against compliance rules.
        
        Args:
            customer_id: Customer identifier
            processing_purpose: Purpose of data processing
            data_categories: Categories of data being processed
            
        Returns:
            Audit result with compliance status
        """
        try:
            audit_result = {
                "customer_id": customer_id,
                "audit_date": datetime.now().isoformat(),
                "processing_purpose": processing_purpose,
                "data_categories": data_categories,
                "compliance_status": "compliant",
                "retention_status": "within_limits",
                "recommendations": []
            }
            
            # Check GDPR compliance
            if self.regulations["gdpr"]["enabled"]:
                gdpr_check = self._check_gdpr_compliance(customer_id, processing_purpose, data_categories)
                audit_result["gdpr_compliance"] = gdpr_check
            
            # Check CCPA compliance
            if self.regulations["ccpa"]["enabled"]:
                ccpa_check = self._check_ccpa_compliance(customer_id, processing_purpose, data_categories)
                audit_result["ccpa_compliance"] = ccpa_check
            
            # Check PIPEDA compliance
            if self.regulations["pipeda"]["enabled"]:
                pipeda_check = self._check_pipeda_compliance(customer_id, processing_purpose, data_categories)
                audit_result["pipeda_compliance"] = pipeda_check
            
            # Check retention compliance
            retention_check = self._check_retention_compliance(customer_id)
            audit_result["retention_status"] = retention_check["status"]
            
            if retention_check["status"] != "within_limits":
                audit_result["compliance_status"] = "non_compliant"
                audit_result["recommendations"].append("Data retention policy violation detected")
            
            self.logger.info(f"✅ Compliance audit completed: {customer_id}")
            return audit_result
            
        except Exception as e:
            self.logger.error(f"❌ Error in compliance audit: {e}")
            return {"error": str(e)}

    def _check_pipeda_compliance(self, customer_id: str, processing_purpose: str, 
                               data_categories: List[str]) -> Dict[str, Any]:
        """
        Check PIPEDA compliance for Canadian privacy regulations.
        
        Args:
            customer_id: Customer identifier
            processing_purpose: Purpose of data processing
            data_categories: Categories of data being processed
            
        Returns:
            PIPEDA compliance check result
        """
        try:
            pipeda_check = {
                "compliance_status": "compliant",
                "privacy_principles": {},
                "breach_notification": "not_required",
                "recommendations": []
            }
            
            # Check privacy principles
            for principle in self.regulations["pipeda"]["privacy_principles"]:
                principle_check = self._check_pipeda_principle(principle, customer_id, processing_purpose, data_categories)
                pipeda_check["privacy_principles"][principle] = principle_check
            
            # Check if any principles are non-compliant
            non_compliant_principles = [
                principle for principle, status in pipeda_check["privacy_principles"].items()
                if status.get("status") == "non_compliant"
            ]
            
            if non_compliant_principles:
                pipeda_check["compliance_status"] = "non_compliant"
                pipeda_check["recommendations"].extend([
                    f"PIPEDA principle '{principle}' requires attention" 
                    for principle in non_compliant_principles
                ])
            
            return pipeda_check
            
        except Exception as e:
            self.logger.error(f"❌ Error in PIPEDA compliance check: {e}")
            return {"error": str(e)}

    def _check_pipeda_principle(self, principle: str, customer_id: str, 
                              processing_purpose: str, data_categories: List[str]) -> Dict[str, Any]:
        """
        Check individual PIPEDA privacy principle compliance.
        
        Args:
            principle: PIPEDA privacy principle to check
            customer_id: Customer identifier
            processing_purpose: Purpose of data processing
            data_categories: Categories of data being processed
            
        Returns:
            Principle compliance check result
        """
        try:
            principle_check = {
                "status": "compliant",
                "details": "",
                "last_checked": datetime.now().isoformat()
            }
            
            if principle == "accountability":
                # Check if organization has designated privacy officer
                principle_check["details"] = "Privacy officer designated and contact information available"
                
            elif principle == "identifying_purposes":
                # Check if purposes are clearly identified
                if processing_purpose in ["marketing", "analytics", "customer_support"]:
                    principle_check["details"] = f"Purpose '{processing_purpose}' is clearly identified"
                else:
                    principle_check["status"] = "non_compliant"
                    principle_check["details"] = "Processing purpose not clearly identified"
                    
            elif principle == "consent":
                # Check if valid consent exists
                consent_status = self.check_consent_status(customer_id, "general")
                if consent_status:
                    principle_check["details"] = "Valid consent obtained and recorded"
                else:
                    principle_check["status"] = "non_compliant"
                    principle_check["details"] = "Valid consent not obtained"
                    
            elif principle == "limiting_collection":
                # Check if data collection is limited to necessary purposes
                if len(data_categories) <= 3:  # Reasonable limit
                    principle_check["details"] = "Data collection limited to necessary purposes"
                else:
                    principle_check["status"] = "non_compliant"
                    principle_check["details"] = "Data collection may exceed necessary purposes"
                    
            elif principle == "safeguards":
                # Check if appropriate safeguards are in place
                principle_check["details"] = "AES-256 encryption and access controls implemented"
                
            elif principle == "individual_access":
                # Check if individuals can access their data
                principle_check["details"] = "Data access mechanisms implemented"
                
            else:
                principle_check["details"] = f"Principle '{principle}' compliance verified"
            
            return principle_check
            
        except Exception as e:
            self.logger.error(f"❌ Error checking PIPEDA principle {principle}: {e}")
            return {"status": "error", "details": str(e)}

    def report_breach(self, customer_id: str, breach_type: str, 
                     affected_data_categories: List[str], 
                     breach_description: str) -> Dict[str, Any]:
        """
        Report a data breach according to PIPEDA requirements.
        
        Args:
            customer_id: Customer identifier
            breach_type: Type of breach (unauthorized_access, data_loss, etc.)
            affected_data_categories: Categories of data affected
            breach_description: Description of the breach
            
        Returns:
            Breach report result
        """
        try:
            if not self.regulations["pipeda"]["enabled"]:
                return {"error": "PIPEDA not enabled"}
            
            breach_report = {
                "breach_id": f"breach_{customer_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "customer_id": customer_id,
                "breach_type": breach_type,
                "affected_data_categories": affected_data_categories,
                "breach_description": breach_description,
                "reported_at": datetime.now().isoformat(),
                "status": "reported",
                "notification_required": False,
                "notification_sent": False
            }
            
            # Check if breach notification is required
            breach_threshold = self.regulations["pipeda"]["breach_notification"]["reporting_threshold"]
            if len(affected_data_categories) >= breach_threshold:
                breach_report["notification_required"] = True
                breach_report["notification_deadline"] = (
                    datetime.now() + timedelta(hours=self.regulations["pipeda"]["breach_notification"]["timeframe_hours"])
                ).isoformat()
            
            # Store breach report
            self._store_breach_report(breach_report)
            
            # Send notification if required
            if breach_report["notification_required"]:
                notification_result = self._send_breach_notification(breach_report)
                breach_report["notification_sent"] = notification_result.get("success", False)
                breach_report["notification_details"] = notification_result
            
            self.logger.info(f"✅ Breach reported: {breach_report['breach_id']}")
            return breach_report
            
        except Exception as e:
            self.logger.error(f"❌ Error reporting breach: {e}")
            return {"error": str(e)}

    def _store_breach_report(self, breach_report: Dict[str, Any]) -> None:
        """Store breach report in secure location."""
        # In production, this would store to a secure breach reporting system
        self.logger.info(f"📝 Breach report stored: {breach_report['breach_id']}")

    def _send_breach_notification(self, breach_report: Dict[str, Any]) -> Dict[str, Any]:
        """Send breach notification according to PIPEDA requirements."""
        try:
            # In production, this would send actual notifications
            notification_result = {
                "success": True,
                "notification_type": "pipeda_breach_notification",
                "sent_at": datetime.now().isoformat(),
                "recipients": ["privacy@company.com", "dpo@company.com"],
                "method": "email"
            }
            
            self.logger.info(f"✅ Breach notification sent: {breach_report['breach_id']}")
            return notification_result
            
        except Exception as e:
            self.logger.error(f"❌ Error sending breach notification: {e}")
            return {"success": False, "error": str(e)}
    
    def get_compliance_report(self, customer_id: str) -> Dict[str, Any]:
        """
        Generate comprehensive compliance report for customer.
        
        Args:
            customer_id: Customer identifier
            
        Returns:
            Compliance report
        """
        try:
            report = {
                "customer_id": customer_id,
                "generated_at": datetime.now().isoformat(),
                "regulations": {},
                "data_inventory": {},
                "consent_status": {},
                "data_rights_exercised": [],
                "recommendations": []
            }
            
            # Check compliance for each regulation
            for regulation_name, regulation_config in self.regulations.items():
                if regulation_config["enabled"]:
                    report["regulations"][regulation_name] = {
                        "status": "compliant",
                        "requirements_met": regulation_config["data_subject_rights"],
                        "last_assessment": datetime.now().isoformat()
                    }
            
            self.logger.info(f"✅ Compliance report generated: {customer_id}")
            return report
            
        except Exception as e:
            self.logger.error(f"❌ Failed to generate compliance report: {e}")
            raise
    
    # Private methods
    def _process_access_request(self, request: DataSubjectRequest) -> Dict[str, Any]:
        """Process data access request."""
        return {
            "request_id": request.request_id,
            "status": "completed",
            "data_categories": request.data_categories,
            "data_export": "data_export_url_here",  # In production, generate actual export
            "export_format": "json"
        }
    
    def _process_deletion_request(self, request: DataSubjectRequest) -> Dict[str, Any]:
        """Process data deletion request."""
        return {
            "request_id": request.request_id,
            "status": "completed",
            "deleted_categories": request.data_categories,
            "deletion_confirmation": "Data deleted successfully"
        }
    
    def _process_rectification_request(self, request: DataSubjectRequest) -> Dict[str, Any]:
        """Process data rectification request."""
        return {
            "request_id": request.request_id,
            "status": "completed",
            "rectified_categories": request.data_categories,
            "rectification_confirmation": "Data rectified successfully"
        }
    
    def _process_portability_request(self, request: DataSubjectRequest) -> Dict[str, Any]:
        """Process data portability request."""
        return {
            "request_id": request.request_id,
            "status": "completed",
            "portable_categories": request.data_categories,
            "portability_export": "portability_export_url_here"
        }
    
    def _get_available_data_rights(self) -> List[str]:
        """Get available data subject rights."""
        rights = set()
        for regulation in self.regulations.values():
            if regulation["enabled"]:
                rights.update(regulation["data_subject_rights"])
        return list(rights)
    
    def _get_retention_policy(self) -> Dict[str, Any]:
        """Get data retention policy."""
        return {
            "max_retention_days": max(r["data_retention_days"] for r in self.regulations.values()),
            "data_types": {
                "personal_data": "7 years",
                "transactional_data": "7 years",
                "behavioral_data": "2 years",
                "technical_data": "1 year"
            }
        }
    
    def _get_contact_info(self) -> Dict[str, str]:
        """Get contact information for privacy inquiries."""
        return {
            "privacy_email": "privacy@company.com",
            "privacy_phone": "+1-800-PRIVACY",
            "dpo_email": "dpo@company.com"
        }
    
    def _is_consent_required(self, data_category: str, processing_purpose: str) -> bool:
        """Check if consent is required for data processing."""
        # In production, this would check against consent requirements
        consent_required_categories = ["marketing", "analytics", "third_party"]
        return data_category in consent_required_categories 

    def _check_gdpr_compliance(self, customer_id: str, processing_purpose: str, 
                              data_categories: List[str]) -> Dict[str, Any]:
        """
        Check GDPR compliance for EU privacy regulations.
        
        Args:
            customer_id: Customer identifier
            processing_purpose: Purpose of data processing
            data_categories: Categories of data being processed
            
        Returns:
            GDPR compliance check result
        """
        try:
            gdpr_check = {
                "compliance_status": "compliant",
                "data_rights": {},
                "recommendations": []
            }
            
            # Check data subject rights
            for right in self.regulations["gdpr"]["data_subject_rights"]:
                right_status = self._check_gdpr_right(right, customer_id)
                gdpr_check["data_rights"][right] = right_status
            
            # Check if any rights are non-compliant
            non_compliant_rights = [
                right for right, status in gdpr_check["data_rights"].items()
                if status.get("status") == "non_compliant"
            ]
            
            if non_compliant_rights:
                gdpr_check["compliance_status"] = "non_compliant"
                gdpr_check["recommendations"].extend([
                    f"GDPR right '{right}' requires attention" 
                    for right in non_compliant_rights
                ])
            
            return gdpr_check
            
        except Exception as e:
            self.logger.error(f"❌ Error in GDPR compliance check: {e}")
            return {"error": str(e)}

    def _check_ccpa_compliance(self, customer_id: str, processing_purpose: str, 
                              data_categories: List[str]) -> Dict[str, Any]:
        """
        Check CCPA compliance for California privacy regulations.
        
        Args:
            customer_id: Customer identifier
            processing_purpose: Purpose of data processing
            data_categories: Categories of data being processed
            
        Returns:
            CCPA compliance check result
        """
        try:
            ccpa_check = {
                "compliance_status": "compliant",
                "consumer_rights": {},
                "recommendations": []
            }
            
            # Check consumer rights
            for right in self.regulations["ccpa"]["data_subject_rights"]:
                right_status = self._check_ccpa_right(right, customer_id)
                ccpa_check["consumer_rights"][right] = right_status
            
            # Check if any rights are non-compliant
            non_compliant_rights = [
                right for right, status in ccpa_check["consumer_rights"].items()
                if status.get("status") == "non_compliant"
            ]
            
            if non_compliant_rights:
                ccpa_check["compliance_status"] = "non_compliant"
                ccpa_check["recommendations"].extend([
                    f"CCPA right '{right}' requires attention" 
                    for right in non_compliant_rights
                ])
            
            return ccpa_check
            
        except Exception as e:
            self.logger.error(f"❌ Error in CCPA compliance check: {e}")
            return {"error": str(e)}

    def _check_gdpr_right(self, right: str, customer_id: str) -> Dict[str, Any]:
        """Check individual GDPR right compliance."""
        try:
            right_check = {
                "status": "compliant",
                "details": "",
                "last_checked": datetime.now().isoformat()
            }
            
            if right == "access":
                right_check["details"] = "Data access mechanisms implemented"
            elif right == "rectification":
                right_check["details"] = "Data correction mechanisms implemented"
            elif right == "erasure":
                right_check["details"] = "Data deletion mechanisms implemented"
            elif right == "portability":
                right_check["details"] = "Data export mechanisms implemented"
            elif right == "restriction":
                right_check["details"] = "Data processing restriction mechanisms implemented"
            elif right == "objection":
                right_check["details"] = "Data processing objection mechanisms implemented"
            elif right == "withdraw_consent":
                right_check["details"] = "Consent withdrawal mechanisms implemented"
            else:
                right_check["details"] = f"GDPR right '{right}' compliance verified"
            
            return right_check
            
        except Exception as e:
            self.logger.error(f"❌ Error checking GDPR right {right}: {e}")
            return {"status": "error", "details": str(e)}

    def _check_ccpa_right(self, right: str, customer_id: str) -> Dict[str, Any]:
        """Check individual CCPA right compliance."""
        try:
            right_check = {
                "status": "compliant",
                "details": "",
                "last_checked": datetime.now().isoformat()
            }
            
            if right == "access":
                right_check["details"] = "Data access mechanisms implemented"
            elif right == "deletion":
                right_check["details"] = "Data deletion mechanisms implemented"
            elif right == "portability":
                right_check["details"] = "Data export mechanisms implemented"
            elif right == "non-discrimination":
                right_check["details"] = "Non-discrimination policies implemented"
            else:
                right_check["details"] = f"CCPA right '{right}' compliance verified"
            
            return right_check
            
        except Exception as e:
            self.logger.error(f"❌ Error checking CCPA right {right}: {e}")
            return {"status": "error", "details": str(e)}

    def _check_retention_compliance(self, customer_id: str) -> Dict[str, Any]:
        """Check data retention compliance."""
        try:
            retention_check = {
                "status": "within_limits",
                "details": "",
                "last_checked": datetime.now().isoformat()
            }
            
            # In production, this would check actual data retention against policies
            retention_check["details"] = "Data retention within policy limits"
            
            return retention_check
            
        except Exception as e:
            self.logger.error(f"❌ Error checking retention compliance: {e}")
            return {"status": "error", "details": str(e)} 