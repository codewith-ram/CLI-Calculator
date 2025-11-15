"""
Input validation utilities for SmartDine Desktop Edition
"""
import re
from typing import Any, Optional


class Validators:
    """Collection of validation methods"""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """Validate phone number format"""
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        # Check if it's 10 digits (US format) or 11 digits (with country code)
        return len(digits_only) in [10, 11]
    
    @staticmethod
    def is_valid_price(price: Any) -> bool:
        """Validate price (must be positive number)"""
        try:
            price_float = float(price)
            return price_float >= 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_quantity(quantity: Any) -> bool:
        """Validate quantity (must be positive integer)"""
        try:
            quantity_int = int(quantity)
            return quantity_int > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_username(username: str) -> bool:
        """Validate username format (alphanumeric and underscore only)"""
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def is_valid_password(password: str) -> bool:
        """Validate password strength"""
        # At least 6 characters, contains at least one letter and one number
        if len(password) < 6:
            return False
        
        has_letter = bool(re.search(r'[a-zA-Z]', password))
        has_number = bool(re.search(r'\d', password))
        
        return has_letter and has_number
    
    @staticmethod
    def is_valid_table_number(table_number: Any) -> bool:
        """Validate table number (positive integer)"""
        try:
            table_int = int(table_number)
            return table_int > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_capacity(capacity: Any) -> bool:
        """Validate table capacity (positive integer between 1 and 20)"""
        try:
            capacity_int = int(capacity)
            return 1 <= capacity_int <= 20
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_percentage(percentage: Any) -> bool:
        """Validate percentage (0-100)"""
        try:
            percent_float = float(percentage)
            return 0 <= percent_float <= 100
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def sanitize_string(text: str) -> str:
        """Sanitize string input (remove dangerous characters)"""
        if not isinstance(text, str):
            return str(text)
        
        # Remove or replace potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', text)
        return sanitized.strip()
    
    @staticmethod
    def validate_menu_item_data(data: dict) -> tuple[bool, str]:
        """Validate menu item data"""
        required_fields = ['name', 'price', 'category']
        
        # Check required fields
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Missing required field: {field}"
        
        # Validate name
        if len(data['name'].strip()) < 2:
            return False, "Name must be at least 2 characters long"
        
        # Validate price
        if not Validators.is_valid_price(data['price']):
            return False, "Price must be a valid positive number"
        
        # Validate category
        valid_categories = ['starters', 'main_course', 'desserts', 'beverages']
        if data['category'] not in valid_categories:
            return False, f"Category must be one of: {', '.join(valid_categories)}"
        
        return True, "Valid"
    
    @staticmethod
    def validate_user_data(data: dict) -> tuple[bool, str]:
        """Validate user data"""
        required_fields = ['username', 'password', 'role', 'full_name']
        
        # Check required fields
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Missing required field: {field}"
        
        # Validate username
        if not Validators.is_valid_username(data['username']):
            return False, "Username must be 3-20 characters, alphanumeric and underscore only"
        
        # Validate password
        if not Validators.is_valid_password(data['password']):
            return False, "Password must be at least 6 characters with letters and numbers"
        
        # Validate role
        valid_roles = ['admin', 'waiter', 'chef', 'cashier']
        if data['role'] not in valid_roles:
            return False, f"Role must be one of: {', '.join(valid_roles)}"
        
        # Validate full name
        if len(data['full_name'].strip()) < 2:
            return False, "Full name must be at least 2 characters long"
        
        return True, "Valid"


# Global validators instance
validators = Validators()
