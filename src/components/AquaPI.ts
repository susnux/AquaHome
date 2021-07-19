import { api } from 'boot/axios';

interface BooleanAnswer {
  data: boolean;
}

interface NumericAnswer {
  data: number;
}

export async function isPiMuted() {
  const { data } = await api.get<BooleanAnswer>('/pi/mute');
  return data.data;
}

export function mutePi(mute: boolean) {
  return api.post<BooleanAnswer>(`pi/mute/${mute ? 1 : 0}`);
}

export async function isPiLimited() {
  const { data } = await api.get<BooleanAnswer>('/pi/limit');
  return data.data;
}

export function limitPi(limit: boolean) {
  return api.post<BooleanAnswer>(`pi/limit/${limit ? 1 : 0}`);
}

export async function isBarMuted() {
  const { data } = await api.get<BooleanAnswer>('/dcx/bar/mute');
  return data.data;
}

export function muteBar(mute: boolean) {
  return api.post<BooleanAnswer>(`dcx/bar/mute/${mute ? 1 : 0}`);
}

export function setBarFloorBalance(balance: number) {
  return api.post<NumericAnswer>(`dcx/balance/${balance}`);
}

export async function getBarFloorBalance() {
  const { data } = await api.get<NumericAnswer>('dcx/balance');
  return data.data;
}

export async function isSubwooferMuted() {
  const { data } = await api.get<BooleanAnswer>('/dcx/subwoofer/mute');
  return data.data;
}

export function muteSubwoofer(mute: boolean) {
  return api.post<BooleanAnswer>(`dcx/subwoofer/mute/${mute ? 1 : 0}`);
}
