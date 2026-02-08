# 🔐 Molt‑Pay Security Model

This document describes the **intended security properties** of Molt‑Pay
under its defined threat model. It does not constitute a warranty or guarantee.

---

## Design Intent

Molt‑Pay is designed as a **non‑custodial, human‑approved payment interface**
for AI agents, with explicit limits and constraints.

---

## Intended Security Properties

Under normal operation and within its threat model, Molt‑Pay is designed to:

- Require explicit human approval for every transaction
- Prevent autonomous or background spending by agents
- Enforce per‑transaction spending limits at the smart‑contract level
- Bind approvals to specific payment requests
- Limit the impact of compromised agent logic

---

## Threat Model Assumptions

Molt‑Pay v0.1 assumes:

- The user controls their private keys securely
- The Polygon network and Safe contracts operate correctly
- Third‑party merchants behave according to their terms

---

## Out of Scope

Molt‑Pay is **not designed to protect against**:

- Compromised user devices or browsers
- Lost or leaked private keys
- Malicious or fraudulent merchants
- Blockchain‑level failures

---

## Known Limitations

- No cryptographic approval signatures yet
- No cumulative daily spend enforcement
- Shopping agents operate on prepaid value only

---

## Important Notice

This document describes **design intent**, not guaranteed outcomes.
Users are responsible for evaluating whether Molt‑Pay meets their needs.

For legal terms, see LEGAL.md.
