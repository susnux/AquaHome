from flask import Blueprint
from pulsectl import Pulse


pi_bp = Blueprint('pi', __name__)


def pulse_volume(limit=None):
    with Pulse("AquaHome") as pulse:
        sink_input = pulse.sink_list()[0]
        volume = sink_input.volume
        if limit is not None:
            volume.value_flat = limit
            pulse.volume_set(sink_input, volume)
        return volume.value_flat



@pi_bp.route("/api/pi/mute/")
@pi_bp.route("/api/pi/mute/<int:i>", methods=["GET", "POST"])
def mute_pi(i=None):
    if i is not None:
        pulse_volume(0.0 if i == 1 else 0.6)
        return {"data": i == 1}
    else:
        return {"data": pulse_volume() < 0.01}


@pi_bp.route("/api/pi/limit/")
@pi_bp.route("/api/pi/limit/<int:i>", methods=["GET", "POST"])
def limit_pi(i=None):
    if i is not None:
        pulse_volume(1.0 if i == 0 else 0.6)
        return {"data": i == 1}
    else:
        return {"data": pulse_volume() < 0.98}
