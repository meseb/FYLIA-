from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static, Input

class ChatPanel(Static):
    """Pannello chat a sinistra per input utente."""
    def compose(self) -> ComposeResult:
        yield Static("Chat: Scrivi la tua richiesta qui.")
        yield Input(placeholder="Inserisci testo...")

class OutputPanel(Static):
    """Pannello output al centro per risultati."""
    def compose(self) -> ComposeResult:
        yield Static("Output: Qui appariranno i risultati.")

class MapPanel(Static):
    """Pannello mappa a destra per struttura progetto."""
    def compose(self) -> ComposeResult:
        yield Static("Mappa: Struttura del progetto.")

class FyliaTUI(App):
    """App principale TUI per FYLIA."""
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield ChatPanel()
            yield OutputPanel()
            yield MapPanel()


def run_tui():
    """Lancia la TUI."""
    app = FyliaTUI()
    app.run()