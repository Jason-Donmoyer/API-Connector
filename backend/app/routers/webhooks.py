from fastapi import APIRouter, Request, HTTPException
import stripe
from app.config import STRIPE_WEBHOOK_SECRET

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

    print(f"Event reveived: {event['type']}")
    print(event['data']['object'])
    
    return {"recieved": True}