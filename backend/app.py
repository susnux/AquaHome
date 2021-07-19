from flask import Flask, request
from pulsectl import Pulse
from DCX2496 import DCX2496, Channel, TransmitMode


# Some defines
CHANNEL_SUB = Channel.OUTPUT_1
CHANNEL_L = Channel.OUTPUT_2
CHANNEL_R = Channel.OUTPUT_3
CHANNEL_BAR = Channel.OUTPUT_4
CHANNEL_ROOM = Channel.OUTPUT_5
CHANNEL_SMOKE = Channel.OUTPUT_6

SOCKET = "unix:///run/dcx2496"

# Other stuff
_dcx = None


def create_dcx():
    global _dcx
    if _dcx is None:
        _dcx = DCX2496(SOCKET)
        _dcx.transmit_mode(TransmitMode.REMOTE_RECEIVE)
    return _dcx


def pulse_volume(limit=None):
    with Pulse("AquaHome") as pulse:
        sink_input = pulse.sink_list()[0]
        volume = sink_input.volume
        if limit is not None:
            volume.value_flat = limit
            pulse.volume_set(sink_input, volume)
        return volume.value_flat


# Some flask shit starting here
app = Flask(__name__)


@app.route("/api/pi/mute/")
@app.route("/api/pi/mute/<int:i>", methods=["GET", "POST"])
def mute_pi(i=None):
    if i is not None:
        pulse_volume(0.0 if i == 1 else 0.6)
        return {"data": i == 1}
    else:
        return {"data": pulse_volume() < 0.01}


@app.route("/api/pi/limit/")
@app.route("/api/pi/limit/<int:i>", methods=["GET", "POST"])
def limit_pi(i=None):
    if i is not None:
        pulse_volume(1.0 if i == 0 else 0.6)
        return {"data": i == 1}
    else:
        return {"data": pulse_volume() < 0.98}


@app.route("/api/dcx/subwoofer/mute")
@app.route("/api/dcx/subwoofer/mute/<int:mute>", methods=["GET", "POST"])
def mute_subwoofer(mute=None):
    dcx = create_dcx()
    if mute is None:
        dcx.dump()
        return {"data": dcx.channels[CHANNEL_SUB].muted}
    else:
        dcx.channels[CHANNEL_SUB].mute().send()


@app.route("/api/dcx/bar/mute")
@app.route("/api/dcx/bar/mute/<int:mute>", methods=["GET", "POST"])
def mute_bar(mute=None):
    dcx = create_dcx()
    if mute is None:
        dcx.dump()
        return {"data": dcx.channels[CHANNEL_BAR].muted}
    else:
        dcx.channels[CHANNEL_BAR].mute().send()


@app.route("/api/dcx/balance")
@app.route("/api/dcx/balance/<int:balance>", methods=["GET", "POST"])
def balance_bar_room(balance=None):
    dcx = create_dcx()
    if balance is None:
        dcx.dump()
        gain_bar = dcx.channels[CHANNEL_BAR].gain
        gain_room = dcx.channels[CHANNEL_ROOM].gain
        return {"data": gain_bar if gain_bar < 0 else gain_room}
    else:
        # bar -12 ... 0 ... 12 room
        # Clamp value
        balance = max(min(balance, 12), -12)
        gain_bar = (min(balance, 0) / -4) - max(balance, 0)
        gain_room = (max(balance, 0) / 4) + min(balance, 0)

        dcx.channels[CHANNEL_BAR].set_gain(gain_bar)
        dcx.channels[CHANNEL_ROOM].set_gain(gain_room).send()


if __name__ == "__main__":
    app.run()
