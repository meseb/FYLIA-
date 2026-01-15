"""
TUI - Interfaccia testuale a pannelli
Gestisce l'interfaccia a 3 pannelli: chat, output, mappa
"""

import sys
from typing import Optional
from .providers.mock import MockProvider
from .mapgen import MapGenerator
from .patcher import Patcher


class SimpleTUI:
    """
    Interfaccia testuale semplificata per FYLIA
    Versione base che funziona senza dipendenze esterne complesse
    """
    
    def __init__(self, root_path: str = '.'):
        self.provider = MockProvider()
        self.mapgen = MapGenerator(root_path)
        self.patcher = Patcher(root_path)
        self.root_path = root_path
        self.running = False
        self.code_map = None
    
    def start(self):
        """Avvia l'interfaccia TUI"""
        self.running = True
        self._print_header()
        self._show_welcome()
        
        # Genera la mappa iniziale
        print("\n⏳ Generazione mappa del progetto...")
        self.code_map = self.mapgen.generate_map()
        print("✓ Mappa generata\n")
        
        self._main_loop()
    
    def _print_header(self):
        """Stampa l'intestazione"""
        print("=" * 70)
        print(" " * 25 + "FYLIA v0.1.0")
        print(" " * 15 + "Sviluppo conversazionale in Termux")
        print("=" * 70)
    
    def _show_welcome(self):
        """Mostra messaggio di benvenuto"""
        print("\n👋 Benvenuto in FYLIA!")
        print("\nComandi disponibili:")
        print("  /map    - Mostra la mappa del progetto")
        print("  /stats  - Mostra statistiche del progetto")
        print("  /help   - Mostra questo messaggio")
        print("  /exit   - Esci da FYLIA")
        print("\nScrivi un messaggio per iniziare la conversazione...")
    
    def _main_loop(self):
        """Loop principale dell'interfaccia"""
        while self.running:
            try:
                # Prompt per l'input
                print("\n" + "-" * 70)
                user_input = input("Tu: ").strip()
                
                if not user_input:
                    continue
                
                # Gestisci comandi speciali
                if user_input.startswith('/'):
                    self._handle_command(user_input)
                else:
                    # Invia il messaggio al provider
                    self._handle_message(user_input)
            
            except KeyboardInterrupt:
                print("\n\n👋 Arrivederci!")
                self.running = False
            except EOFError:
                print("\n\n👋 Arrivederci!")
                self.running = False
    
    def _handle_command(self, command: str):
        """Gestisce i comandi speciali"""
        cmd = command.lower().split()[0]
        
        if cmd == '/exit' or cmd == '/quit':
            print("\n👋 Arrivederci!")
            self.running = False
        
        elif cmd == '/help':
            self._show_welcome()
        
        elif cmd == '/map':
            self._show_map()
        
        elif cmd == '/stats':
            self._show_stats()
        
        elif cmd == '/refresh':
            print("\n⏳ Rigenerazione mappa del progetto...")
            self.code_map = self.mapgen.generate_map()
            print("✓ Mappa aggiornata")
        
        else:
            print(f"\n⚠️  Comando sconosciuto: {cmd}")
            print("Usa /help per vedere i comandi disponibili")
    
    def _handle_message(self, message: str):
        """Gestisce un messaggio dell'utente"""
        # Mostra indicatore di pensiero
        print("\n💭 FYLIA sta pensando...")
        
        # Ottieni risposta dal provider
        response = self.provider.chat(message)
        
        # Mostra la risposta
        print("\n" + "=" * 70)
        print("FYLIA:")
        print("-" * 70)
        print(response)
        print("=" * 70)
        
        # Cerca istruzioni per creare/modificare file
        file_instruction = self.patcher.parse_file_instruction(response)
        if file_instruction:
            file_path, content = file_instruction
            print(f"\n📝 Rilevata istruzione per il file: {file_path}")
            
            # Mostra anteprima
            diff = self.patcher.preview_changes(file_path, content)
            if diff:
                print("\n📋 Anteprima modifiche:")
                print(self.patcher.format_diff_for_display(diff))
            
            # Chiedi conferma
            confirm = input("\n❓ Applicare le modifiche? (s/n): ").strip().lower()
            if confirm == 's' or confirm == 'si':
                if self.patcher.apply_patch(file_path, content):
                    print(f"✓ File {file_path} aggiornato con successo")
                    # Rigenera la mappa
                    self.code_map = self.mapgen.generate_map()
                else:
                    print("✗ Errore nell'applicare le modifiche")
    
    def _show_map(self):
        """Mostra la mappa del progetto"""
        if not self.code_map:
            print("\n⚠️  Mappa non disponibile")
            return
        
        print("\n" + "=" * 70)
        print("📊 MAPPA DEL PROGETTO")
        print("=" * 70)
        print(self.mapgen.format_tree(self.code_map))
        print("=" * 70)
    
    def _show_stats(self):
        """Mostra statistiche del progetto"""
        if not self.code_map:
            print("\n⚠️  Mappa non disponibile")
            return
        
        stats = self.mapgen.get_summary(self.code_map)
        
        print("\n" + "=" * 70)
        print("📈 STATISTICHE DEL PROGETTO")
        print("=" * 70)
        print(f"  📄 File Python:  {stats['files']}")
        print(f"  🏛️  Classi:       {stats['classes']}")
        print(f"  ⚙️  Funzioni:     {stats['functions']}")
        print(f"  🔧 Metodi:       {stats['methods']}")
        print("=" * 70)


def run_tui(root_path: str = '.'):
    """
    Funzione helper per avviare la TUI
    
    Args:
        root_path: Percorso radice del progetto da analizzare
    """
    tui = SimpleTUI(root_path)
    tui.start()
