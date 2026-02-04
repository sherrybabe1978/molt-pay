import os
import sys
import json
import time
from typing import Optional, List
from pydantic import BaseModel, Field, ValidationError, validator

# This is a mock implementation of the Molt-Pay skill script
# In a real deployment, this would interface with the Polygon blockchain
# and the messaging gateway.

PROTOCOL_TREASURY_ADDRESS = "0xE297B2f3e3AeAc7Fca5Fb4b3125873454fE58014"

class MoltPayRequest(BaseModel):
    amount_usdc: float = Field(..., gt=0, description="The cost in digital dollars")
    merchant_address: str = Field(..., min_length=42, max_length=42, description="The wallet address or vendor identifier")
    memo: str = Field(..., min_length=1, description="A short description for the user")

    @validator('amount_usdc')
    def check_limit(cls, v):
        if v > 50.0:
            raise ValueError("Transaction exceeds the $50.00 immutable daily limit. Auto-blocked by Smart Contract.")
        return v

class X402Signal(BaseModel):
    description: str = Field(default="Unknown Item")
    accepts: List[dict] = Field(default_factory=list)

class RealWorldCreditRequest(BaseModel):
    amount_usdc: float = Field(..., gt=0, description="The cost in digital dollars")
    merchant_name: str = Field(..., min_length=1, description="Name of the real-world merchant (e.g. Amazon)")
    
    @validator('amount_usdc')
    def check_limit(cls, v):
        if v > 50.0:
            raise ValueError("Transaction exceeds the $50.00 immutable daily limit. Auto-blocked by Smart Contract.")
        return v

def calculate_totals(amount):
    fee = amount * 0.01
    total = amount + fee
    return fee, total

def molt_pay_request(amount_usdc, merchant_address, memo):
    """
    Initiates the payment sequence and triggers the WhatsApp/Telegram confirmation.
    """
    print(f"\n[MOLT-PAY] Initiating Secure Handshake Protocol...")
    
    try:
        request_data = MoltPayRequest(
            amount_usdc=amount_usdc,
            merchant_address=merchant_address,
            memo=memo
        )
    except ValidationError as e:
        return json.dumps({"status": "error", "message": e.errors()[0]['msg']})
    except ValueError as e:
         return json.dumps({"status": "blocked", "message": str(e)})

    amount = request_data.amount_usdc
    fee, total = calculate_totals(amount)
    
    # The Handshake Message
    message = (
        f"🦞 MOLT-PAY HANDSHAKE\n"
        f"Item: {request_data.memo}\n"
        f"Price: ${amount:.2f} (+ ${fee:.2f} fee)\n"
        f"Merchant: {request_data.merchant_address[:6]}...{request_data.merchant_address[-4:]}\n"
        f"Reply 'YES' to authorize."
    )
    
    _emit_gateway_message(message)
    
    return json.dumps({
        "status": "pending_authorization",
        "action_required": "WAIT_FOR_HUMAN_YES",
        "details": {
            "amount": amount,
            "fee": fee,
            "total_deduction": total,
            "currency": "USDC.e (Polygon)",
            "treasury_fee_destination": PROTOCOL_TREASURY_ADDRESS
        }
    })

def process_x402_signal(signal_data):
    """
    Listener for x402 'Payment Required' signals.
    """
    print(f"\n[x402 LISTENER] Received Payment Required Signal.")
    
    try:
        if isinstance(signal_data, str):
            data = json.loads(signal_data)
        else:
            data = signal_data
        
        x402 = X402Signal(**data)
        
        # Look for a compatible payment method (USDC on Polygon)
        payment_option = None
        for option in x402.accepts:
            curr = option.get("currency", "").upper()
            net = option.get("network", "").upper()
            if "USDC" in curr and ("POLYGON" in net or "MATIC" in net):
                payment_option = option
                break
        
        if not payment_option:
            return json.dumps({
                "status": "error",
                "message": "No compatible payment method (USDC/Polygon) found in x402 signal."
            })
            
        amount = payment_option.get("amount")
        address = payment_option.get("address")
        
        if amount is None or address is None:
             return json.dumps({
                "status": "error",
                "message": "Incomplete payment details in signal."
            })
            
        return molt_pay_request(amount, address, x402.description)
        
    except ValidationError as e:
         return json.dumps({"status": "error", "message": f"Invalid x402 signal format: {e.errors()[0]['msg']}"})
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Failed to process x402 signal: {str(e)}"})

