import { AxiosError } from 'axios';
import { defineStore } from 'pinia';
import { api } from 'src/boot/axios';
import { BooleanAnswer } from '../components/AquaPI';

export type Mode = 'blackout' | 'color' | 'fade' | 'rainbow' | 'manual' | 'text' | 'fish_tank';

interface StatusAnswer {
  mode: Mode;
  ok: boolean;
  speed: number;
  brightness: number;
}

function handleError(e: AxiosError) {
  const status = e.response?.status;
  if (typeof status === 'number') {
    if (status >= 500) return Promise.reject('Serverfehler, wenn das noch einmal passiert schreib mal der Technik.');
    else if (status === 400 || status === 404) return Promise.reject('Nicht implementiert, sorry :/');
  }
  return Promise.reject('Ups, das hätte nicht passieren sollen.');
}

export const useMatrixStore = defineStore('matrix', {
  state: () => ({
    mode: 'blackout' as Mode,
    _lastMode: 'color' as Mode,
    _lastData: { color: parseInt('ffab00', 16) } as object | undefined,
    isBlackout: true,
    speed: 0,
    brightness: 0,
  }),
  getters: {
    isBlackout(state) {
      return state.mode == 'blackout';
    },
  },
  actions: {
    status() {
      return api
        .get<StatusAnswer>('matrix/status')
        .then(({ data }) => {
          this.mode = data.mode;
          this.speed = data.speed;
          this.brightness = data.brightness;
        })
        .catch(handleError);
    },
    blackout(x = true) {
      if (x) void this.setMode('blackout');
      else void this.setMode(this._lastMode, this._lastData);
    },
    setData(data: object) {
      return api.post<BooleanAnswer>('matrix/prefs', data);
    },
    setMode(m: Mode, data: object | undefined = undefined) {
      if (this.mode === m)
        if (data) return this.setData(data);
        else return Promise.resolve();
      else
        return api
          .post<BooleanAnswer>('matrix/mode', { mode: m, prefs: data })
          .then(() => {
            this.mode = m;
            if (m !== 'blackout') {
              this._lastMode = m;
              this._lastData = data;
            }
          })
          .catch(handleError);
    },
    setBrightness(b: number) {
      return api
        .post<BooleanAnswer>('matrix/brightness', { value: b })
        .then(() => (this.brightness = b))
        .catch(handleError);
    },
    setSpeed(s: number) {
      return api
        .post<BooleanAnswer>('matrix/speed', { value: s })
        .then(() => (this.speed = s))
        .catch(handleError);
    },
  },
});
