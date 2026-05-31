from fastapi import APIRouter, Request, HTTPException
import stripe
from app.config import STRIPE_WEBHOOK_SECRET
from app.database import supabase

router = APIRouter()

@router.post("/stripe", summary="Stripe Webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except stripe.errors.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Save to database
    supabase.table("events").insert({
        "event_id": event["id"],
        "event_type": event["type"],
        "source": "stripe",
        "payload": event["data"]["object"].to_dict(),
        "status": "received"
    }).execute()

    print(f"Event reveived: {event['type']}")
    print(event['data']['object'])
    
    return {"recieved": True}