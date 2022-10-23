<template>
  <q-splitter v-model="splitterWidth">
    <template #before>
      <q-tabs v-model="modeTab" vertical class="text-secondary">
        <q-tab name="fish_tank" label="Aquarium" />
        <q-tab name="text" label="Text" />
      </q-tabs>
    </template>

    <template #after>
      <q-tab-panels v-model="modeTab" animated transition-prev="slide-down" transition-next="slide-up">
        <q-tab-panel name="fish_tank">
          <div class="text-h5">Aquarium</div>
          <p>Animation eines Aquariums.</p>
          <q-item>
            <q-item-section side>
              <q-icon name="mdi-speedometer" />
            </q-item-section>
            <q-item-section>
              <q-slider v-model="speed" title="Geschwindigkeit" :min="0" :max="255" />
            </q-item-section>
          </q-item>
        </q-tab-panel>

        <q-tab-panel name="text">
          <div class="text-h5">Textanimation</div>
          <p>In diesem Modus kann ein Text angezeigt werden</p>
          <div class="row q-gutter-md justify-around">
            <q-input filled debounce="900" v-model="text" label="Text" class="col-sm-5 col-xs-12"></q-input>
            <q-input filled debounce="900" v-model="color" label="Farbe (Text)" class="col-sm-5 col-xs-12">
              <template #append>
                <q-icon name="mdi-select-color" class="cursor-pointer">
                  <q-popup-proxy transition-show="scale" transition-hide="scale">
                    <q-color v-model="color" />
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
            <q-select v-model="font" title="Schriftart" :options="fonts" filled class="col-sm-5 col-xs-12">
              <template #prepend>
                <q-icon name="mdi-format-font" />
              </template>
            </q-select>
            <q-input filled debounce="900" v-model="background" label="Farbe (Hintergrund)" class="col-sm-5 col-xs-12">
              <template #append>
                <q-icon name="mdi-select-color" class="cursor-pointer">
                  <q-popup-proxy transition-show="scale" transition-hide="scale">
                    <q-color v-model="background" />
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
            <div class="col-12">
              <q-item-label caption>Geschwindigkeit</q-item-label>
              <q-item>
                <q-item-section side>
                  <q-icon name="mdi-speedometer" />
                </q-item-section>
                <q-item-section>
                  <q-slider v-model="speed" title="Geschwindigkeit" :min="0" :max="255" />
                </q-item-section>
              </q-item>
            </div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </template>
  </q-splitter>
</template>

<script lang="ts">
import { debounce, Notify } from 'quasar';
import { useMatrixStore } from 'src/stores/matrix';
import { computed, defineComponent, ref, watch } from 'vue';

export default defineComponent({
  name: 'AnimationPanel',
  setup() {
    const store = useMatrixStore();

    const splitterWidth = ref(20);

    const modeTab = computed({
      get: () => store.mode,
      set(mode: string) {
        void (async () => {
          try {
            if (mode == 'fish_tank') await store.setMode('fish_tank');
            else if (mode == 'text')
              await store.setMode('text', {
                color: color.value,
                background: background.value,
                font: font.value.value,
                text: text.value,
              });
          } catch (reason) {
            error(reason as string);
          }
        })();
      },
    });

    const fonts = [
      { value: 0, label: '8x8' },
      { value: 1, label: '5x8' },
    ];
    const background = ref('#000000');
    const color = ref('#FFAB00');
    const text = ref('');
    const font = ref(fonts[0]);

    watch([background, color, font, text], (current, old) => {
      if (current[0] != old[0]) {
        store
          .setData({
            background: parseInt(background.value.substring(1), 16),
          })
          .catch(() => {
            error();
            background.value = old[0];
          });
      }
      if (current[1] != old[1]) {
        store
          .setData({
            color: parseInt(color.value.substring(1), 16),
          })
          .catch(() => {
            error();
            color.value = old[1];
          });
      }
      if (current[2] != old[2])
        store.setData({ font: font.value.value }).catch(() => {
          error();
          font.value = old[2];
        });
      if (current[3] != old[3])
        store.setData({ text: text.value }).catch(() => {
          error();
          text.value = old[3];
        });
    });

    const speed = computed({
      get: () => store.speed,
      set: debounce((s: number) => void store.setSpeed(s), 500),
    });

    function error(s = 'Fehler beim Senden der Daten.') {
      Notify.create({
        type: 'negative',
        message: s,
      });
    }

    return { background, color, text, font, fonts, speed, modeTab, splitterWidth };
  },
});
</script>
