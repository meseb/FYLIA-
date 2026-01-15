"""
CLI Entry Point per FYLIA

Gestisce i comandi della linea di comando e avvia l'interfaccia TUI.
"""
import click
from fylia.tui import FyliaApp


@click.group()
@click.version_option()
def main():
    """FYLIA - Programmare parlando, capire programmando"""
    pass


@main.command()
def chat():
    """Avvia l'interfaccia conversazionale di FYLIA"""
    app = FyliaApp()
    app.run()


@main.command()
@click.argument('path', default='.')
def map(path):
    """Mostra la mappa concettuale del progetto"""
    from fylia.mapgen import generate_map
    
    mappa = generate_map(path)
    click.echo(mappa)


if __name__ == "__main__":
    main()
