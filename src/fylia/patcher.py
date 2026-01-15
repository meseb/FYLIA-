"""
Patcher - Sistema di applicazione patch e diff

Gestisce l'applicazione di modifiche ai file attraverso patch/diff.
"""
import os
from pathlib import Path
from typing import Optional
from unidiff import PatchSet


def apply_patch(patch_content: str, project_path: str = ".") -> dict:
    """
    Applica una patch al progetto
    
    Args:
        patch_content: Contenuto della patch in formato unified diff
        project_path: Percorso base del progetto
        
    Returns:
        Dizionario con risultati dell'operazione
    """
    results = {
        'success': False,
        'files_modified': [],
        'errors': []
    }
    
    try:
        patch_set = PatchSet(patch_content)
        
        for patched_file in patch_set:
            file_path = Path(project_path) / patched_file.path
            
            if patched_file.is_added_file:
                # Nuovo file
                result = create_new_file(file_path, patched_file)
                if result['success']:
                    results['files_modified'].append(str(file_path))
                else:
                    results['errors'].append(result['error'])
            
            elif patched_file.is_removed_file:
                # File da rimuovere
                result = remove_file(file_path)
                if result['success']:
                    results['files_modified'].append(str(file_path))
                else:
                    results['errors'].append(result['error'])
            
            else:
                # File da modificare
                result = modify_file(file_path, patched_file)
                if result['success']:
                    results['files_modified'].append(str(file_path))
                else:
                    results['errors'].append(result['error'])
        
        results['success'] = len(results['errors']) == 0
        
    except Exception as e:
        results['errors'].append(f"Errore nell'elaborazione della patch: {str(e)}")
    
    return results


def create_new_file(file_path: Path, patched_file) -> dict:
    """Crea un nuovo file"""
    try:
        # Crea le directory necessarie
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Estrai il contenuto dalle hunks
        content_lines = []
        for hunk in patched_file:
            for line in hunk:
                if line.is_added:
                    content_lines.append(line.value)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(content_lines)
        
        return {'success': True}
    
    except Exception as e:
        return {'success': False, 'error': f"Errore nella creazione di {file_path}: {str(e)}"}


def remove_file(file_path: Path) -> dict:
    """Rimuove un file"""
    try:
        if file_path.exists():
            file_path.unlink()
        return {'success': True}
    
    except Exception as e:
        return {'success': False, 'error': f"Errore nella rimozione di {file_path}: {str(e)}"}


def modify_file(file_path: Path, patched_file) -> dict:
    """Modifica un file esistente"""
    try:
        if not file_path.exists():
            return {'success': False, 'error': f"File non trovato: {file_path}"}
        
        # Leggi il file corrente
        with open(file_path, 'r', encoding='utf-8') as f:
            original_lines = f.readlines()
        
        # Applica le modifiche
        modified_lines = apply_hunks(original_lines, patched_file)
        
        # Scrivi il file modificato
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(modified_lines)
        
        return {'success': True}
    
    except Exception as e:
        return {'success': False, 'error': f"Errore nella modifica di {file_path}: {str(e)}"}


def apply_hunks(original_lines: list, patched_file) -> list:
    """
    Applica le modifiche (hunks) alle righe originali
    
    Args:
        original_lines: Righe del file originale
        patched_file: File patchato da unidiff
        
    Returns:
        Righe modificate
    """
    result_lines = original_lines.copy()
    offset = 0  # Offset per tenere traccia delle modifiche
    
    for hunk in patched_file:
        source_start = hunk.source_start - 1 + offset  # Le righe in diff partono da 1
        
        # Rimuovi le righe vecchie
        lines_to_remove = sum(1 for line in hunk if line.is_removed)
        if lines_to_remove > 0:
            del result_lines[source_start:source_start + lines_to_remove]
            offset -= lines_to_remove
        
        # Aggiungi le righe nuove
        new_lines = [line.value for line in hunk if line.is_added]
        for i, new_line in enumerate(new_lines):
            result_lines.insert(source_start + i, new_line)
            offset += 1
    
    return result_lines


def generate_diff(original_content: str, modified_content: str, filename: str = "file") -> str:
    """
    Genera un diff unified tra due contenuti
    
    Args:
        original_content: Contenuto originale
        modified_content: Contenuto modificato
        filename: Nome del file per l'intestazione del diff
        
    Returns:
        Diff in formato unified
    """
    import difflib
    
    original_lines = original_content.splitlines(keepends=True)
    modified_lines = modified_content.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        original_lines,
        modified_lines,
        fromfile=f"a/{filename}",
        tofile=f"b/{filename}",
        lineterm=''
    )
    
    return ''.join(diff)
