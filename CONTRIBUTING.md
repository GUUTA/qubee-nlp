# Contributing to Qubee NLP

Thank you for your interest in contributing to Qubee NLP! We welcome contributions from everyone.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/qubee-nlp.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
5. Install development dependencies: `pip install -e .[dev]`
6. Install pre-commit hooks: `pre-commit install`

## Development Workflow

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `pytest`
4. Format code: `black src/qubee_nlp tests`
5. Check linting: `flake8 src/qubee_nlp tests`
6. Commit your changes: `git commit -m "Add feature: your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Pull Request Guidelines

- Keep PRs focused on a single feature or bug fix
- Include tests for new functionality
- Update documentation as needed
- Follow the existing code style
- Add a descriptive title and description

## Testing

- Write tests for new functionality
- Ensure all tests pass: `pytest`
- Run specific test files: `pytest tests/test_alphabet.py`
- Run with coverage: `pytest --cov=qubee_nlp`

## Documentation

- Update docstrings for new functions/classes
- Update README.md if needed
- Add examples in the examples/ directory
- Update API documentation if adding new modules

## Questions?

- Open an issue for bug reports
- Start a discussion for questions
- Join our community chat (link in README)

Thank you for contributing! 🎉