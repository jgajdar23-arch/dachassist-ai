from typing import Optional, Tuple
from datetime import datetime
from app.domain.models import Lead, Message
from app.storage.lead_storage import LeadStorage


class LeadService:
    """Business logic for lead management"""

    def __init__(self, storage: LeadStorage):
        self.storage = storage

    def create_lead(self, company_id: str) -> Lead:
        """Create new lead"""
        lead = Lead(company_id=company_id)
        self.storage.save_lead(lead)
        return lead

    def get_or_create_lead_from_session(
        self, company_id: str, session_id: str
    ) -> Tuple[Lead, bool]:
        """
        Get existing lead or create new one.
        
        Returns:
            Tuple[Lead, is_new]: Lead object and whether it's newly created
        """
        # For MVP: session_id is used to derive lead_id
        # Later: we'll use a session->lead mapping
        lead_id = f"lead_{session_id.split('_')[1] if '_' in session_id else session_id[:8]}"
        
        existing_lead = self.storage.load_lead(company_id, lead_id)
        if existing_lead:
            return existing_lead, False
        
        new_lead = Lead(id=lead_id, company_id=company_id)
        self.storage.save_lead(new_lead)
        return new_lead, True

    def add_user_message(
        self, lead: Lead, message: str
    ) -> None:
        """Add user message to conversation"""
        msg = Message(
            timestamp=datetime.utcnow(),
            role="user",
            message=message
        )
        lead.conversation.append(msg)

    def add_assistant_message(
        self, lead: Lead, message: str
    ) -> None:
        """Add assistant message to conversation"""
        msg = Message(
            timestamp=datetime.utcnow(),
            role="assistant",
            message=message
        )
        lead.conversation.append(msg)

    def save_lead(self, lead: Lead) -> None:
        """Persist lead to storage"""
        self.storage.save_lead(lead)
