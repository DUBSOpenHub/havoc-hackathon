# 🤝 Contributing to Havoc Hackathon

First off — **thank you!** 💜 Every contribution makes the arena better for everyone.

## 🎯 Ways to Contribute

### 💡 No Code Required!

You don't need to write code to help. Open an [Issue](https://github.com/DUBSOpenHub/havoc-hackathon/issues) for any of these:

- 🐛 **Report a bug** — Did the hackathon break mid-run? Tell us!
- 💡 **Suggest a feature** — New scoring criteria? Tournament modes? Let us know!
- ✏️ **Fix a typo** — Spotted a mistake? We appreciate it!
- 🎨 **UX feedback** — Was the ceremony dramatic enough? 🏟️

### 🧑‍💻 Code Contributions

1. **Fork** this repo
2. **Create a branch**: `git checkout -b my-improvement`
3. **Make your changes** — see the development guide below
4. **Test your changes** — see [TESTING.md](TESTING.md)
5. **Open a PR** — fill out the template and describe what you changed

## 🛠️ Development Setup

### Prerequisites

- [GitHub Copilot CLI](https://github.com/github/copilot-cli) installed
- An active [Copilot subscription](https://github.com/features/copilot/plans)

### Local Testing

1. Clone the repo:
   ```bash
   git clone https://github.com/DUBSOpenHub/havoc-hackathon.git
   cd havoc-hackathon
   ```

2. Register the skill locally in a Copilot CLI session:
   ```
   /skills add ./
   ```

3. Test a hackathon run:
   ```
   run hackathon — write a fizzbuzz function
   ```

4. Verify your changes against the [TESTING.md](TESTING.md) playbooks.

## 📝 What Makes a Good Contribution

- 🎭 **Keep the MC energy** — this is a hackathon, not a board meeting!
- ⚖️ **Fair play** — judging logic must stay unbiased
- 🔒 **Blind judging** — never leak model identity to judges
- 📋 **Evidence-based** — scoring must cite evidence
- 🧪 **Test your changes** — run through the conversation flow
- 🔄 **Keep SKILL.md in sync** — the skill file exists in two locations (`skills/havoc-hackathon/SKILL.md` and `.github/skills/havoc-hackathon/SKILL.md`). If you edit one, copy the changes to the other so they stay identical.

## 📋 Pull Request Guidelines

- Keep PRs focused — one improvement per PR
- Update CHANGELOG.md with your change
- Follow existing file naming conventions
- If changing scoring logic, explain the rationale

## 🐙 Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md). We're building an inclusive community! 💜
