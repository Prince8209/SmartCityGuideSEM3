"""
Custom Exceptions
Application-specific exception classes
"""


class SmartCityException(Exception):
    """Base exception for Smart City Guide application"""
    pass


class DatabaseException(SmartCityException):
    """Database-related exceptions"""
    pass


class ValidationException(SmartCityException):
    """Data validation exceptions"""
    pass


class AuthenticationException(SmartCityException):
    """Authentication-related exceptions"""
    pass


class AuthorizationException(SmartCityException):
    """Authorization-related exceptions"""
    pass


class RecordNotFoundException(DatabaseException):
    """Exception raised when a record is not found"""
    pass


class DuplicateRecordException(DatabaseException):
    """Exception raised when trying to create a duplicate record"""
    pass


class InvalidTokenException(AuthenticationException):
    """Exception raised for invalid JWT tokens"""
    pass


class TokenExpiredException(AuthenticationException):
    """Exception raised for expired JWT tokens"""
    pass
