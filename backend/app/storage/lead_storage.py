import json
import os
from pathlib import Path
from typing import Optional
from datetime import datetime
from app.domain.models import Lead


class LeadStorage:
    """Handle Lead persistence to JSON files"""

    def __init__(self, base_path: str = "customers"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    def _get_company_leads_dir(self, company_id: str) -> Path:
        """Get leads directory for company"""
        leads_dir = self.base_path / company_id / "leads"
        leads_dir.mkdir(parents=True, exist_ok=True)
        return leads_dir

    def _get_lead_file_path(self, company_id: str, lead_id: str) -> Path:
        """Get full path to lead JSON file"""
        leads_dir = self._get_company_leads_dir(company_id)
        return leads_dir / f"{lead_id}.json"

    def save_lead(self, lead: Lead) -> None:
        """Save lead to JSON file"""
        file_path = self._get_lead_file_path(lead.company_id, lead.id)
        
        # Update timestamp
        lead.updated_at = datetime.utcnow()
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(lead.dict(), f, indent=2, default=str)

    def load_lead(self, company_id: str, lead_id: str) -> Optional[Lead]:
        """Load lead from JSON file"""
        file_path = self._get_lead_file_path(company_id, lead_id)
        
        if not file_path.exists():
            return None
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Convert datetime strings back to datetime objects
        if isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        
        # Convert conversation messages
        for msg in data["conversation"]:
            if isinstance(msg["timestamp"], str):
                msg["timestamp"] = datetime.fromisoformat(msg["timestamp"])
        
        return Lead(**data)

    def lead_exists(self, company_id: str, lead_id: str) -> bool:
        """Check if lead file exists"""
        file_path = self._get_lead_file_path(company_id, lead_id)
        return file_path.exists()
