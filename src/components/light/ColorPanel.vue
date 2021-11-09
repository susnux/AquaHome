<template>
  <q-splitter v-model="splitterWidth">
    <template #before>
      <q-tabs v-model="modeTab" vertical class="text-secondary">
        <q-tab name="color" label="Einfarbig" />
        <q-tab name="fade" label="Farbwechsel" />
        <q-tab name="rainbow" label="Regenbogen" />
      </q-tabs>
    </template>

    <template #after>
      <q-tab-panels v-model="modeTab" animated transition-prev="slide-down" transition-next="slide-up">
        <q-tab-panel name="color">
          <div class="text-h5">Einfarbig</div>
          <p>In dieser Einstellung wird eine statische Farbe angezeigt.</p>
          <div class="text-h6">Farbe</div>
          <q-color v-model="color" default-value="#ffab00" default-view="palette" style="max-width: 25vw" />
        </q-tab-panel>

        <q-tab-panel name="fade">
          <div class="text-h5">Farbwechsel</div>
          <p>In dieser Einstellung wird der gesamte Farbraum durchlaufen, die Geschwindigkeit ist einstellbar.</p>
          <q-item>
            <q-item-section side>
              <q-icon name="mdi-speedometer" />
            </q-item-section>
            <q-item-section>
              <q-slider :model-value="speed" @change="setSpeed" title="Geschwindigkeit" :min="0" :max="255" />
            </q-item-section>
          </q-item>
        </q-tab-panel>

        <q-tab-panel name="rainbow">
          <div class="text-h5">Regenbogen</div>
          <p>In dieser Einstellung wird ein Regenbogen angezeigt.</p>
          <q-item>
            <q-item-section side>
              <q-icon name="mdi-speedometer" />
            </q-item-section>
            <q-item-section>
              <q-slider :model-value="speed" @change="setSpeed" title="Geschwindigkeit" :min="0" :max="255" />
            </q-item-section>
            <q-item-section side>
              <q-btn-toggle
                v-model="rainbowVertical"
                outline
                rounded
                :options="[
                  { label: 'Vertikal', value: true },
                  { label: 'Horizontal', value: false },
                ]"
              />
            </q-item-section>
          </q-item>
        </q-tab-panel>
      </q-tab-panels>
    </template>
  </q-splitter>
</template>

<script lang="ts">
import { debounce, Notify } from 'quasar';
import { useMatrixStore } from 'src/stores/matrix';
import { computed, defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'ColorPanel',
  setup() {
    const store = useMatrixStore();

    const _color = ref('#ffab00');
    const _vertical = ref(false);
    const splitterWidth = ref(20);

    function c2i(c: string) {
      return parseInt(c.substring(1), 16);
    }

    const modeTab = computed({
      get: () => store.mode,
      set(mode: string) {
        void (async () => {
          try {
            if (mode == 'color') await store.setMode('color', { color: c2i(color.value) });
            else if (mode == 'fade') await store.setMode('fade');
            else if (mode == 'rainbow') await store.setMode('rainbow', { vertical: rainbowVertical.value });
          } catch (reason) {
            createNotify(reason as string);
          }
        })();
      },
    });

    const color = computed({
      get: () => _color.value,
      set: debounce(
        (c: string) =>
          void store.setData({ color: c2i(c) }).then(() => {
            _color.value = c;
          }),
        500
      ),
    });

    const speed = ref(store.speed);
    function setSpeed(s: number) {
      speed.value = s;
      store.setSpeed(s).catch((e) => {
        createNotify(e as string);
        console.log(speed.value);
        speed.value = store.speed;
        console.log(speed.value);
      });
    }

    const rainbowVertical = computed({
      get: () => _vertical.value,
      set: (c: boolean) =>
        store.setData({ vertical: c }).then(() => {
          _vertical.value = c;
        }),
    });

    function createNotify(reason: string) {
      Notify.create({
        type: 'negative',
        message: reason,
      });
    }

    return { speed, setSpeed, rainbowVertical, color, modeTab, splitterWidth };
  },
});
</script>
