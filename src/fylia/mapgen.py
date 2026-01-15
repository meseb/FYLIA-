"""
Generatore di mappa concettuale del codice
Analizza la struttura dei file e del codice Python
"""

import os
import ast
from pathlib import Path


class CodeMapGenerator:
    """Genera una mappa della struttura del progetto"""
    
    def __init__(self):
        self.ignore_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.tox'}
        self.ignore_files = {'.DS_Store', '.gitignore'}
    
    def generate_map(self, root_path: str) -> str:
        """Genera la mappa completa del progetto"""
        root = Path(root_path)
        
        if not root.exists():
            return f"❌ Percorso non trovato: {root_path}"
        
        output = []
        output.append("╔═══════════════════════════════╗")
        output.append("║   MAPPA PROGETTO FYLIA       ║")
        output.append("╚═══════════════════════════════╝")
        output.append("")
        output.append("📁 Struttura File:")
        
        # Genera albero dei file
        file_tree = self._generate_file_tree(root)
        output.append(file_tree)
        
        output.append("")
        output.append("🐍 Struttura Python:")
        
        # Analizza file Python
        python_structure = self._analyze_python_files(root)
        output.append(python_structure)
        
        return "\n".join(output)
    
    def _generate_file_tree(self, root: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0) -> str:
        """Genera un albero dei file"""
        if current_depth >= max_depth:
            return ""
        
        output = []
        
        try:
            items = sorted(root.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            items = [item for item in items if item.name not in self.ignore_files and item.name not in self.ignore_dirs]
        except PermissionError:
            return ""
        
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "
            
            if item.is_dir():
                output.append(f"{prefix}{connector}📁 {item.name}/")
                if item.name not in self.ignore_dirs:
                    extension = "    " if is_last else "│   "
                    subtree = self._generate_file_tree(item, prefix + extension, max_depth, current_depth + 1)
                    if subtree:
                        output.append(subtree)
            else:
                icon = self._get_file_icon(item.name)
                output.append(f"{prefix}{connector}{icon} {item.name}")
        
        return "\n".join(output)
    
    def _get_file_icon(self, filename: str) -> str:
        """Restituisce un'icona per il tipo di file"""
        ext = filename.split('.')[-1].lower() if '.' in filename else ''
        
        icons = {
            'py': '🐍',
            'md': '📝',
            'txt': '📄',
            'json': '📋',
            'yaml': '⚙️',
            'yml': '⚙️',
            'toml': '⚙️',
            'sh': '🔧',
        }
        
        return icons.get(ext, '📄')
    
    def _analyze_python_files(self, root: Path) -> str:
        """Analizza file Python per estrarre classi e funzioni"""
        output = []
        
        for py_file in root.rglob('*.py'):
            if any(ignored in py_file.parts for ignored in self.ignore_dirs):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read(), filename=str(py_file))
                
                classes = []
                functions = []
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                        classes.append((node.name, methods))
                    elif isinstance(node, ast.FunctionDef) and isinstance(node, ast.FunctionDef):
                        # Solo funzioni top-level (non metodi)
                        if not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree)):
                            functions.append(node.name)
                
                if classes or functions:
                    rel_path = py_file.relative_to(root)
                    output.append(f"\n📄 {rel_path}")
                    
                    for class_name, methods in classes:
                        output.append(f"  🔷 class {class_name}")
                        for method in methods[:5]:  # Mostra max 5 metodi
                            output.append(f"    ├─ {method}()")
                        if len(methods) > 5:
                            output.append(f"    └─ ... (+{len(methods)-5} metodi)")
                    
                    for func in functions[:5]:  # Mostra max 5 funzioni
                        output.append(f"  🔹 def {func}()")
                    if len(functions) > 5:
                        output.append(f"  └─ ... (+{len(functions)-5} funzioni)")
            
            except (SyntaxError, UnicodeDecodeError):
                continue
        
        if not output:
            output.append("Nessun file Python trovato o analizzabile.")
        
        return "\n".join(output)
