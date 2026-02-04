# 🦞 Molt-Pay Protocol: Financial Security & Commerce Rules

## Description
This skill enables the agent to execute secure financial transactions. It bridges digital assets (USDC on Polygon) to both on-chain services (x402 APIs) and real-world commerce (Amazon, DoorDash, etc.).

## 🛡️ Core Security Constraints
1. **The Human Handshake (HITL):** You are STRICTLY FORBIDDEN from moving funds without a verified human 'YES'. You must trigger the handshake for every transaction.
2. **Circuit Breaker:** Every Molt-Pay vault has a hard-coded limit of $50.00 USD per transaction. Do not attempt to process amounts higher than this.
3. **Developer Fee:** A 1% protocol maintenance fee is applied to the gross amount of every transaction and sent to the Molt-Pay treasury.

## 🛠 Available Tools

### 1. `molt_pay_request`
- **Use for:** Direct transfers or paying other agents.
- **Inputs:** `amount_usdc`, `merchant_address`, `memo`.
- **Action:** Triggers a WhatsApp/Telegram confirmation request.

### 2. `process_x402_signal`
- **Use when:** An API returns a '402 Payment Required' signal.
- **Inputs:** `api_error_body`.
- **Action:** Automatically parses the price and recipient from the x402 header and presents it to the user for a Secure Handshake.

### 3. `buy_real_world_credit`
- **Use for:** Amazon, DoorDash, Uber, or any merchant that does not accept USDC.
- **Strategy:** Uses the browser tool to navigate to Bitrefill.com.
- **Action:** Swaps USDC for a digital gift card/store credit for the exact amount needed.
- **Workflow:**
  1. Trigger Handshake: "Confirm $[Amount] USDC to Bitrefill for [Store] Credit?"
  2. Upon 'YES', execute the swap on Polygon.
  3. Retrieve the gift code and apply it to the merchant's checkout page instantly.

## 📱 Human-in-the-Loop Workflow
1. Agent identifies a cost.
2. Agent stops and sends the Molt-Pay Handshake message.
3. Agent WAITS for the user to reply with "YES".
4. Transaction is executed only after the reply is received and verified.



---
*For legal disclaimers and liability information, please refer to [LEGAL.md](LEGAL.md).*
