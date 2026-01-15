"""
TUI (Text User Interface) per FYLIA

Interfaccia a 3 pannelli:
- Sinistra: Chat conversazionale
- Centro: Editor/Diff del codice
- Destra: Mappa concettuale del progetto
"""
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Input, RichLog
from textual.binding import Binding
from fylia.mapgen import generate_map
from fylia.providers.mock import MockProvider


class ChatPanel(Vertical):
    """Pannello chat per la conversazione con l'assistente"""
    
    def compose(self) -> ComposeResult:
        yield Static("💬 Chat", classes="panel-title")
        yield RichLog(id="chat-log")
        yield Input(placeholder="Scrivi qui...", id="chat-input")


class EditorPanel(Vertical):
    """Pannello centrale per visualizzare codice e diff"""
    
    def compose(self) -> ComposeResult:
        yield Static("📝 Editor / Output", classes="panel-title")
        yield RichLog(id="editor-output")


class MapPanel(Vertical):
    """Pannello mappa concettuale del progetto"""
    
    def compose(self) -> ComposeResult:
        yield Static("🗺️  Mappa Progetto", classes="panel-title")
        yield RichLog(id="map-output")


class FyliaApp(App):
    """Applicazione principale FYLIA"""
    
    CSS = """
    Screen {
        layout: horizontal;
    }
    
    ChatPanel {
        width: 1fr;
        border: solid green;
    }
    
    EditorPanel {
        width: 2fr;
        border: solid blue;
    }
    
    MapPanel {
        width: 1fr;
        border: solid yellow;
    }
    
    .panel-title {
        background: $boost;
        color: $text;
        padding: 1;
        text-align: center;
    }
    
    TextLog {
        height: 1fr;
    }
    
    Input {
        dock: bottom;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Esci"),
        Binding("r", "refresh_map", "Aggiorna Mappa"),
    ]
    
    def __init__(self):
        super().__init__()
        self.provider = MockProvider()
        self.project_path = "."
    
    def compose(self) -> ComposeResult:
        """Crea la struttura dell'interfaccia"""
        yield Header()
        yield Horizontal(
            ChatPanel(),
            EditorPanel(),
            MapPanel(),
        )
        yield Footer()
    
    def on_mount(self) -> None:
        """Inizializzazione all'avvio"""
        self.query_one("#chat-log").write("Benvenuto in FYLIA! 👋")
        self.query_one("#chat-log").write("Scrivi qui sotto per iniziare...")
        self.refresh_map()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Gestisce l'invio di messaggi nella chat"""
        if event.input.id == "chat-input":
            user_message = event.value
            
            if not user_message.strip():
                return
            
            # Mostra il messaggio dell'utente
            chat_log = self.query_one("#chat-log")
            chat_log.write(f"Tu: {user_message}")
            
            # Ottieni risposta dal provider
            response = self.provider.get_response(user_message)
            chat_log.write(f"FYLIA: {response}")
            
            # Se c'è del codice generato, mostralo nell'editor
            if "```" in response:
                editor = self.query_one("#editor-output")
                editor.write("--- Codice Generato ---")
                editor.write(response)
            
            # Pulisci input
            event.input.value = ""
    
    def action_refresh_map(self) -> None:
        """Aggiorna la mappa concettuale"""
        self.refresh_map()
    
    def refresh_map(self) -> None:
        """Rigenera e mostra la mappa del progetto"""
        map_output = self.query_one("#map-output")
        map_output.clear()
        
        try:
            mappa = generate_map(self.project_path)
            map_output.write(mappa)
        except Exception as e:
            map_output.write(f"Errore nella generazione della mappa: {e}")
