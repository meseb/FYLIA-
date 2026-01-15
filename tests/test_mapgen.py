"""
Test per MapGenerator
"""

import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fylia.mapgen import MapGenerator, CodeNode


def test_code_node_creation():
    """Test creazione CodeNode"""
    node = CodeNode("test.py", "file", 1)
    assert node.name == "test.py"
    assert node.node_type == "file"
    assert node.line_number == 1
    assert len(node.children) == 0


def test_code_node_add_child():
    """Test aggiunta figli a CodeNode"""
    parent = CodeNode("parent", "directory")
    child = CodeNode("child.py", "file")
    parent.add_child(child)
    
    assert len(parent.children) == 1
    assert parent.children[0] == child


def test_code_node_to_dict():
    """Test conversione CodeNode a dizionario"""
    node = CodeNode("test.py", "file", 10)
    node.add_child(CodeNode("func1", "function", 15))
    
    d = node.to_dict()
    assert d['name'] == "test.py"
    assert d['type'] == "file"
    assert d['line'] == 10
    assert len(d['children']) == 1


def test_mapgen_creation():
    """Test creazione MapGenerator"""
    mapgen = MapGenerator()
    assert mapgen is not None


def test_mapgen_analyze_simple_file():
    """Test analisi file Python semplice"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Crea un file Python di test
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("""
def hello():
    return "Hello"

class TestClass:
    def method1(self):
        pass
""")
        
        mapgen = MapGenerator(tmpdir)
        file_node = mapgen._analyze_python_file(test_file)
        
        assert file_node.name == "test.py"
        assert file_node.node_type == "file"
        assert len(file_node.children) >= 2  # function + class


def test_mapgen_format_tree():
    """Test formattazione albero"""
    node = CodeNode("root", "directory")
    child = CodeNode("child.py", "file")
    node.add_child(child)
    
    mapgen = MapGenerator()
    tree = mapgen.format_tree(node)
    
    assert "root" in tree
    assert "child.py" in tree


def test_mapgen_get_summary():
    """Test statistiche"""
    root = CodeNode("root", "directory")
    file1 = CodeNode("file1.py", "file")
    class1 = CodeNode("Class1", "class", 10)
    func1 = CodeNode("func1", "function", 20)
    method1 = CodeNode("method1", "method", 15)
    
    file1.add_child(class1)
    file1.add_child(func1)
    class1.add_child(method1)
    root.add_child(file1)
    
    mapgen = MapGenerator()
    stats = mapgen.get_summary(root)
    
    assert stats['files'] == 1
    assert stats['classes'] == 1
    assert stats['functions'] == 1
    assert stats['methods'] == 1


if __name__ == '__main__':
    # Esegui i test
    test_code_node_creation()
    print("✓ test_code_node_creation")
    
    test_code_node_add_child()
    print("✓ test_code_node_add_child")
    
    test_code_node_to_dict()
    print("✓ test_code_node_to_dict")
    
    test_mapgen_creation()
    print("✓ test_mapgen_creation")
    
    test_mapgen_analyze_simple_file()
    print("✓ test_mapgen_analyze_simple_file")
    
    test_mapgen_format_tree()
    print("✓ test_mapgen_format_tree")
    
    test_mapgen_get_summary()
    print("✓ test_mapgen_get_summary")
    
    print("\n✓ Tutti i test del MapGenerator passati!")
