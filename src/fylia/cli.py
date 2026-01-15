#!/usr/bin/env python3
"""
CLI - Interfaccia a riga di comando per FYLIA
Entry point per tutti i comandi del tool
"""

import argparse
import sys
from pathlib import Path
from .tui import run_tui
from .mapgen import MapGenerator
from .providers.mock import MockProvider
from . import __version__


def cmd_chat(args):
    """Comando: fylia chat - Avvia l'interfaccia conversazionale"""
    print(f"🚀 Avvio FYLIA chat in: {args.path}")
    run_tui(args.path)


def cmd_map(args):
    """Comando: fylia map - Genera e mostra la mappa del progetto"""
    print(f"📊 Generazione mappa del progetto: {args.path}")
    
    mapgen = MapGenerator(args.path)
    code_map = mapgen.generate_map()
    
    if args.format == 'tree':
        # Formato albero (default)
        print("\n" + "=" * 70)
        print(mapgen.format_tree(code_map))
        print("=" * 70)
    elif args.format == 'stats':
        # Solo statistiche
        stats = mapgen.get_summary(code_map)
        print("\n📈 Statistiche:")
        print(f"  📄 File Python:  {stats['files']}")
        print(f"  🏛️  Classi:       {stats['classes']}")
        print(f"  ⚙️  Funzioni:     {stats['functions']}")
        print(f"  🔧 Metodi:       {stats['methods']}")
    elif args.format == 'json':
        # Formato JSON
        import json
        print(json.dumps(code_map.to_dict(), indent=2, ensure_ascii=False))


def cmd_test(args):
    """Comando: fylia test - Testa il provider con un messaggio"""
    provider = MockProvider()
    
    if args.message:
        message = args.message
    else:
        print("Inserisci il tuo messaggio (premi Ctrl+D per inviare):")
        message = sys.stdin.read().strip()
    
    print("\n💭 Invio messaggio al provider...")
    response = provider.chat(message)
    
    print("\n" + "=" * 70)
    print("Risposta:")
    print("-" * 70)
    print(response)
    print("=" * 70)


def cmd_version(args):
    """Comando: fylia version - Mostra la versione"""
    print(f"FYLIA v{__version__}")
    print("Strumento di sviluppo conversazionale per Termux")


def main():
    """Entry point principale del CLI"""
    parser = argparse.ArgumentParser(
        prog='fylia',
        description='FYLIA - Sviluppo conversazionale in Termux',
        epilog='Per maggiori informazioni, visita: https://github.com/meseb/FYLIA-'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'FYLIA v{__version__}'
    )
    
    subparsers = parser.add_subparsers(
        title='comandi disponibili',
        dest='command',
        help='usa "fylia <comando> --help" per più informazioni'
    )
    
    # Comando: chat
    parser_chat = subparsers.add_parser(
        'chat',
        help='Avvia l\'interfaccia conversazionale (TUI)'
    )
    parser_chat.add_argument(
        '-p', '--path',
        default='.',
        help='Percorso del progetto (default: directory corrente)'
    )
    parser_chat.set_defaults(func=cmd_chat)
    
    # Comando: map
    parser_map = subparsers.add_parser(
        'map',
        help='Genera e mostra la mappa del progetto'
    )
    parser_map.add_argument(
        '-p', '--path',
        default='.',
        help='Percorso del progetto (default: directory corrente)'
    )
    parser_map.add_argument(
        '-f', '--format',
        choices=['tree', 'stats', 'json'],
        default='tree',
        help='Formato di output (default: tree)'
    )
    parser_map.set_defaults(func=cmd_map)
    
    # Comando: test
    parser_test = subparsers.add_parser(
        'test',
        help='Testa il provider con un messaggio'
    )
    parser_test.add_argument(
        '-m', '--message',
        help='Messaggio da inviare (se omesso, legge da stdin)'
    )
    parser_test.set_defaults(func=cmd_test)
    
    # Comando: version
    parser_version = subparsers.add_parser(
        'version',
        help='Mostra la versione di FYLIA'
    )
    parser_version.set_defaults(func=cmd_version)
    
    # Parse degli argomenti
    args = parser.parse_args()
    
    # Se nessun comando specificato, mostra help
    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)
    
    # Esegui il comando
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n\n👋 Operazione annullata")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Errore: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
