from flask import Blueprint
import alsaaudio


pi_bp = Blueprint('pi', __name__)


class HiFiBerry:
    @staticmethod
    def find_hifiberry():
        for i in alsaaudio.card_indexes():
            (name, longname) = alsaaudio.card_name(i)
            if name == "snd_rpi_hifiberry_dacplus" or longname == "snd_rpi_hifiberry_dacplus":
                return i
        raise RuntimeError("HiFi Berry device not found")

    @staticmethod
    def limit(limit = True):
        hifiberry = HiFiBerry.find_hifiberry()
        mixer = alsaaudio.Mixer("Analogue", cardindex=hifiberry)
        channel = alsaaudio.MIXER_CHANNEL_ALL
        mixer.setvolume(100 if not limit else 0, channel)

    def is_limited():
        hifiberry = HiFiBerry.find_hifiberry()
        mixer = alsaaudio.Mixer("Analogue", cardindex=hifiberry)
        return any([c == 0 for c in mixer.getvolume()])

    @staticmethod
    def mute(muted=True):
        hifiberry = HiFiBerry.find_hifiberry()
        mixer = alsaaudio.Mixer("Digital", cardindex=hifiberry)
        mixer.setmute(1 if muted else 0)

    @staticmethod
    def is_muted():
        hifiberry = HiFiBerry.find_hifiberry()
        mixer = alsaaudio.Mixer("Digital", cardindex=hifiberry)
        return any([c == 1 for c in mixer.getmute()])


@pi_bp.route("/api/pi/mute/")
@pi_bp.route("/api/pi/mute/<int:i>", methods=["GET", "POST"])
def mute_pi(i=None):
    if i is not None:
        HiFiBerry.mute(i == 1)
        return {"data": i == 1}
    else:
        return {"data": HiFiBerry.is_muted()}


@pi_bp.route("/api/pi/limit/")
@pi_bp.route("/api/pi/limit/<int:i>", methods=["GET", "POST"])
def limit_pi(i=None):
    if i is not None:
        HiFiBerry.limit(i == 1)
        return {"data": i == 1}
    else:
        return {"data": HiFiBerry.is_limited()}
