# 🔒 Security Policy

## 🛡️ Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | ✅ Yes     |

## 🚨 Reporting a Vulnerability

We take security seriously! 🐙 If you discover a security vulnerability in this project, **please report it responsibly**.

### How to Report

1. **DO NOT** open a public GitHub issue for security vulnerabilities
2. Instead, email us at: **security@dubsopenhub.com**
3. Or use [GitHub's private vulnerability reporting](https://github.com/DUBSOpenHub/havoc-hackathon/security/advisories/new)

### What to Include

Please provide as much of the following as possible:

- 📝 Description of the vulnerability
- 🔄 Steps to reproduce
- 💥 Potential impact
- 💡 Suggested fix (if you have one)

### What to Expect

- ⏱️ **Acknowledgment** within 48 hours
- 🔍 **Assessment** within 1 week
- 🛠️ **Fix or mitigation** as quickly as possible
- 🎉 **Credit** in the release notes (unless you prefer anonymity)

## 🔐 Security Features

This repository has the following GitHub security features configured:

| Feature | Status | Notes |
|---------|--------|-------|
| ✅ Dependabot Alerts | Enabled | Monitors dependencies for known vulnerabilities |
| ✅ Dependabot Security Updates | Enabled | Auto-creates PRs to fix vulnerable dependencies |
| ✅ Secret Scanning | Enabled | Detects accidentally committed secrets |
| ✅ Secret Scanning Push Protection | Enabled | Blocks pushes containing secrets |
| ✅ Code Scanning (CodeQL) | Available | Static analysis for security bugs |

## 📋 Best Practices

Since this is a Copilot CLI skill (no runtime code, only markdown instructions), the primary security considerations are:

- 🔑 **No secrets in skill files**  -  SKILL.md and agent.md should never contain API keys, tokens, or credentials
- 📜 **Safe instructions**  -  Skill instructions should never instruct the agent to bypass security controls
- 🔍 **Dependency awareness**  -  If dependencies are added in the future, keep them updated

## 🛡️ Prompt Injection Mitigation

Since this skill orchestrates multiple AI models and processes user-provided task descriptions, prompt injection is a relevant concern:

- 🔒 **Sealed judging**  -  Judge models receive anonymized submissions with model fingerprints stripped, reducing the attack surface for identity-based manipulation
- 🧹 **Input sanitization**  -  The SKILL.md includes anti-gaming protections: calibration anchors, keyword stuffing detection, test tampering scans, and prompt injection scans
- 🚫 **No credential passthrough**  -  User input is used as task descriptions only; it is never interpolated into system-level commands or used to access external services
- ⚖️ **Consensus scoring**  -  Even if one judge model is influenced by injected content, the median-of-3 consensus mechanism limits the impact on final scores

## 📄 License

This project is licensed under the [MIT License](LICENSE).
