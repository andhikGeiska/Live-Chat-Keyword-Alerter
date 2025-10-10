# Contributing to Live Chat Keyword Alerter

Thank you for your interest in contributing to this project! We welcome contributions from the community and are grateful for any help you can provide.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow:

- **Be respectful**: Treat everyone with respect and kindness
- **Be inclusive**: Welcome people of all backgrounds and identities
- **Be collaborative**: Work together and help each other
- **Be professional**: Keep discussions focused and constructive

## How to Contribute

There are many ways you can contribute to this project:

### 🐛 Bug Reports
- Use the bug report template
- Include detailed reproduction steps
- Provide environment information

### 💡 Feature Requests
- Use the feature request template
- Explain the use case and benefits
- Consider implementation complexity

### 📝 Documentation
- Improve README clarity
- Add usage examples
- Fix typos and grammar

### 🔧 Code Contributions
- Fix bugs
- Implement new features
- Improve performance
- Add tests

## Development Setup

1. **Fork the repository** on GitHub

2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Live-Chat-Keyword-Alerter.git
   cd Live-Chat-Keyword-Alerter
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source ./venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

## Coding Standards

### Python Style
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use descriptive variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small

### Code Quality
- Write readable, maintainable code
- Add comments for complex logic
- Handle errors gracefully
- Use logging instead of print statements

### Example Code Style:
```python
def monitor_chat(live_chat_id: str, keywords: list, poll_interval: int, logger) -> None:
    """
    Monitor live chat for specified keywords.
    
    Args:
        live_chat_id: The ID of the live chat to monitor
        keywords: List of keywords to search for
        poll_interval: Seconds between API polls
        logger: Logger instance for output
    """
    logger.info("Starting chat monitoring for keywords: %s", keywords)
    # Implementation here...
```

### Testing
- Test your changes before submitting
- Include both positive and negative test cases
- Verify functionality on both YouTube and TikTok monitors

## Pull Request Process

1. **Ensure your code follows the coding standards**

2. **Update documentation** if you're changing functionality

3. **Write a clear commit message**:
   ```
   feat: add keyword highlighting in alerts
   
   - Add color coding for matched keywords
   - Improve alert readability
   - Update CLI help text
   ```

4. **Create a pull request** with:
   - Clear title describing the change
   - Detailed description of what was changed and why
   - Reference any related issues with `Fixes #123`

5. **Respond to review feedback** promptly and professionally

### Commit Message Format
Use conventional commits format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

## Reporting Issues

Before creating a new issue:

1. **Search existing issues** to avoid duplicates
2. **Use the appropriate template** (bug report, feature request, question)
3. **Provide detailed information** including:
   - Environment details (OS, Python version)
   - Steps to reproduce
   - Expected vs actual behavior
   - Console output or error messages

## Platform-Specific Contributions

### YouTube Monitor
- Requires YouTube Data API v3 knowledge
- Consider API quota limitations
- Test with live streams that have active chat

### TikTok Monitor
- Uses unofficial TikTokLive library
- Handle connection instability gracefully
- Test retry mechanisms thoroughly

## Getting Help

If you need help with contributing:

1. **Check the README** for setup instructions
2. **Look at existing code** for examples
3. **Create a question issue** using the template
4. **Join discussions** in existing issues

## Recognition

Contributors will be recognized in the project:
- README contributors section (if we add one)
- Release notes for significant contributions
- GitHub contributors page

Thank you for helping make this project better! 🚀