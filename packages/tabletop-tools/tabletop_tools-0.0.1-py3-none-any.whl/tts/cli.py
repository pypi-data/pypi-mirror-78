# -*- coding: utf-8 -*-

from pathlib import Path

from .utils.cli import CLI

app = CLI("Interact with Tabletop Simulator mods")


@app.command("unpack", help="Unpack a tts mod.")
@app.argument(
    "savegame", type=Path,
)
def unpack(options):
    from .unpack import unpack
    from .config import config

    unpack(savegame=options["savegame"], config=config)


@app.command("repack", help="Repack a tts mod.")
@app.argument(
    "savegame", type=Path, nargs="?", default="build/savegame.json",
)
def repack(options):
    from .repack import repack
    from .config import config

    repack(savegame=options["savegame"], config=config)


main = app.main
