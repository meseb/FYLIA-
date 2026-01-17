#!/usr/bin/env python3
"""
CLI entry point per FYLIA
Comandi disponibili: chat, map
"""

import click
from fylia import __version__


@click.group()
@click.version_option(version=__version__)
def cli():
    """FYLIA - Ambiente di sviluppo conversazionale"""
    pass


@cli.command()
def chat():
    """Avvia l'interfaccia TUI a 3 pannelli"""
    from fylia.tui import run_tui
    run_tui()


@cli.command()
@click.argument('path', default='.')
def map(path):
    """Mostra la mappa concettuale del progetto"""
    from fylia.mapgen import CodeMapGenerator
    
    generator = CodeMapGenerator()
    mappa = generator.generate_map(path)
    click.echo(mappa)


if __name__ == '__main__':
    cli()
