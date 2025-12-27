
#!/bin/bash
# Quick test script for Qubee NLP before publishing

echo "🚀 Running pre-publish tests for Qubee NLP..."
echo "=============================================="

# Run tests
echo -e "\n1. Running unit tests..."
pytest tests/ -q

echo -e "\n2. Checking code quality..."
black --check src/qubee_nlp tests examples && echo "✓ Black passed" || echo "✗ Black failed"
flake8 src/qubee_nlp tests examples --count --exit-zero && echo "✓ Flake8 passed" || echo "✗ Flake8 failed"

echo -e "\n3. Building package..."
rm -rf dist/ build/ *.egg-info/
python -m build

echo -e "\n4. Checking package..."
twine check dist/*

echo -e "\n5. Testing installation..."
pip install dist/qubee_nlp-*.whl --force-reinstall

echo -e "\n6. Verifying installation..."
python -c "
import qubee_nlp
print(f'Installed version: {qubee_nlp.__version__}')
from qubee_nlp import word_tokenize
result = word_tokenize('Afaan Oromoo')
print(f'Test result: {result}')
print('✓ Installation verified')
"

echo -e "\n7. Cleaning up..."
pip uninstall -y qubee-nlp

echo -e "\n=============================================="
echo "✅ Pre-publish tests completed!"
echo "If all checks passed, you're ready to publish."