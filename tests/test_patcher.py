"""
Test per Patcher
"""

import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fylia.patcher import Patcher


def test_patcher_creation():
    """Test creazione Patcher"""
    patcher = Patcher()
    assert patcher is not None


def test_create_diff():
    """Test creazione diff"""
    patcher = Patcher()
    old = "line1\nline2\nline3\n"
    new = "line1\nline2_modified\nline3\n"
    
    diff = patcher.create_diff("test.py", old, new)
    assert diff is not None
    assert "-line2" in diff or "line2" in diff
    assert "+line2_modified" in diff or "line2_modified" in diff


def test_extract_code_blocks():
    """Test estrazione blocchi di codice"""
    patcher = Patcher()
    text = """
Ecco un esempio:

```python
def hello():
    return "world"
```

E altro testo
"""
    
    blocks = patcher.extract_code_blocks(text)
    assert len(blocks) == 1
    assert blocks[0][0] == "python"
    assert "def hello" in blocks[0][1]


def test_extract_multiple_code_blocks():
    """Test estrazione multipli blocchi"""
    patcher = Patcher()
    text = """
```python
code1
```

Testo intermedio

```javascript
code2
```
"""
    
    blocks = patcher.extract_code_blocks(text)
    assert len(blocks) == 2
    assert blocks[0][0] == "python"
    assert blocks[1][0] == "javascript"


def test_parse_file_instruction():
    """Test parsing istruzioni file"""
    patcher = Patcher()
    text = """
File: src/example.py
```python
def test():
    pass
```
"""
    
    result = patcher.parse_file_instruction(text)
    assert result is not None
    file_path, content = result
    assert file_path == "src/example.py"
    assert "def test" in content


def test_apply_patch():
    """Test applicazione patch"""
    with tempfile.TemporaryDirectory() as tmpdir:
        patcher = Patcher(tmpdir)
        content = "print('hello')\n"
        
        success = patcher.apply_patch("test.py", content, backup=False)
        assert success
        
        # Verifica che il file esista
        test_file = Path(tmpdir) / "test.py"
        assert test_file.exists()
        assert test_file.read_text() == content


def test_preview_changes():
    """Test anteprima modifiche"""
    with tempfile.TemporaryDirectory() as tmpdir:
        patcher = Patcher(tmpdir)
        
        # Crea un file iniziale
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("old content\n")
        
        # Genera anteprima
        new_content = "new content\n"
        preview = patcher.preview_changes("test.py", new_content)
        
        assert preview is not None
        assert len(preview) > 0


if __name__ == '__main__':
    # Esegui i test
    test_patcher_creation()
    print("✓ test_patcher_creation")
    
    test_create_diff()
    print("✓ test_create_diff")
    
    test_extract_code_blocks()
    print("✓ test_extract_code_blocks")
    
    test_extract_multiple_code_blocks()
    print("✓ test_extract_multiple_code_blocks")
    
    test_parse_file_instruction()
    print("✓ test_parse_file_instruction")
    
    test_apply_patch()
    print("✓ test_apply_patch")
    
    test_preview_changes()
    print("✓ test_preview_changes")
    
    print("\n✓ Tutti i test del Patcher passati!")
