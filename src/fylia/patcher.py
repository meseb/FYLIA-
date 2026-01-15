"""
Patcher - Applica patch e diff ai file
Gestisce la modifica del codice esistente
"""

import os
import difflib
from pathlib import Path
from typing import List, Tuple, Optional


class Patcher:
    """Gestisce l'applicazione di patch ai file"""
    
    def __init__(self, root_path: str = '.'):
        self.root_path = Path(root_path)
    
    def create_diff(self, file_path: str, old_content: str, new_content: str) -> str:
        """
        Crea un diff unificato tra due versioni di un file
        
        Args:
            file_path: Percorso del file
            old_content: Contenuto originale
            new_content: Nuovo contenuto
            
        Returns:
            Diff in formato unificato
        """
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}",
            lineterm='\n'
        )
        
        return ''.join(diff)
    
    def apply_patch(self, file_path: str, new_content: str, backup: bool = True) -> bool:
        """
        Applica una modifica a un file
        
        Args:
            file_path: Percorso del file da modificare
            new_content: Nuovo contenuto del file
            backup: Se True, crea un backup del file originale
            
        Returns:
            True se l'operazione ha successo, False altrimenti
        """
        full_path = self.root_path / file_path
        
        try:
            # Crea directory se non esiste
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Backup del file originale se esiste
            if backup and full_path.exists():
                backup_path = full_path.with_suffix(full_path.suffix + '.backup')
                with open(full_path, 'r', encoding='utf-8') as f:
                    old_content = f.read()
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(old_content)
            
            # Scrivi il nuovo contenuto
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
        
        except Exception as e:
            print(f"Errore nell'applicare la patch: {e}")
            return False
    
    def preview_changes(self, file_path: str, new_content: str) -> str:
        """
        Mostra un'anteprima delle modifiche che verranno applicate
        
        Args:
            file_path: Percorso del file
            new_content: Nuovo contenuto proposto
            
        Returns:
            Diff formattato per la visualizzazione
        """
        full_path = self.root_path / file_path
        
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                old_content = f.read()
        else:
            old_content = ""
        
        return self.create_diff(file_path, old_content, new_content)
    
    def extract_code_blocks(self, text: str) -> List[Tuple[str, str]]:
        """
        Estrae blocchi di codice da un testo markdown
        
        Args:
            text: Testo che può contenere blocchi di codice in formato ```
            
        Returns:
            Lista di tuple (linguaggio, codice)
        """
        blocks = []
        lines = text.split('\n')
        in_block = False
        current_lang = ""
        current_code = []
        
        for line in lines:
            if line.startswith('```'):
                if in_block:
                    # Fine del blocco
                    blocks.append((current_lang, '\n'.join(current_code)))
                    current_code = []
                    current_lang = ""
                    in_block = False
                else:
                    # Inizio del blocco
                    current_lang = line[3:].strip()
                    in_block = True
            elif in_block:
                current_code.append(line)
        
        return blocks
    
    def parse_file_instruction(self, text: str) -> Optional[Tuple[str, str]]:
        """
        Cerca nel testo istruzioni per creare/modificare file
        
        Formato atteso:
        File: path/to/file.py
        ```python
        codice...
        ```
        
        Args:
            text: Testo da analizzare
            
        Returns:
            Tupla (file_path, content) o None se non trovato
        """
        lines = text.split('\n')
        file_path = None
        
        # Cerca una linea che inizia con "File:" o simili
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            if line_lower.startswith('file:') or line_lower.startswith('path:'):
                # Estrai il path
                file_path = line.split(':', 1)[1].strip()
                # Cerca il blocco di codice che segue
                remaining_text = '\n'.join(lines[i+1:])
                blocks = self.extract_code_blocks(remaining_text)
                if blocks:
                    return (file_path, blocks[0][1])
        
        return None
    
    def format_diff_for_display(self, diff: str) -> str:
        """
        Formatta un diff per la visualizzazione nella TUI
        
        Args:
            diff: Diff grezzo
            
        Returns:
            Diff formattato con colori (ANSI codes)
        """
        lines = diff.split('\n')
        formatted = []
        
        for line in lines:
            if line.startswith('+') and not line.startswith('+++'):
                # Linee aggiunte in verde
                formatted.append(f"\033[32m{line}\033[0m")
            elif line.startswith('-') and not line.startswith('---'):
                # Linee rimosse in rosso
                formatted.append(f"\033[31m{line}\033[0m")
            elif line.startswith('@@'):
                # Intestazioni in ciano
                formatted.append(f"\033[36m{line}\033[0m")
            else:
                formatted.append(line)
        
        return '\n'.join(formatted)
