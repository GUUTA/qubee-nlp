You can copy and paste **this version** of the README.md file. This is the properly formatted version that includes all the original content with correct Markdown formatting:

```markdown
# Qubee NLP

<div align="center">

[![PyPI version](https://img.shields.io/pypi/v/qubee-nlp.svg)](https://pypi.org/project/qubee-nlp/)
[![Python versions](https://img.shields.io/pypi/pyversions/qubee-nlp.svg)](https://pypi.org/project/qubee-nlp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-readthedocs-blue)](https://qubee-nlp.readthedocs.io)
[![Tests](https://github.com/afaanoromoo/qubee-nlp/actions/workflows/tests.yml/badge.svg)](https://github.com/afaanoromoo/qubee-nlp/actions/workflows/tests.yml)
[![Codecov](https://codecov.io/gh/afaanoromoo/qubee-nlp/branch/main/graph/badge.svg)](https://codecov.io/gh/afaanoromoo/qubee-nlp)
[![Downloads](https://static.pepy.tech/badge/qubee-nlp/month)](https://pepy.tech/project/qubee-nlp)

**Natural Language Processing tools for Afaan Oromoo (Oromo language) using Qubee script**

[Installation](#installation) • [Quick Start](#quick-start) • [Documentation](https://qubee-nlp.readthedocs.io) • [Examples](examples/)

</div>

## Features

- **Text Validation**: Validate Qubee script text for Afaan Oromoo
- **Tokenization**: Word and sentence tokenization with context awareness
- **Normalization**: Text cleaning, diacritic handling, and standardization
- **Stemming**: Morphological analysis and stemming for Afaan Oromoo
- **POS Tagging**: Part-of-speech tagging framework
- **Syllabification**: Syllable segmentation based on Oromo phonotactics
- **Stopword Removal**: Language-specific stopword lists
- **Corpus Tools**: Corpus building, processing, and analysis

## Installation

### From PyPI (Recommended)

```bash
pip install qubee-nlp
```

### From Source

```bash
git clone https://github.com/afaanoromoo/qubee-nlp.git
cd qubee-nlp
pip install -e .
```

### For Development

```bash
git clone https://github.com/afaanoromoo/qubee-nlp.git
cd qubee-nlp
pip install -e .[dev]  # Includes testing and development tools
```

## Quick Start

```python
from qubee_nlp import word_tokenize, sentence_tokenize

# Tokenize text
text = "Afaan Oromoo afaan guddaa dha."
tokens = word_tokenize(text)
print(tokens)  # ['AFAAN', 'OROMOO', 'AFAAN', 'GUDDAA', 'DHA']

# Tokenize sentences
sentences = sentence_tokenize("Kuni kitaaba dha. Inni bareessaa dha.")
print(sentences)  # ['KUNI KITAABA DHA.', 'INNI BAREESSAA DHA.']
```

### Text Validation

```python
from qubee_nlp import validate_qubee_text

is_valid, invalid_chars = validate_qubee_text("Afaan Oromoo")
print(is_valid)  # True
print(invalid_chars)  # []
```

### Text Normalization

```python
from qubee_nlp import normalize_qubee

text = "  Áfáan   Oromoo  "
normalized = normalize_qubee(text)
print(normalized)  # "AFAAN OROMOO"
```

### Advanced Tokenization

```python
from qubee_nlp import QubeeTokenizer

tokenizer = QubeeTokenizer(preserve_case=True)
tokens = tokenizer.tokenize("Afaan Oromoo")
print(tokens)  # ['Afaan', 'Oromoo']
```

### Stemming

```python
from qubee_nlp.stemmer import QubeeStemmer

stemmer = QubeeStemmer()
stem = stemmer.stem("barreessuu")
print(stem)  # "bar"
```

## Documentation

Complete documentation is available at [https://qubee-nlp.readthedocs.io](https://qubee-nlp.readthedocs.io)

- [API Reference](https://qubee-nlp.readthedocs.io/en/latest/api/)
- [Getting Started Guide](https://qubee-nlp.readthedocs.io/en/latest/tutorials/getting_started.html)
- [Afaan Oromoo NLP Tutorial](https://qubee-nlp.readthedocs.io/en/latest/tutorials/afaan_oromoo_nlp.html)
- [Examples](https://github.com/afaanoromoo/qubee-nlp/tree/main/examples)

## Examples

Check the [examples directory](examples/) for complete usage examples:

- [Basic Usage](examples/basic_usage.py)
- [Tokenization Examples](examples/tokenization_example.py)
- [Stemming Examples](examples/stemming_example.py)
- [Advanced Features](examples/advanced_features.py)

## Command Line Interface

Qubee NLP includes a command-line interface:

```bash
# Analyze text
qubee-nlp analyze "Afaan Oromoo afaan guddaa dha."

