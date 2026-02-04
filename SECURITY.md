# Security Policy

## Reporting a Vulnerability

We take the security of Molt-Pay seriously. If you discover a security vulnerability, please do **NOT** open a public issue.

### How to Report
Please report sensitive security issues via email to: **security@molt.bot** (or your preferred contact email).

We will respond within 48 hours to acknowledge your report.

### Scope
- **In Scope:** 
  - Vulnerabilities in the `molt-pay.py` payment logic.
  - Issues with the `molt-pay-install.js` installer.
  - Bypass of the $50 limit.
- **Out of Scope:** 
  - User error (leaked private keys).
  - Vulnerabilities in the Polygon network itself.
  - Issues with third-party merchants (Amazon, Bitrefill).

## Managing Vulnerabilities

### 1. Automated Scanning
We use GitHub Dependabot and `npm audit` to track dependency vulnerabilities.

### 2. Emergency Response Plan
If a critical bug is found in a live version:
1.  **Deprecate:** Run `npm deprecate molt-pay-cli@<version> "Critical security issue. Please upgrade."`
2.  **Patch:** Fix the code and bump the version (e.g., 0.1.1).
3.  **Publish:** Run `npm publish` immediately.
