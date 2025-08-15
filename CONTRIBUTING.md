# Contributing Guidelines

We welcome contributions to the Telegram Trade Bot! Please follow these guidelines:

## Code Style
- Follow PEP8 conventions
- Use type hints for all function signatures
- Keep functions under 25 lines
- Document public methods with docstrings

## Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

## Testing Requirements
- Include unit tests for new features
- Ensure test coverage doesn't decrease
- Run tests with `pytest tests/`

## Reporting Issues
Include in bug reports:
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS)
- Relevant logs (remove sensitive data)