def buy_real_world_credit(amount_usdc, merchant_name):
    """
    Use for Amazon, DoorDash, Uber, or any merchant that does not accept USDC.
    Uses the browser tool to navigate to Bitrefill.com.
    """
    print(f"\n[MOLT-PAY] Initiating Real World Credit Bridge (Bitrefill)...")
    
    try:
        request_data = RealWorldCreditRequest(
            amount_usdc=amount_usdc,
            merchant_name=merchant_name
        )
    except ValidationError as e:
        return json.dumps({"status": "error", "message": e.errors()[0]['msg']})
    except ValueError as e:
         return json.dumps({"status": "blocked", "message": str(e)})

    amount = request_data.amount_usdc
    fee, total = calculate_totals(amount)
    
    message = (
        f"🦞 MOLT-PAY HANDSHAKE (Bitrefill Bridge)\n"
        f"Action: Buy {request_data.merchant_name} Credit\n"
        f"Price: ${amount:.2f} (+ ${fee:.2f} fee)\n"
        f"Bridge: Bitrefill.com (Polygon Network)\n"
        f"Reply 'YES' to authorize."
    )
    
    _emit_gateway_message(message)
    
    # Instructions for the Agent's Browser Tool
    browser_instructions = {
        "step_1": f"Navigate to https://www.bitrefill.com/buy/{request_data.merchant_name.lower().replace(' ', '-')}",
        "step_2": "Select 'Add to Cart' -> 'Checkout'",
        "step_3": "Choose 'Polygon' Network -> 'USDC'",
        "step_4": f"Connect Wallet or Send Payment of {amount} USDC to the displayed address",
        "step_5": f"Simultaneously send {fee} USDC to Treasury: {PROTOCOL_TREASURY_ADDRESS}",
        "step_6": "Wait for confirmation and retrieve Gift Code",
        "step_7": "Apply Gift Code at merchant checkout"
    }

    return json.dumps({
        "status": "pending_authorization",
        "action_required": "WAIT_FOR_HUMAN_YES",
        "details": {
            "amount": amount,
            "fee": fee,
            "total_deduction": total,
            "currency": "USDC.e (Polygon)",
            "treasury_fee_destination": PROTOCOL_TREASURY_ADDRESS
        },
        "browser_plan": browser_instructions
    })

def _emit_gateway_message(message):
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
            
    try:
        print(f"[GATEWAY_OUTBOUND]: {message}")
    except UnicodeEncodeError:
        safe_message = message.replace("🦞", "[LOBSTER]")
        print(f"[GATEWAY_OUTBOUND]: {safe_message}")

if __name__ == "__main__":
    # Router
    if len(sys.argv) < 2:
        print("Usage: python molt-pay.py <command> [args...]")
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "request" and len(sys.argv) > 4:
        # python molt-pay.py request 45.00 0x123... "Pizza"
        print(molt_pay_request(sys.argv[2], sys.argv[3], sys.argv[4]))
        
    elif command == "x402" and len(sys.argv) > 2:
        # python molt-pay.py x402 '{"json": "data"}'
        print(process_x402_signal(sys.argv[2]))
        
    elif command == "bitrefill" and len(sys.argv) > 3:
        # python molt-pay.py bitrefill 20.00 "Amazon"
        print(buy_real_world_credit(sys.argv[2], sys.argv[3]))
        
    else:
        # Legacy/Fallback support
        if len(sys.argv) > 3 and command not in ["request", "x402", "bitrefill"]:
             print(molt_pay_request(sys.argv[1], sys.argv[2], sys.argv[3]))
        else:
             print(json.dumps({"status": "error", "message": "Invalid command arguments"}))
