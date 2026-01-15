"""
Interfaccia TUI a 3 pannelli per FYLIA
- Pannello sinistro: input chat utente
- Pannello centrale: output/codice generato
- Pannello destro: mappa concettuale del progetto
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, TextArea, Static, Input
from textual.binding import Binding
from fylia.providers.mock import MockProvider
from fylia.mapgen import CodeMapGenerator
import os


class FyliaApp(App):
    """Applicazione TUI principale di FYLIA"""
    
    CSS = """
    #chat-panel {
        width: 30%;
        border: solid green;
    }
    
    #output-panel {
        width: 40%;
        border: solid blue;
    }
    
    #map-panel {
        width: 30%;
        border: solid yellow;
    }
    
    .panel-content {
        height: 100%;
        overflow-y: scroll;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+c", "quit", "Esci"),
        Binding("ctrl+r", "refresh_map", "Aggiorna mappa"),
    ]
    
    def __init__(self):
        super().__init__()
        self.provider = MockProvider()
        self.map_generator = CodeMapGenerator()
        self.chat_history = []
    
    def compose(self) -> ComposeResult:
        """Crea il layout a 3 pannelli"""
        yield Header()
        
        with Horizontal():
            with Container(id="chat-panel"):
                yield Static("💬 Chat\n" + "─" * 20, classes="panel-header")
                yield Static("", id="chat-content", classes="panel-content")
                yield Input(placeholder="Scrivi qui cosa vuoi costruire...", id="chat-input")
            
            with Container(id="output-panel"):
                yield Static("📝 Output / Codice\n" + "─" * 20, classes="panel-header")
                yield Static("Benvenuto in FYLIA!\nScrivi nella chat cosa vuoi costruire.", 
                           id="output-content", classes="panel-content")
            
            with Container(id="map-panel"):
                yield Static("🗺️  Mappa Progetto\n" + "─" * 20, classes="panel-header")
                yield Static("", id="map-content", classes="panel-content")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Inizializza l'app al caricamento"""
        self.refresh_map()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Gestisce l'invio di un messaggio nella chat"""
        user_input = event.value
        if not user_input.strip():
            return
        
        # Aggiungi alla chat history
        self.chat_history.append(f"Tu: {user_input}")
        
        # Ottieni risposta dal provider
        response = self.provider.generate_response(user_input)
        self.chat_history.append(f"FYLIA: {response}")
        
        # Aggiorna i pannelli
        chat_widget = self.query_one("#chat-content", Static)
        chat_widget.update("\n".join(self.chat_history[-10:]))  # Mostra ultime 10 righe
        
        output_widget = self.query_one("#output-content", Static)
        output_widget.update(response)
        
        # Pulisci input
        event.input.value = ""
    
    def action_refresh_map(self) -> None:
        """Aggiorna la mappa del progetto"""
        self.refresh_map()
    
    def refresh_map(self) -> None:
        """Genera e mostra la mappa del progetto corrente"""
        current_dir = os.getcwd()
        mappa = self.map_generator.generate_map(current_dir)
        
        map_widget = self.query_one("#map-content", Static)
        map_widget.update(mappa)


def run_tui():
    """Avvia l'interfaccia TUI"""
    app = FyliaApp()
    app.run()
