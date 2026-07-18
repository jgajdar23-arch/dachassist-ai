from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
import uuid


class Message(BaseModel):
    """Single message in conversation"""
    timestamp: datetime
    role: str  # "user" or "assistant"
    message: str


class Contact(BaseModel):
    """Customer contact information"""
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class Inquiry(BaseModel):
    """Customer inquiry details"""
    type: Optional[str] = None
    summary: Optional[str] = None
    urgency: Optional[str] = None
    is_emergency: bool = False


class Lead(BaseModel):
    """Lead/customer conversation record"""
    id: str = Field(default_factory=lambda: f"lead_{uuid.uuid4().hex[:8]}")
    company_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    contact: Contact = Field(default_factory=Contact)
    inquiry: Inquiry = Field(default_factory=Inquiry)
    conversation: List[Message] = Field(default_factory=list)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ChatRequest(BaseModel):
    """Chat API request"""
    company_id: str
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat API response"""
    reply: str
    session_id: str
    lead_id: str
