# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | ✅ Current release |
| 0.1.x   | ⚠️ Bug-fixes only  |

---

## Reporting a Vulnerability

If you discover a security vulnerability in `muxpy`, **please do NOT open a public GitHub Issue**.  
Instead, contact us via email:

📧 **owner@kzunique.com**

Please include:
- A clear description of the vulnerability.
- Steps to reproduce the issue (if applicable).
- The potential impact or attack vector.

We will acknowledge your report within **72 hours** and aim to provide a fix or mitigation within **14 days**.

---

## Security Considerations

- `muxpy` interacts with Android hardware through Termux:API CLI binaries. Ensure that sensitive data (GPS coordinates, SMS bodies, clipboard content) is handled responsibly in your application.
- **Never hardcode** API keys, tokens, or personal credentials inside scripts using `muxpy`. Use environment variables or encrypted secret stores.
- The **mock engine** (enabled automatically outside Android) returns synthetic data and poses no security risk for local development and testing.
