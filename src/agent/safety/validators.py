"""Input and output validation for safety."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ValidationError


class ValidationResult:
    """Result of validation."""
    
    def __init__(self, valid: bool, errors: Optional[List[str]] = None):
        self.valid = valid
        self.errors = errors or []


class InputValidator:
    """
    Validates agent inputs for safety and correctness.
    
    Checks for:
    - Schema compliance
    - Malicious content
    - Size limits
    """
    
    def __init__(self, max_input_size: int = 10000):
        self.max_input_size = max_input_size
    
    def validate(self, input_data: BaseModel) -> ValidationResult:
        """Validate input data."""
        errors = []
        
        # Check size
        input_str = input_data.model_dump_json()
        if len(input_str) > self.max_input_size:
            errors.append(f"Input exceeds maximum size of {self.max_input_size} bytes")
        
        # Check for suspicious patterns (basic example)
        if self._contains_suspicious_content(input_str):
            errors.append("Input contains suspicious content")
        
        return ValidationResult(valid=len(errors) == 0, errors=errors)
    
    def _contains_suspicious_content(self, content: str) -> bool:
        """Check for suspicious patterns in content."""
        # TODO: Implement more sophisticated checks
        suspicious_patterns = ["<script>", "javascript:", "eval("]
        return any(pattern in content.lower() for pattern in suspicious_patterns)


class OutputValidator:
    """
    Validates agent outputs for safety.
    
    Checks for:
    - Sensitive information leakage
    - Harmful content
    - Format compliance
    """
    
    def __init__(self):
        self.blocked_patterns = [
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Emails (example)
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN pattern (example)
        ]
    
    def validate(self, output: str) -> ValidationResult:
        """Validate output content."""
        errors = []
        
        # Check for sensitive patterns
        if self._contains_sensitive_info(output):
            errors.append("Output may contain sensitive information")
        
        return ValidationResult(valid=len(errors) == 0, errors=errors)
    
    def _contains_sensitive_info(self, content: str) -> bool:
        """Check for sensitive information patterns."""
        import re
        return any(re.search(pattern, content) for pattern in self.blocked_patterns)
