# Molt-Pay

The Secure Handshake for AI Agents. Non-custodial. Immutable limits. Human-in-the-loop. The first protocol designed to stop unauthorized agent spending.

## Technical Documentation

### 1. System Architecture
Molt-Pay operates as a "Trust Middleware" between three primary technologies:

- **The Interface (OpenClaw):** Acting as the communication bridge, Molt-Pay listens to user intent via WhatsApp, Telegram, or Discord.
- **The Logic (Google AP2):** Using the Agent Payments Protocol, Molt-Pay captures commercial intentions (e.g., "I want to buy X") and translates them into structured settlement objects.
- **The Network (Polygon/Safe):** All transactions are settled on the Polygon PoS network. We utilize Safe (Gnosis) Smart Accounts to enforce spending limits and non-custodial ownership.

#### The Smart Account (Safe + Pimlico)
Molt-Pay uses Smart Accounts. Unlike a traditional wallet, your bot's funds live in a secure, on-chain vault with a hardware-level spending limit. You control the vault with your existing MetaMask, but the bot only has access to the 'Daily Allowance' you authorize. Molt-Pay is non-custodial: You keep the master keys; we provide the secure bridge.

### 2. The "Molt-Handshake" Protocol (HITL)
The core of Molt-Pay is the Human-in-the-Loop (HITL) security sequence:

1. **Request:** An agent identifies a purchase and calls the molt-pay skill.
2. **Validation:** The protocol checks the $50 Daily Limit. If the amount is higher, the transaction is auto-blocked.
3. **The Handshake:** A "Payment Request" is sent to the user's phone via the OpenClaw Gateway.
4. **Signature:** The user replies YES to sign transaction (via MetaMask signature).
5. **Settlement:** The Smart Account releases the USDC.e payment to the merchant.

### 3. Developer Quick-Start (CLI)
To integrate Molt-Pay into a local OpenClaw instance (Alpha Release):

1. **Download the Installer:**
   Get the `molt-pay-install.js` script from the repository.

2. **Run the Installer:**
   ```bash
   node molt-pay-install.js
   ```

3. **Follow the Prompts:**
   The script will ask for your MetaMask address to provision your secure **Safe Smart Account**.

4. **Automatic Setup:**
   The installer will automatically generate:
   - `molt-pay.py`: The secure payment skill logic.
   - `PAYMENT_SKILL.md`: The instruction manual for your AI agent.
   - `.env`: The configuration file with your new Vault address.

#### The Installer Logic
In this script, we utilize the Safe Core SDK and Pimlico infrastructure to:
- Provision a **Safe Smart Account** owned by your MetaMask address.
- Enable the **Pimlico Paymaster** for a "Gasless" experience (pay fees in USDC).
- Output your unique **Molt Vault Address**.

> **Note for Alpha Users:** This version currently simulates the on-chain deployment for testing purposes. Real-money settlement will be enabled in the Beta release.

#### Required Environment Variables:
The installer automatically generates a `.env` file in your **current working directory** (the same folder where you ran the script).

You should verify this file contains:
- `MOLT_PAY_VAULT_ADDRESS`: Your bot's secure wallet.
- `MOLT_PAY_OWNER_ADDRESS`: Your master controller address.

*(Note: On Mac/Linux, files starting with `.` may be hidden. Use `ls -a` to see it.)*


### 4. Security & Exploit Protection
Molt-Pay was specifically designed to mitigate Remote Code Execution (RCE) vulnerabilities recently found in AI agent gateways.

- **Key Isolation:** Even if an attacker compromises the Moltbot server, they do not have the authorization to move funds. Authorization is "Out-of-Band," meaning it depends on the user's physical mobile device.
- **Immutable Limits:** Because spending limits are set at the Smart Contract level (On-chain), they cannot be modified by a compromised agent.

### 5. Protocol Fees
Molt-Pay is a free-to-install, open-source protocol. To maintain the network and community development, a 1% Protocol Fee is applied to each successful transaction.

Example: A $20.00 purchase results in a $0.20 fee to the Molt-Pay treasury.
