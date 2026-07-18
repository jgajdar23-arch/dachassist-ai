import uuid
from fastapi import APIRouter, HTTPException
from app.domain.models import ChatRequest, ChatResponse
from app.services.lead_service import LeadService
from app.storage.lead_storage import LeadStorage
from app.infrastructure.llm.openai_client import OpenAIClient
from app.core.config import settings

router = APIRouter(prefix="/api", tags=["chat"])

# Initialize services
lead_storage = LeadStorage()
lead_service = LeadService(lead_storage)
llm_client = OpenAIClient(api_key=settings.openai_api_key)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint with session and lead management.
    
    First request: session_id = null → creates new session and lead
    Follow-up requests: includes session_id → loads existing lead
    """
    
    # Validate company exists
    company_config_path = f"customers/{request.company_id}/config.json"
    # TODO: Add proper company validation
    
    # Generate or use existing session_id
    if not request.session_id:
        session_id = f"session_{uuid.uuid4().hex[:12]}"
        lead, _ = lead_service.create_lead(request.company_id)
    else:
        session_id = request.session_id
        # Extract lead_id from session_id or use mapping
        lead_id = f"lead_{session_id.split('_')[1][:8]}"
        lead = lead_storage.load_lead(request.company_id, lead_id)
        
        if not lead:
            raise HTTPException(
                status_code=404,
                detail=f"Lead not found for session {session_id}"
            )
    
    # Add user message to conversation
    lead_service.add_user_message(lead, request.message)
    
    # Get response from OpenAI
    # For MVP: simple chat, no KB or system prompt yet
    system_prompt = "Du bist ein hilfreicher Kundenservice-Agent für einen Handwerksbetrieb. Antworte kurz und professionell auf Deutsch."
    
    try:
        response_text = llm_client.chat(
            system_prompt=system_prompt,
            messages=[
                {"role": "user", "content": request.message}
            ]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI API error: {str(e)}"
        )
    
    # Add assistant message to conversation
    lead_service.add_assistant_message(lead, response_text)
    
    # Save lead
    lead_service.save_lead(lead)
    
    return ChatResponse(
        reply=response_text,
        session_id=session_id,
        lead_id=lead.id
    )