# Tokenize file
qubee-nlp tokenize input.txt output.txt

# Validate text
qubee-nlp validate "Áfáan Órómóó"

# Get help
qubee-nlp --help
```

## Qubee Alphabet

Qubee is the Latin-based alphabet used for writing Afaan Oromoo. The library supports:

- **Vowels (5)**: A, E, I, O, U (with optional diacritics: á, é, í, ó, ú)
- **Consonants (21)**: B, C, D, F, G, H, J, K, L, M, N, P, Q, R, S, T, V, W, X, Y, Z
- **Digraphs**: CH, DH, NY, PH, SH
- **Special Characters**: Apostrophe (') and hyphen (-) for words like "waa'ee"

## Language Support

This library is specifically designed for **Afaan Oromoo** (Oromo language), which:

- Is a Cushitic language spoken by over 40 million people
- Uses the Qubee (Latin) script for writing
- Has rich morphology with agglutinative structure
- Is the most widely spoken Cushitic language

## Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/afaanoromoo/qubee-nlp.git
cd qubee-nlp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=qubee_nlp

# Run specific test file
pytest tests/test_alphabet.py -v

# Run with parallel execution
pytest -n auto
```

### Code Quality

```bash
# Format code
black src/qubee_nlp tests examples

# Lint code
flake8 src/qubee_nlp tests examples

# Type checking
mypy src/qubee_nlp

# Security check
bandit -r src/qubee_nlp
```

### Building Documentation

```bash
# Install documentation dependencies
pip install -e .[docs]

# Build documentation
cd docs
make html

# View documentation
open _build/html/index.html  # macOS
start _build/html/index.html  # Windows
xdg-open _build/html/index.html  # Linux
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Ways to Contribute

1. **Report bugs**: File issues on [GitHub Issues](https://github.com/afaanoromoo/qubee-nlp/issues)
2. **Suggest features**: Share ideas in [Discussions](https://github.com/afaanoromoo/qubee-nlp/discussions)
3. **Submit pull requests**: Fix bugs or add features
4. **Improve documentation**: Help make docs better
5. **Share examples**: Create tutorials or examples
6. **Test the library**: Try it out and give feedback

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Support

### Community Support

- [GitHub Discussions](https://github.com/afaanoromoo/qubee-nlp/discussions): For questions and discussions
- [GitHub Issues](https://github.com/afaanoromoo/qubee-nlp/issues): For bug reports and feature requests
- [Documentation](https://qubee-nlp.readthedocs.io): For detailed guides and API reference

### Professional Support

For commercial support, consulting, or custom development, please contact [contact@qubeenlp.org](mailto:contact@qubeenlp.org).

## Citation

If you use Qubee NLP in your research, please cite:

```bibtex
@software{qubee_nlp,
  title = {Qubee NLP: Natural Language Processing for Afaan Oromoo},
  author = {Guta Tesema Tufa, Qubee NLP Team},
  year = {2025},
  url = {https://github.com/afaanoromoo/qubee-nlp},
  version = {0.1.0}
}
```

## Related Projects

- [Oromo Text Corpus](https://github.com/afaanoromoo/oromo-text-corpus): Collection of Afaan Oromoo texts
- [Oromo Language Tools](https://github.com/afaanoromoo/oromo-language-tools): Additional language tools
- [Qubee Fonts](https://github.com/afaanoromoo/qubee-fonts): Fonts for Qubee script

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The Afaan Oromoo language community
- Contributors and maintainers
- Early adopters and testers
- Open source community

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=afaanoromoo/qubee-nlp&type=Date)](https://star-history.com/#afaanoromoo/qubee-nlp&Date)

---

<div align="center">
Made with ❤️ for the Afaan Oromoo language community
</div>
```

