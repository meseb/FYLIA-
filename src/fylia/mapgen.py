"""
Map Generator - Generatore di Mappa Concettuale

Analizza il progetto e genera una mappa della struttura:
- Albero dei file
- Funzioni e classi estratte dai file Python
"""
import ast
import os
from pathlib import Path
from typing import List, Dict, Any


def generate_map(project_path: str = ".") -> str:
    """
    Genera una rappresentazione testuale della struttura del progetto
    
    Args:
        project_path: Percorso della directory del progetto
        
    Returns:
        Stringa formattata con la mappa del progetto
    """
    path = Path(project_path).resolve()
    
    if not path.exists():
        return f"Errore: Il percorso {project_path} non esiste"
    
    lines = [
        "╔═══════════════════════════════╗",
        "║   MAPPA PROGETTO FYLIA       ║",
        "╚═══════════════════════════════╝",
        "",
    ]
    
    # Genera albero dei file
    lines.append("📁 Struttura File:")
    lines.append("")
    file_tree = generate_file_tree(path)
    lines.extend(file_tree)
    
    lines.append("")
    lines.append("─" * 40)
    lines.append("")
    
    # Analizza file Python
    lines.append("🐍 Struttura Python:")
    lines.append("")
    python_structure = analyze_python_files(path)
    lines.extend(python_structure)
    
    return "\n".join(lines)


def generate_file_tree(path: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0) -> List[str]:
    """
    Genera un albero della struttura dei file
    
    Args:
        path: Percorso da analizzare
        prefix: Prefisso per l'indentazione
        max_depth: Profondità massima di ricorsione
        current_depth: Profondità corrente
        
    Returns:
        Lista di stringhe che rappresentano l'albero
    """
    if current_depth >= max_depth:
        return []
    
    lines = []
    
    try:
        items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
        
        # Filtra file nascosti e directory comuni da ignorare
        items = [
            item for item in items 
            if not item.name.startswith('.') and 
            item.name not in ['__pycache__', 'node_modules', 'venv', 'env']
        ]
        
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            
            if item.is_dir():
                lines.append(f"{prefix}{current_prefix}📁 {item.name}/")
                # Ricorsione per le sottodirectory
                extension = "    " if is_last else "│   "
                lines.extend(
                    generate_file_tree(item, prefix + extension, max_depth, current_depth + 1)
                )
            else:
                icon = get_file_icon(item.suffix)
                lines.append(f"{prefix}{current_prefix}{icon} {item.name}")
    
    except PermissionError:
        lines.append(f"{prefix}[Accesso negato]")
    
    return lines


def get_file_icon(suffix: str) -> str:
    """Restituisce un'icona appropriata per il tipo di file"""
    icons = {
        '.py': '🐍',
        '.md': '📝',
        '.txt': '📄',
        '.json': '📋',
        '.yaml': '⚙️',
        '.yml': '⚙️',
        '.toml': '⚙️',
        '.sh': '💻',
    }
    return icons.get(suffix, '📄')


def analyze_python_files(path: Path) -> List[str]:
    """
    Analizza i file Python e estrae funzioni e classi
    
    Args:
        path: Percorso della directory da analizzare
        
    Returns:
        Lista di stringhe con la struttura Python trovata
    """
    lines = []
    python_files = list(path.rglob("*.py"))
    
    # Filtra file in directory da ignorare
    python_files = [
        f for f in python_files 
        if not any(part.startswith('.') or part in ['__pycache__', 'venv', 'env'] 
                  for part in f.parts)
    ]
    
    if not python_files:
        lines.append("  Nessun file Python trovato")
        return lines
    
    for py_file in python_files[:10]:  # Limita a 10 file per non sovraccaricare
        try:
            relative_path = py_file.relative_to(path)
            structure = parse_python_file(py_file)
            
            if structure:
                lines.append(f"📄 {relative_path}")
                lines.extend(structure)
                lines.append("")
        
        except Exception as e:
            lines.append(f"  Errore nell'analisi di {py_file.name}: {e}")
    
    return lines


def parse_python_file(file_path: Path) -> List[str]:
    """
    Analizza un file Python ed estrae classi e funzioni
    
    Args:
        file_path: Percorso del file Python
        
    Returns:
        Lista di stringhe con la struttura del file
    """
    lines = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [
                    m.name for m in node.body 
                    if isinstance(m, ast.FunctionDef)
                ]
                lines.append(f"  🔷 class {node.name}")
                for method in methods:
                    lines.append(f"    ├─ {method}()")
            
            elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                # Solo funzioni top-level (non metodi)
                lines.append(f"  🔹 def {node.name}()")
    
    except SyntaxError:
        lines.append("  [Errore di sintassi nel file]")
    except Exception as e:
        lines.append(f"  [Errore: {e}]")
    
    return lines
