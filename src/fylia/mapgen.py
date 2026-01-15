"""
Generatore di mappe concettuali del codice
Analizza file Python e crea una rappresentazione della struttura del progetto
"""

import os
import ast
from pathlib import Path
from typing import Dict, List, Any


class CodeNode:
    """Rappresenta un nodo nella mappa del codice"""
    
    def __init__(self, name: str, node_type: str, line_number: int = 0):
        self.name = name
        self.node_type = node_type  # 'file', 'class', 'function', 'method'
        self.line_number = line_number
        self.children = []
    
    def add_child(self, child):
        """Aggiunge un nodo figlio"""
        self.children.append(child)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte il nodo in un dizionario"""
        return {
            'name': self.name,
            'type': self.node_type,
            'line': self.line_number,
            'children': [child.to_dict() for child in self.children]
        }


class MapGenerator:
    """Genera mappe concettuali del codice Python"""
    
    def __init__(self, root_path: str = '.'):
        self.root_path = Path(root_path)
    
    def generate_map(self) -> CodeNode:
        """
        Genera una mappa completa del progetto
        
        Returns:
            Un CodeNode radice contenente l'intera struttura
        """
        root = CodeNode(str(self.root_path), 'directory')
        self._scan_directory(self.root_path, root)
        return root
    
    def _scan_directory(self, path: Path, parent_node: CodeNode):
        """Scansiona ricorsivamente una directory"""
        try:
            items = sorted(path.iterdir())
        except PermissionError:
            return
        
        for item in items:
            # Ignora directory e file nascosti e comuni da escludere
            if item.name.startswith('.') or item.name in ['__pycache__', 'venv', 'env', 'node_modules']:
                continue
            
            if item.is_dir():
                dir_node = CodeNode(item.name, 'directory')
                parent_node.add_child(dir_node)
                self._scan_directory(item, dir_node)
            
            elif item.suffix == '.py':
                file_node = self._analyze_python_file(item)
                if file_node:
                    parent_node.add_child(file_node)
    
    def _analyze_python_file(self, file_path: Path) -> CodeNode:
        """
        Analizza un file Python ed estrae classi e funzioni
        
        Args:
            file_path: Percorso del file da analizzare
            
        Returns:
            CodeNode rappresentante il file con i suoi contenuti
        """
        file_node = CodeNode(file_path.name, 'file')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.ClassDef):
                    class_node = CodeNode(node.name, 'class', node.lineno)
                    
                    # Estrai metodi della classe
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_node = CodeNode(item.name, 'method', item.lineno)
                            class_node.add_child(method_node)
                    
                    file_node.add_child(class_node)
                
                elif isinstance(node, ast.FunctionDef):
                    func_node = CodeNode(node.name, 'function', node.lineno)
                    file_node.add_child(func_node)
        
        except Exception as e:
            # In caso di errore, restituisci comunque il nodo del file
            error_node = CodeNode(f"[Errore: {str(e)}]", 'error')
            file_node.add_child(error_node)
        
        return file_node
    
    def format_tree(self, node: CodeNode, indent: int = 0, is_last: bool = True) -> str:
        """
        Formatta la mappa come albero testuale
        
        Args:
            node: Nodo da formattare
            indent: Livello di indentazione
            is_last: Se è l'ultimo figlio del genitore
            
        Returns:
            Stringa formattata come albero
        """
        lines = []
        
        # Simboli per l'albero
        if indent == 0:
            prefix = ""
            branch = ""
        else:
            prefix = "  " * (indent - 1)
            branch = "└─ " if is_last else "├─ "
        
        # Icone per tipo
        icons = {
            'directory': '📁',
            'file': '📄',
            'class': '🏛️',
            'function': '⚙️',
            'method': '🔧',
            'error': '⚠️'
        }
        
        icon = icons.get(node.node_type, '•')
        line_info = f" (L{node.line_number})" if node.line_number > 0 else ""
        
        lines.append(f"{prefix}{branch}{icon} {node.name}{line_info}")
        
        # Ricorsione sui figli
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            lines.append(self.format_tree(child, indent + 1, is_last_child))
        
        return "\n".join(lines)
    
    def get_summary(self, node: CodeNode) -> Dict[str, int]:
        """
        Genera statistiche sulla mappa
        
        Returns:
            Dizionario con conteggi per tipo
        """
        stats = {
            'files': 0,
            'classes': 0,
            'functions': 0,
            'methods': 0
        }
        
        def count_recursive(n: CodeNode):
            if n.node_type == 'file':
                stats['files'] += 1
            elif n.node_type == 'class':
                stats['classes'] += 1
            elif n.node_type == 'function':
                stats['functions'] += 1
            elif n.node_type == 'method':
                stats['methods'] += 1
            
            for child in n.children:
                count_recursive(child)
        
        count_recursive(node)
        return stats
