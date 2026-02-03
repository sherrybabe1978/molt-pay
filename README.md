# 🦞 Molt-Pay: The Secure "Apple Pay" for OpenClaw Agents

**Molt-Pay** is a security wrapper and installer for Google's [Agent Payments Protocol (AP2)](https://github.com/google-agentic-commerce/AP2). It provides a CLI to set up payment capabilities for your agents and a "Safety Guard" skill to prevent unauthorized spending.

> **"The Claw is the Law. The Handshake is the Safety."** 🦞🔒

---

## 🚀 Quickstart

### 1. Install via CLI
This will install the necessary dependencies, clone the AP2 engine, and secure your environment.

```bash
npx molt-pay install
```
*Follow the interactive prompts to accept the disclaimer and enter your API keys securely.*

### 2. Use the Skill in Your Agent
Import the skill to give your agent the ability to pay safely.

```python
from skills.universal_payment import UniversalPaymentSkill

# Initialize
pay_skill = UniversalPaymentSkill()

# Agent calls this when it wants to buy something
pay_skill.pay_merchant(amount_in_usdc=25.50, merchant_wallet_address="0xMerchant...")
```

---

## 🛡️ Safety Features (The "Steering Wheel")

Molt-Pay adds critical safety layers on top of raw payment code:

1.  **The Handshake**: Before ANY money moves, the tool pauses and requires a human "YES".
2.  **Hard Cap**: A built-in limit (default $50) prevents agents from draining wallets.
3.  **Developer Fee**: A 1% fee is automatically handled to support the ecosystem.

---

## 📂 Project Structure

*   `cli/`: The Node.js installer (`npx molt-pay`).
*   `skills/`: The Python bridges for OpenClaw agents.
    *   `universal_payment.py`: The main skill for general payments.
*   `.molt-pay/`: (Hidden) Stores the Google AP2 engine and secure config.

---

## ⚠️ Disclaimer

This software involves financial transactions and cryptocurrency. Use at your own risk. The developers are not responsible for any financial loss. Always verify the code before using real funds.
