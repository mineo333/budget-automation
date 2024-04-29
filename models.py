from pydantic import BaseModel
from typing import List, Optional
from enum import StrEnum


class Submission(BaseModel):
    """submission form"""

    form_date: str
    last_name: str
    first_name: str
    purchase_date: str
    contact_email: str
    vendor_name: str
    purchased_items: List[str]
    card_purchase: str
    cash_purchase: str
    csec_card: str
    gci_card: str
    refund: str
    yes_tax: str
    no_tax: str
    denied_tax: str
    refund_date: str
    purchase_reason: str
    attendance_list: str
    image: str


class ErrorType(StrEnum):
    """Error types. TODO: Add more error types
    and better handle existing errors"""

    FILE_ERROR = "file_error"
    COMPILE_ERROR = "compile_error"
    UPLOAD_ERROR = "upload_error"
    INVALID_IMG = "invalid_image"


class SubmissionResponse(BaseModel):
    """submission response"""

    gdrive_link: Optional[str] = None
    error: Optional[ErrorType] = None
