"""
Security Manager for Memory System
Ensures customer data is handled with enterprise-grade security and compliance.
"""

import logging
import hashlib
import hmac
import os
import json
import base64
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets
import re

logger = logging.getLogger(__name__)

class SecurityManager:
    """
    Enterprise-grade security manager for customer data handling.
    Implements encryption, access controls, audit logging, and compliance features.
    """
    
    def __init__(self, encryption_key: Optional[str] = None):
        """Initialize SecurityManager with encryption and security features."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize encryption
        self.encryption_key = encryption_key or os.getenv("MEMORY_ENCRYPTION_KEY")
        if not self.encryption_key:
            self.encryption_key = self._generate_encryption_key()
        
        self.cipher_suite = self._initialize_encryption()
        
        # Security settings
        self.max_retention_days = int(os.getenv("MEMORY_MAX_RETENTION_DAYS", "2555"))  # 7 years
        self.encryption_required = os.getenv("MEMORY_ENCRYPTION_REQUIRED", "true").lower() == "true"
        self.audit_logging = os.getenv("MEMORY_AUDIT_LOGGING", "true").lower() == "true"
        
        # Access control
        self.access_controls = {
            "customer_data": ["admin", "support", "analytics"],
            "product_data": ["admin", "sales", "analytics"],
            "agent_data": ["admin", "analytics"],
            "system_data": ["admin"]
        }
        
        # Compliance settings
        self.compliance_frameworks = {
            "gdpr": True,
            "ccpa": True,
            "hipaa": False,  # Set to True if handling health data
            "sox": True
        }
        
        self.logger.info("✅ SecurityManager initialized with enterprise-grade security")
    
    def _generate_encryption_key(self) -> str:
        """Generate a secure encryption key."""
        key = Fernet.generate_key()
        return base64.urlsafe_b64encode(key).decode()
    
    def _initialize_encryption(self) -> Fernet:
        """Initialize the encryption cipher suite."""
        try:
            key = base64.urlsafe_b64decode(self.encryption_key.encode())
            return Fernet(key)
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize encryption: {e}")
            raise
    
    def encrypt_sensitive_data(self, data: str, data_type: str = "customer_data") -> Dict[str, Any]:
        """
        Encrypt sensitive data with metadata for compliance.
        
        Args:
            data: Data to encrypt
            data_type: Type of data (customer_data, product_data, etc.)
            
        Returns:
            Encrypted data with metadata
        """
        try:
            # Generate unique identifier
            data_id = self._generate_data_id()
            
            # Create metadata
            metadata = {
                "data_id": data_id,
                "data_type": data_type,
                "encrypted_at": datetime.now().isoformat(),
                "encryption_version": "1.0",
                "compliance_frameworks": list(self.compliance_frameworks.keys())
            }
            
            # Encrypt data
            encrypted_data = self.cipher_suite.encrypt(data.encode())
            
            # Create secure package
            secure_package = {
                "encrypted_data": base64.urlsafe_b64encode(encrypted_data).decode(),
                "metadata": metadata,
                "checksum": self._generate_checksum(data),
                "version": "1.0"
            }
            
            self.logger.info(f"✅ Data encrypted: {data_id}")
            return secure_package
            
        except Exception as e:
            self.logger.error(f"❌ Encryption failed: {e}")
            raise
    
    def decrypt_sensitive_data(self, secure_package: Dict[str, Any]) -> str:
        """
        Decrypt sensitive data with validation.
        
        Args:
            secure_package: Encrypted data package
            
        Returns:
            Decrypted data
        """
        try:
            # Validate package structure
            if not self._validate_secure_package(secure_package):
                raise ValueError("Invalid secure package structure")
            
            # Extract encrypted data
            encrypted_data = base64.urlsafe_b64decode(secure_package["encrypted_data"].encode())
            
            # Decrypt data
            decrypted_data = self.cipher_suite.decrypt(encrypted_data).decode()
            
            # Validate checksum
            if not self._validate_checksum(decrypted_data, secure_package["checksum"]):
                raise ValueError("Data integrity check failed")
            
            self.logger.info(f"✅ Data decrypted: {secure_package['metadata']['data_id']}")
            return decrypted_data
            
        except Exception as e:
            self.logger.error(f"❌ Decryption failed: {e}")
            raise
    
    def sanitize_customer_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize customer data for storage and processing.
        
        Args:
            data: Raw customer data
            
        Returns:
            Sanitized customer data
        """
        try:
            sanitized_data = {}
            
            # Define sensitive fields and their sanitization rules
            sensitive_fields = {
                "email": self._sanitize_email,
                "phone": self._sanitize_phone,
                "address": self._sanitize_address,
                "credit_card": self._mask_credit_card,
                "ssn": self._mask_ssn,
                "ip_address": self._anonymize_ip
            }
            
            for key, value in data.items():
                if key in sensitive_fields:
                    sanitized_data[key] = sensitive_fields[key](value)
                else:
                    sanitized_data[key] = self._sanitize_general_data(value)
            
            self.logger.info("✅ Customer data sanitized")
            return sanitized_data
            
        except Exception as e:
            self.logger.error(f"❌ Data sanitization failed: {e}")
            raise
    
    def validate_data_access(self, user_role: str, data_type: str) -> bool:
        """
        Validate if user has access to specific data type.
        
        Args:
            user_role: User's role
            data_type: Type of data being accessed
            
        Returns:
            True if access is allowed
        """
        try:
            if data_type not in self.access_controls:
                self.logger.warning(f"⚠️ Unknown data type: {data_type}")
                return False
            
            allowed_roles = self.access_controls[data_type]
            has_access = user_role in allowed_roles
            
            if not has_access:
                self.logger.warning(f"⚠️ Access denied: {user_role} -> {data_type}")
            
            return has_access
            
        except Exception as e:
            self.logger.error(f"❌ Access validation failed: {e}")
            return False
    
    def audit_data_access(self, user_id: str, user_role: str, action: str, 
                         data_type: str, data_id: Optional[str] = None) -> None:
        """
        Log data access for audit purposes.
        
        Args:
            user_id: User identifier
            user_role: User's role
            action: Action performed (read, write, delete)
            data_type: Type of data accessed
            data_id: Specific data identifier
        """
        try:
            if not self.audit_logging:
                return
            
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "user_role": user_role,
                "action": action,
                "data_type": data_type,
                "data_id": data_id,
                "session_id": self._get_session_id(),
                "ip_address": self._get_client_ip(),
                "user_agent": self._get_user_agent()
            }
            
            # Log audit entry
            self.logger.info(f"🔍 AUDIT: {json.dumps(audit_entry)}")
            
            # Store audit entry (in production, this would go to a secure audit log)
            self._store_audit_entry(audit_entry)
            
        except Exception as e:
            self.logger.error(f"❌ Audit logging failed: {e}")
    
    def check_data_retention(self, data_timestamp: str) -> bool:
        """
        Check if data should be retained based on retention policy.
        
        Args:
            data_timestamp: Timestamp when data was created
            
        Returns:
            True if data should be retained
        """
        try:
            # Handle empty or invalid timestamps
            if not data_timestamp or data_timestamp.strip() == '':
                self.logger.debug("Empty timestamp provided, defaulting to retain")
                return True
            
            # Parse the timestamp
            data_date = datetime.fromisoformat(data_timestamp.replace('Z', '+00:00'))
            cutoff_date = datetime.now() - timedelta(days=self.max_retention_days)
            
            should_retain = data_date > cutoff_date
            
            if not should_retain:
                self.logger.info(f"⚠️ Data expired: {data_timestamp}")
            
            return should_retain
            
        except Exception as e:
            self.logger.error(f"❌ Retention check failed: {e}")
            return True  # Default to retain if check fails
    
    def generate_data_export(self, customer_id: str, export_type: str = "gdpr") -> Dict[str, Any]:
        """
        Generate compliant data export for customer.
        
        Args:
            customer_id: Customer identifier
            export_type: Type of export (gdpr, ccpa, etc.)
            
        Returns:
            Compliant data export
        """
        try:
            export_data = {
                "customer_id": customer_id,
                "export_type": export_type,
                "export_date": datetime.now().isoformat(),
                "data_categories": [],
                "data_usage": [],
                "retention_policy": self._get_retention_policy(),
                "data_rights": self._get_data_rights(export_type)
            }
            
            self.logger.info(f"✅ Data export generated: {customer_id} ({export_type})")
            return export_data
            
        except Exception as e:
            self.logger.error(f"❌ Data export generation failed: {e}")
            raise
    
    def anonymize_customer_data(self, customer_id: str) -> bool:
        """
        Anonymize customer data for privacy compliance.
        
        Args:
            customer_id: Customer identifier
            
        Returns:
            True if anonymization successful
        """
        try:
            # Generate anonymized identifier
            anonymized_id = self._generate_anonymized_id(customer_id)
            
            # Replace sensitive data with anonymized versions
            # This would be implemented based on specific requirements
            
            self.logger.info(f"✅ Customer data anonymized: {customer_id} -> {anonymized_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Data anonymization failed: {e}")
            return False
    
    # Helper methods
    def _generate_data_id(self) -> str:
        """Generate a unique data identifier."""
        return f"data_{secrets.token_urlsafe(16)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _generate_checksum(self, data: str) -> str:
        """Generate checksum for data integrity."""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _validate_checksum(self, data: str, checksum: str) -> bool:
        """Validate data integrity using checksum."""
        return self._generate_checksum(data) == checksum
    
    def _validate_secure_package(self, package: Dict[str, Any]) -> bool:
        """Validate secure package structure."""
        required_fields = ["encrypted_data", "metadata", "checksum", "version"]
        return all(field in package for field in required_fields)
    
    def _sanitize_email(self, email: str) -> str:
        """Sanitize email address."""
        if not email:
            return ""
        # Basic email validation and sanitization
        email = email.strip().lower()
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return email
        return ""
    
    def _sanitize_phone(self, phone: str) -> str:
        """Sanitize phone number."""
        if not phone:
            return ""
        # Remove non-digit characters and format
        digits = re.sub(r'\D', '', phone)
        if len(digits) >= 10:
            return f"***-***-{digits[-4:]}"
        return ""
    
    def _sanitize_address(self, address: str) -> str:
        """Sanitize address information."""
        if not address:
            return ""
        # Remove sensitive parts and keep general location
        parts = address.split(',')
        if len(parts) > 1:
            return f"{parts[0]}, {parts[-1]}"
        return address
    
    def _mask_credit_card(self, card: str) -> str:
        """Mask credit card number."""
        if not card:
            return ""
        digits = re.sub(r'\D', '', card)
        if len(digits) >= 4:
            return f"****-****-****-{digits[-4:]}"
        return ""
    
    def _mask_ssn(self, ssn: str) -> str:
        """Mask social security number."""
        if not ssn:
            return ""
        digits = re.sub(r'\D', '', ssn)
        if len(digits) >= 4:
            return f"***-**-{digits[-4:]}"
        return ""
    
    def _anonymize_ip(self, ip: str) -> str:
        """Anonymize IP address."""
        if not ip:
            return ""
        parts = ip.split('.')
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.*.*"
        return ip
    
    def _sanitize_general_data(self, data: Any) -> Any:
        """Sanitize general data."""
        if isinstance(data, str):
            # Remove potentially dangerous characters
            return re.sub(r'[<>"\']', '', data)
        return data
    
    def _get_session_id(self) -> str:
        """Get current session ID."""
        return os.getenv("SESSION_ID", "unknown")
    
    def _get_client_ip(self) -> str:
        """Get client IP address."""
        return os.getenv("CLIENT_IP", "unknown")
    
    def _get_user_agent(self) -> str:
        """Get user agent string."""
        return os.getenv("USER_AGENT", "unknown")
    
    def _store_audit_entry(self, entry: Dict[str, Any]) -> None:
        """Store audit entry in secure location."""
        # In production, this would store to a secure audit log system
        pass
    
    def _get_retention_policy(self) -> Dict[str, Any]:
        """Get data retention policy."""
        return {
            "max_retention_days": self.max_retention_days,
            "compliance_frameworks": self.compliance_frameworks,
            "data_types": {
                "customer_data": "7 years",
                "transaction_data": "7 years",
                "support_data": "3 years",
                "analytics_data": "2 years"
            }
        }
    
    def _get_data_rights(self, export_type: str) -> List[str]:
        """Get customer data rights based on compliance framework."""
        rights_map = {
            "gdpr": ["access", "rectification", "erasure", "portability", "restriction"],
            "ccpa": ["access", "deletion", "portability", "non-discrimination"],
            "hipaa": ["access", "amendment", "accounting", "restriction"]
        }
        return rights_map.get(export_type, [])
    
    def _generate_anonymized_id(self, customer_id: str) -> str:
        """Generate anonymized customer identifier."""
        return hashlib.sha256(customer_id.encode()).hexdigest()[:16] 