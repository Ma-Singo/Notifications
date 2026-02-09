"""
Template Domain Model

This is a PURE domain entity - no database dependencies, no external dependencies.
It contains only business logic about what a Template IS and what rules it must follow.

Following SOLID principles:
- Single Responsibility: Only defines Template business rules
- No dependencies on infrastructure (SQLAlchemy, FastAPI, etc.)
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional
from enum import Enum


class TemplateChannel(str, Enum):
    """Notification channels that a template can be used for"""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class Template:
    """
    Template Domain Entity
    
    Represents a reusable notification template with variable substitution.
    
    Business Rules:
    1. Template name must be unique per user
    2. Template must have at least one channel
    3. Subject is required for email templates
    4. Body cannot be empty
    5. Variables in body must be valid placeholders (e.g., {{username}}, {{amount}})
    """
    
    def __init__(
        self,
        name: str,
        channel: TemplateChannel,
        body: str,
        user_id: int,
        subject: Optional[str] = None,
        variables: Optional[Dict[str, str]] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        is_active: bool = True
    ):
        self.id = id
        self.name = name
        self.channel = channel
        self.subject = subject
        self.body = body
        self.user_id = user_id
        self.variables = variables or {}
        self.is_active = is_active
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)
        
        # Validate on creation
        self._validate()
    
    def _validate(self) -> None:
        """
        Enforce business rules
        
        This is where domain logic lives - NOT in the database layer
        """
        if not self.name or not self.name.strip():
            raise ValueError("Template name cannot be empty")
        
        if not self.body or not self.body.strip():
            raise ValueError("Template body cannot be empty")
        
        if self.channel == TemplateChannel.EMAIL and not self.subject:
            raise ValueError("Email templates must have a subject")
        
        if len(self.name) > 100:
            raise ValueError("Template name cannot exceed 100 characters")
    
    def render(self, variables: Dict[str, Any]) -> Dict[str, str]:
        """
        Render the template with provided variables
        
        Example:
            template.body = "Hello {{name}}, your balance is {{amount}}"
            variables = {"name": "Josh", "amount": "$100"}
            result = template.render(variables)
            # result["body"] = "Hello Josh, your balance is $100"
        
        Args:
            variables: Dictionary of variable names to values
            
        Returns:
            Dictionary with rendered 'subject' and 'body'
            
        Raises:
            ValueError: If required variables are missing
        """
        # Check for missing required variables
        missing_vars = self._get_missing_variables(variables)
        if missing_vars:
            raise ValueError(f"Missing required variables: {', '.join(missing_vars)}")
        
        # Render body
        rendered_body = self.body
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"  # {{variable_name}}
            rendered_body = rendered_body.replace(placeholder, str(value))
        
        # Render subject (if email)
        rendered_subject = None
        if self.subject:
            rendered_subject = self.subject
            for key, value in variables.items():
                placeholder = f"{{{{{key}}}}}"
                rendered_subject = rendered_subject.replace(placeholder, str(value))
        
        return {
            "subject": rendered_subject,
            "body": rendered_body
        }
    
    def _get_missing_variables(self, provided_vars: Dict[str, Any]) -> list[str]:
        """
        Extract required variables from template and check which ones are missing
        
        Example:
            body = "Hello {{name}}, you have {{count}} messages"
            provided_vars = {"name": "Josh"}
            # Returns: ["count"]
        """
        import re
        
        # Find all {{variable}} patterns in body and subject
        text_to_check = self.body
        if self.subject:
            text_to_check += " " + self.subject
        
        # Regex to find {{variable_name}} patterns
        pattern = r'\{\{(\w+)\}\}'
        required_vars = set(re.findall(pattern, text_to_check))
        
        # Check which required variables are missing
        provided_keys = set(provided_vars.keys())
        missing = required_vars - provided_keys
        
        return list(missing)
    
    def update(
        self,
        name: Optional[str] = None,
        subject: Optional[str] = None,
        body: Optional[str] = None,
        variables: Optional[Dict[str, str]] = None,
        is_active: Optional[bool] = None
    ) -> None:
        """
        Update template fields and re-validate
        
        This ensures business rules are always enforced
        """
        if name is not None:
            self.name = name
        if subject is not None:
            self.subject = subject
        if body is not None:
            self.body = body
        if variables is not None:
            self.variables = variables
        if is_active is not None:
            self.is_active = is_active
        
        self.updated_at = datetime.now(timezone.utc)
        self._validate()
    
    def deactivate(self) -> None:
        """Soft delete - mark template as inactive"""
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)
    
    def activate(self) -> None:
        """Reactivate a deactivated template"""
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)
    
    def __repr__(self) -> str:
        return f"<Template(id={self.id}, name='{self.name}', channel={self.channel.value})>"
    
    def __str__(self) -> str:
        return f"Template: {self.name} ({self.channel.value})"
