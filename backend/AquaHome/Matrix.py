from flask import Blueprint, request, make_response
from pythonosc.udp_client import SimpleUDPClient
from enum import IntEnum
from .db import get_db

ADDRESS = "djpult.lan"
PORT = 8000

# MODES


class Mode(IntEnum):
    blackout = 0
    manual = 1
    color = 2
    fade = 3
    rainbow = 4
    text = 5
    fish_tank = 6


# /MODES
matrix_bp = Blueprint('matrix', __name__)


def _set_mode(mode: Mode, data=None):
    osc = SimpleUDPClient(ADDRESS, PORT)
    osc.send_message("/djpult/mode", [mode, data] if not isinstance(data, list) else [mode, *data])
    return {"ok": True}


@matrix_bp.route("/api/matrix/blackout", methods=["POST"])
def set_blackout():
    return _set_mode(Mode.blackout)


@matrix_bp.route("/api/matrix/brightness", methods=["POST"])
def set_brightness():
    data = request.get_json()
    if data and "value" in data:
        osc = SimpleUDPClient(ADDRESS, PORT)
        osc.send_message("/djpult/brightness", int(data["value"]))
        return {"ok": True}
    return make_response({"ok": False}, 400)


@matrix_bp.route("/api/matrix/speed", methods=["POST"])
def set_speed():
    data = request.get_json()
    if data and "value" in data:
        osc = SimpleUDPClient(ADDRESS, PORT)
        osc.send_message("/djpult/speed", int(data["value"]))
        return {"ok": True}
    return make_response({"ok": False}, 400)


@matrix_bp.route("/api/matrix/mode", methods=["POST"])
def set_mode():
    data = request.get_json()
    if data and "mode" in data:
        mode = data["mode"]
        prefs = data.get("prefs", {})
        if mode == "blackout":
            return _set_mode(Mode.blackout)
        elif mode == "color":
            return _set_mode(Mode.color, prefs.get("color", None))
        elif mode == "fade":
            return _set_mode(Mode.fade)
        elif mode == "rainbow":
            return _set_mode(Mode.rainbow, prefs.get("vertical", False))
        elif mode == "fish_tank":
            return _set_mode(Mode.fish_tank)
        elif mode == "text":
            l = [prefs["background"]] if "background" in prefs else []
            if "color" in prefs:
                l.append(prefs["color"])
                if "font" in prefs:
                    l.append(prefs["font"])
                    if "text" in prefs:
                        l.append(prefs["text"])
            return _set_mode(Mode.text, l)
    return make_response({"ok": False}, 400)


@matrix_bp.route("/api/matrix/prefs", methods=["POST"])
def set_prefs():
    data = request.get_json()
    if data:
        osc = SimpleUDPClient(ADDRESS, PORT)
        for pref in data:
            if pref == "pixels":
                pixels = bytearray()
                for i in data[pref]:
                    pixels.extend([i >> 16, i >> 8 & 0xf, i & 0xf])
                osc.send_message(f"/djpult/mode/{pref}", bytes(pixels))
            else:
                osc.send_message(f"/djpult/mode/{pref}", data[pref])
        return {"ok": True}
    return make_response({"ok": False}, 400)


@matrix_bp.route("/api/matrix/status", methods=["GET"])
def get_status():
    con = get_db()
    cur = con.cursor()
    row = cur.execute("select mode, brightness, speed from matrix limit 1").fetchone()
    cur.close()
    if row:
        mode = Mode(row[0])
        return {"ok": True, "mode": mode.name, "brightness": row[1], "speed": row[2]}
    return make_response({"ok": False}, 400)
