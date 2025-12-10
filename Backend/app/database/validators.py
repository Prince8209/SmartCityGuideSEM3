"""
Data Validators
Validation functions for database records
"""

import re
from datetime import datetime


class ValidationError(Exception):
    """Exception raised for validation errors"""
    pass


class Validator:
    """
    Data validation utilities
    Demonstrates: validation, regex, type checking
    """
    
    @staticmethod
    def required(value, field_name="Field"):
        """
        Validate that value is not None or empty
        Raises ValidationError if invalid
        """
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationError(f"{field_name} is required")
        return value
    
    @staticmethod
    def email(value, field_name="Email"):
        """Validate email format"""
        if not value:
            raise ValidationError(f"{field_name} is required")
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise ValidationError(f"{field_name} must be a valid email address")
        
        return value
    
    @staticmethod
    def min_length(value, min_len, field_name="Field"):
        """Validate minimum string length"""
        if not value or len(str(value)) < min_len:
            raise ValidationError(f"{field_name} must be at least {min_len} characters")
        return value
    
    @staticmethod
    def max_length(value, max_len, field_name="Field"):
        """Validate maximum string length"""
        if value and len(str(value)) > max_len:
            raise ValidationError(f"{field_name} must be at most {max_len} characters")
        return value
    
    @staticmethod
    def min_value(value, min_val, field_name="Field"):
        """Validate minimum numeric value"""
        if value is not None and value < min_val:
            raise ValidationError(f"{field_name} must be at least {min_val}")
        return value
    
    @staticmethod
    def max_value(value, max_val, field_name="Field"):
        """Validate maximum numeric value"""
        if value is not None and value > max_val:
            raise ValidationError(f"{field_name} must be at most {max_val}")
        return value
    
    @staticmethod
    def in_range(value, min_val, max_val, field_name="Field"):
        """Validate value is in range"""
        if value is not None and not (min_val <= value <= max_val):
            raise ValidationError(f"{field_name} must be between {min_val} and {max_val}")
        return value
    
    @staticmethod
    def one_of(value, choices, field_name="Field"):
        """Validate value is one of allowed choices"""
        if value not in choices:
            raise ValidationError(f"{field_name} must be one of: {', '.join(map(str, choices))}")
        return value
    
    @staticmethod
    def is_type(value, expected_type, field_name="Field"):
        """Validate value type"""
        if value is not None and not isinstance(value, expected_type):
            raise ValidationError(f"{field_name} must be of type {expected_type.__name__}")
        return value
    
    @staticmethod
    def is_int(value, field_name="Field"):
        """Validate integer"""
        return Validator.is_type(value, int, field_name)
    
    @staticmethod
    def is_float(value, field_name="Field"):
        """Validate float"""
        return Validator.is_type(value, (int, float), field_name)
    
    @staticmethod
    def is_string(value, field_name="Field"):
        """Validate string"""
        return Validator.is_type(value, str, field_name)
    
    @staticmethod
    def is_bool(value, field_name="Field"):
        """Validate boolean"""
        return Validator.is_type(value, bool, field_name)
    
    @staticmethod
    def is_dict(value, field_name="Field"):
        """Validate dictionary"""
        return Validator.is_type(value, dict, field_name)
    
    @staticmethod
    def is_list(value, field_name="Field"):
        """Validate list"""
        return Validator.is_type(value, list, field_name)
    
    @staticmethod
    def pattern(value, regex_pattern, field_name="Field"):
        """Validate against regex pattern"""
        if value and not re.match(regex_pattern, str(value)):
            raise ValidationError(f"{field_name} format is invalid")
        return value
    
    @staticmethod
    def url(value, field_name="URL"):
        """Validate URL format"""
        if not value:
            return value
        
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if not re.match(pattern, value):
            raise ValidationError(f"{field_name} must be a valid URL")
        return value
    
    @staticmethod
    def phone(value, field_name="Phone"):
        """Validate phone number (Indian format)"""
        if not value:
            return value
        
        # Remove spaces and dashes
        cleaned = re.sub(r'[\s\-()]', '', value)
        
        # Check for valid Indian phone number
        pattern = r'^(\+91)?[6-9]\d{9}$'
        if not re.match(pattern, cleaned):
            raise ValidationError(f"{field_name} must be a valid phone number")
        
        return value
    
    @staticmethod
    def date_string(value, field_name="Date"):
        """Validate ISO date string"""
        if not value:
            return value
        
        try:
            datetime.fromisoformat(value)
            return value
        except ValueError:
            raise ValidationError(f"{field_name} must be a valid ISO date string")
    
    @staticmethod
    def validate_record(record, schema):
        """
        Validate record against schema
        Demonstrates: dictionary iteration, validation chaining
        
        Args:
            record: Dictionary to validate
            schema: Dictionary of {field: [validators]}
        
        Example:
            schema = {
                'email': [Validator.required, Validator.email],
                'age': [lambda v: Validator.in_range(v, 0, 150, 'Age')]
            }
        """
        errors = {}
        
        for field, validators in schema.items():
            value = record.get(field)
            
            try:
                for validator in validators:
                    value = validator(value)
            except ValidationError as e:
                errors[field] = str(e)
        
        if errors:
            raise ValidationError(f"Validation failed: {errors}")
        
        return True


class ModelValidator:
    """
    Base class for model-specific validators
    Demonstrates: inheritance, OOP
    """
    
    def __init__(self, data):
        self.data = data
        self.errors = {}
    
    def validate(self):
        """
        Override this method in subclasses
        Should return True if valid, False otherwise
        """
        raise NotImplementedError("Subclasses must implement validate()")
    
    def add_error(self, field, message):
        """Add validation error"""
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)
    
    def is_valid(self):
        """Check if validation passed"""
        return len(self.errors) == 0
    
    def get_errors(self):
        """Get all validation errors"""
        return self.errors
