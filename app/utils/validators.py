import re
import httpx
from typing import Optional

def validate_gst_number(gst_number: str) -> bool:
    """Validate GST number format"""
    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    return bool(re.match(pattern, gst_number))

async def verify_gst_number(gst_number: str) -> dict:
    """Mock GST verification - replace with actual API call"""
    if not validate_gst_number(gst_number):
        return {"valid": False, "message": "Invalid GST format"}
    
    # Mock response - in production, use actual GST verification API
    return {
        "valid": True,
        "company_name": "Mock Company Name",
        "status": "Active"
    }

def validate_phone_number(phone: str) -> bool:
    """Validate Indian phone number"""
    pattern = r'^(\+91|91)?[6-9]\d{9}$'
    return bool(re.match(pattern, phone))
