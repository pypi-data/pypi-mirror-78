import json
from pathlib import Path
from typing import Any, Dict, List

from .config import Config
from .utils.formats import format_json


def repack_objects(base_path: Path) -> List[Dict[str, Any]]:
    objects = []
    index_path = base_path.joinpath("index.list")
    if not index_path.is_file():
        return []
    index = index_path.read_text().splitlines()
    for guid in index:
        path = base_path.joinpath(guid)
        if not path.is_dir():
            raise Exception("Objects must be directories")
        obj = json.loads(path.joinpath("object.json").read_text())
        obj["GUID"] = guid
        script_path = path.joinpath("script.lua")
        if script_path.exists():
            obj["LuaScript"] = script_path.read_text()
        else:
            obj["LuaScript"] = ""
        if path.joinpath("contained").is_dir():
            obj["ContainedObjects"] = repack_objects(path.joinpath("contained"))

        objects.append(obj)
    return objects


def repack(*, savegame: Path, config: Config) -> None:
    game = json.loads(config.savegame.read_text())

    global_script = config.global_script.read_text()
    game["LuaScript"] = global_script

    script_state = json.loads(config.script_state.read_text())
    game["LuaScriptState"] = json.dumps(script_state)

    note = config.note.read_text()
    game["Note"] = note

    xml_ui = config.xml_ui.read_text()
    game["XmlUI"] = xml_ui

    game["ObjectStates"] = repack_objects(config.objects)

    if not savegame.parent.exists():
        savegame.parent.mkdir(parents=True)
    savegame.write_text(format_json(game))
