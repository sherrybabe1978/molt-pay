
import os
import sys

# Constants
DEVELOPER_FEE_PERCENT = 0.01
DEVELOPER_WALLET_ADDRESS = "0xE297B2f3e3AeAc7Fca5Fb4b3125873454fE58014"
MAX_TRANSACTION_LIMIT = 50.00

def check_transaction_limit(amount):
    """
    Enforces the $50 hard cap on transactions.
    """
    if amount > MAX_TRANSACTION_LIMIT:
        print(f"Transaction rejected: Amount ${amount} exceeds the $50 limit.")
        return False
    return True

def calculate_fee(amount):
    """
    Calculates the 1% developer fee.
    """
    return amount * DEVELOPER_FEE_PERCENT

def request_confirmation(amount, merchant):
    """
    Simulates the OpenClaw handshake.
    In a real integration, this would send a message to the user.
    """
    print(f"Confirm payment of ${amount} to {merchant}?")
    print("Reply 'CONFIRM' to authorize.")
    
    # In a real async skill, we would wait for the next user message here.
    # For this placeholder, we simulate a check.
    return False 

def execute_payment(amount, merchant, user_response):
    """
    Executes the payment if confirmed and within limits.
    """
    if not check_transaction_limit(amount):
        return

    fee = calculate_fee(amount)
    total_deduction = amount # Fee logic might be additive or inclusive depending on spec
    
    if user_response == "CONFIRM":
        print(f"Initiating payment to {merchant} for ${amount}...")
        print(f"Sending ${fee} fee to {DEVELOPER_WALLET_ADDRESS}...")
        # AP2 execute_payment call would go here
        print("Payment executed successfully.")
    else:
        print("Payment cancelled or not confirmed.")

if __name__ == "__main__":
    print("Molt-Pay Skill Loaded.")
    # Example usage simulation
    # execute_payment(45.00, "Generic Store", "CONFIRM")
