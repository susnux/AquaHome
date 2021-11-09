from flask import Blueprint
from DCX2496 import DCX2496, Channel, TransmitMode


dcx_bp = Blueprint('dcx', __name__)


# Some defines
CHANNEL_SUB = Channel.OUTPUT_1
CHANNEL_L = Channel.OUTPUT_2
CHANNEL_R = Channel.OUTPUT_3
CHANNEL_BAR = Channel.OUTPUT_4
CHANNEL_FLOOR = Channel.OUTPUT_5
CHANNEL_SMOKE = Channel.OUTPUT_6

SOCKET = "localhost:6666"
# unix:///run/dcx2496"

# Other stuff
_dcx = None


def create_dcx():
    global _dcx
    if _dcx is None:
        _dcx = DCX2496(SOCKET)
        _dcx.transmit_mode(TransmitMode.REMOTE_RECEIVE)
    return _dcx

@dcx_bp.route("/api/dcx/subwoofer/mute")
@dcx_bp.route("/api/dcx/subwoofer/mute/<int:mute>", methods=["GET", "POST"])
def mute_subwoofer(mute=None):
    dcx = create_dcx()
    if mute is None:
        dcx.dump()
        return {"data": dcx.channels[CHANNEL_SUB].muted}
    else:
        dcx.channels[CHANNEL_SUB].mute().send()


@dcx_bp.route("/api/dcx/bar/mute")
@dcx_bp.route("/api/dcx/bar/mute/<int:mute>", methods=["GET", "POST"])
def mute_bar(mute=None):
    dcx = create_dcx()
    if mute is None:
        dcx.dump()
        return {"data": dcx.channels[CHANNEL_BAR].muted}
    else:
        dcx.channels[CHANNEL_BAR].mute().send()


@dcx_bp.route("/api/dcx/bar/gain")
@dcx_bp.route("/api/dcx/bar/gain/<gain>", methods=["GET", "POST"])
def bar_gain(gain=None):
    dcx = create_dcx()
    if gain is None:
        dcx.dump()
        return {"data": dcx.channels[CHANNEL_BAR].gain}
    else:
        gain = float(gain)
        # Clamp value
        gain = max(min(gain, 3), -12)
        dcx.channels[CHANNEL_BAR].set_gain(gain)
        return {"data": gain}


@dcx_bp.route("/api/dcx/floor/gain")
@dcx_bp.route("/api/dcx/floor/gain/<gain>", methods=["GET", "POST"])
def floor_gain(gain=None):
    dcx = create_dcx()
    if gain is None:
        dcx.dump()
        return {"data": dcx.channels[CHANNEL_FLOOR].gain}
    else:
        gain = float(gain)
        # Clamp value
        gain = max(min(gain, 3), -12)
        dcx.channels[CHANNEL_FLOOR].set_gain(gain)
        return {"data": gain}
