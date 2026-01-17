"""
Gestore di patch per applicare modifiche ai file
Supporta creazione, modifica e cancellazione di file
"""

import os
from pathlib import Path
from typing import Optional


class Patcher:
    """Applica patch e diff ai file del progetto"""
    
    def apply_patch(self, file_path: str, patch_content: str) -> bool:
        """
        Applica una patch a un file
        
        Args:
            file_path: percorso del file da modificare
            patch_content: contenuto della patch in formato unified diff
            
        Returns:
            True se la patch è stata applicata con successo
        """
        # Implementazione semplificata - supporto base
        try:
            path = Path(file_path)
            
            # Se il file non esiste, crealo
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(patch_content)
                return True
            
            # Altrimenti sovrascrivi (logica base)
            path.write_text(patch_content)
            return True
        
        except Exception as e:
            print(f"Errore nell'applicare la patch: {e}")
            return False
    
    def create_file(self, file_path: str, content: str) -> bool:
        """
        Crea un nuovo file con il contenuto specificato
        
        Args:
            file_path: percorso del file da creare
            content: contenuto del file
            
        Returns:
            True se il file è stato creato con successo
        """
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            return True
        except Exception as e:
            print(f"Errore nella creazione del file: {e}")
            return False
    
    def modify_file(self, file_path: str, old_content: str, new_content: str) -> bool:
        """
        Modifica un file sostituendo old_content con new_content
        
        Args:
            file_path: percorso del file da modificare
            old_content: contenuto da sostituire
            new_content: nuovo contenuto
            
        Returns:
            True se la modifica è stata applicata con successo
        """
        try:
            path = Path(file_path)
            if not path.exists():
                print(f"File non trovato: {file_path}")
                return False
            
            current_content = path.read_text()
            
            if old_content not in current_content:
                print(f"Contenuto da sostituire non trovato nel file")
                return False
            
            new_file_content = current_content.replace(old_content, new_content)
            path.write_text(new_file_content)
            return True
        
        except Exception as e:
            print(f"Errore nella modifica del file: {e}")
            return False
    
    def delete_file(self, file_path: str) -> bool:
        """
        Elimina un file
        
        Args:
            file_path: percorso del file da eliminare
            
        Returns:
            True se il file è stato eliminato con successo
        """
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                return True
            else:
                print(f"File non trovato: {file_path}")
                return False
        except Exception as e:
            print(f"Errore nell'eliminazione del file: {e}")
            return False
    
    def generate_diff(self, file_path: str, old_content: str, new_content: str) -> str:
        """
        Genera un diff tra vecchio e nuovo contenuto
        
        Args:
            file_path: percorso del file
            old_content: contenuto originale
            new_content: nuovo contenuto
            
        Returns:
            Stringa con il diff in formato leggibile
        """
        old_lines = old_content.splitlines()
        new_lines = new_content.splitlines()
        
        diff = []
        diff.append(f"--- {file_path} (originale)")
        diff.append(f"+++ {file_path} (modificato)")
        diff.append("@@ Differenze @@")
        
        # Diff semplificato linea per linea
        max_lines = max(len(old_lines), len(new_lines))
        
        for i in range(max_lines):
            old_line = old_lines[i] if i < len(old_lines) else ""
            new_line = new_lines[i] if i < len(new_lines) else ""
            
            if old_line != new_line:
                if old_line:
                    diff.append(f"- {old_line}")
                if new_line:
                    diff.append(f"+ {new_line}")
        
        return "\n".join(diff)
