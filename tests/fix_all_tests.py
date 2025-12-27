# fix_all_tests.py
import os
import re

def fix_test_alphabet():
    """Fix test_alphabet.py"""
    if not os.path.exists('tests/test_alphabet.py'):
        return
    
    with open('tests/test_alphabet.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix any occurrence of eiu"""
    content = content.replace('eiu"""', '"""')
    
    with open('tests/test_alphabet.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed test_alphabet.py")

def fix_test_stemmer():
    """Fix test_stemmer.py"""
    if not os.path.exists('tests/test_stemmer.py'):
        return
    
    with open('tests/test_stemmer.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    for line in lines:
        # Fix the unclosed string
        if "'word_type'] in ['verb', '" in line:
            # Complete the list
            line = line.replace("['verb', '", "['verb', 'noun', 'adjective']")
        fixed_lines.append(line)
    
    with open('tests/test_stemmer.py', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("Fixed test_stemmer.py")

def fix_imports():
    """Fix all import statements"""
    
    import_fixes = [
        # (filename, old_import, new_import)
        ('tests/test_normalizer.py', 
         'from qubee_nlp.normalizer import QubeeNormalizer, normalize_text, remove_diacritics',
         'from qubee_nlp.normalizer import TextNormalizer, normalize_text, remove_diacritics'),
        
        ('tests/test_syllabifier.py',
         'from qubee_nlp.syllabifier import QubeeSyllabifier, syllabify_word, syllabify_text',
         'from qubee_nlp.syllabifier import Syllabifier, syllabify_word, syllabify_text'),
        
        ('tests/test_pos/test_tagger.py',
         'from qubee_nlp.pos import POSTagger, get_afaan_oromoo_tags',
         'from qubee_nlp.pos import QubeePOSTagger, get_tag_description')
    ]
    
    for filename, old_import, new_import in import_fixes:
        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            continue
            
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_import in content:
            content = content.replace(old_import, new_import)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed imports in {filename}")
        else:
            # Try to find similar patterns
            print(f"Pattern not found in {filename}, checking file...")
            with open(filename, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    if 'import' in line and ('QubeeNormalizer' in line or 'POSTagger' in line or 'QubeeSyllabifier' in line):
                        print(f"  Line {i}: {line.strip()}")

def check_test_files():
    """Check for syntax errors in test files"""
    print("\nChecking test files for syntax errors...")
    
    test_files = [
        'tests/test_alphabet.py',
        'tests/test_normalizer.py',
        'tests/test_stemmer.py',
        'tests/test_syllabifier.py',
        'tests/test_pos/test_tagger.py'
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    # Try to compile to check syntax
                    compile(f.read(), test_file, 'exec')
                print(f"✓ {test_file}: Syntax OK")
            except SyntaxError as e:
                print(f"✗ {test_file}: Syntax error - {e}")
        else:
            print(f"? {test_file}: File not found")

if __name__ == '__main__':
    print("Fixing test files...")
    print("=" * 50)
    
    fix_test_alphabet()
    fix_test_stemmer()
    fix_imports()
    
    print("\n" + "=" * 50)
    check_test_files()
    
    print("\nDone! Run 'pytest' to see if tests pass now.")