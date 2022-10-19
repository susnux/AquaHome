<template>
  <q-page>
    <q-toggle label="Alles aus (Blackout)" v-model="blackout"></q-toggle>
    <q-item>
      <q-item-section side>
        <q-icon name="mdi-brightness-6" />
      </q-item-section>
      <q-item-section>
        <q-slider v-model="brightness" :disable="blackout" title="Helligkeit" :min="0" :max="255" />
      </q-item-section>
    </q-item>
    <q-card>
      <q-tabs v-model="tab" dense align="justify" narrow-indicator>
        <q-tab :disable="blackout" name="animations" label="Animationen" />
        <q-tab :disable="blackout" name="colors" label="Farben" />
        <q-tab :disable="blackout" name="music" label="Musik" />
        <q-tab :disable="blackout" name="manual" label="Kreativ" />
      </q-tabs>

      <q-separator />

      <q-tab-panels :model-value="blackout ? 'blackout' : tab" animated>
        <q-tab-panel name="blackout" style="text-align: center">
          <div class="text-h6">Blackout</div>
          Aktuell ist die Beleuchtung ausgeschaltet.
        </q-tab-panel>
        <q-tab-panel name="animations">
          <animation-panel />
        </q-tab-panel>
        <q-tab-panel name="colors">
          <color-panel />
        </q-tab-panel>
        <q-tab-panel name="music">
          <div class="text-h6">aquarium</div>
          Lorem ipsum dolor sit amet consectetur adipisicing elit.
        </q-tab-panel>
        <q-tab-panel name="manual">
          <manual-panel />
        </q-tab-panel>
      </q-tab-panels>
    </q-card>
  </q-page>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, onUnmounted, ref } from 'vue';
import ColorPanel from 'src/components/light/ColorPanel.vue';
import AnimationPanel from 'src/components/light/AnimationPanel.vue';
import ManualPanel from 'src/components/light/ManualPanel.vue';
import { useMatrixStore } from 'src/stores/matrix';
import { debounce, Notify } from 'quasar';

export default defineComponent({
  name: 'PageAudio',
  components: { ColorPanel, AnimationPanel, ManualPanel },
  setup() {
    const store = useMatrixStore();

    const _int = ref(
      setInterval(
        () => void store.status().catch((e) => Notify.create({ type: 'negative', message: e as string })),
        60000
      )
    );

    onMounted(() => {
      store.status().catch((e) => {
        Notify.create({ type: 'negative', timeout: 1000, message: e as string });
      });
    });

    onUnmounted(() => clearInterval(_int.value));

    const tab = ref(store.mode === 'manual' ? 'manual' : 'colors');

    const brightness = computed({
      get: () => store.brightness,
      set: debounce((b: number) => void store.setBrightness(b), 500),
    });

    const blackout = computed({
      get: () => store.isBlackout,
      set: debounce((x: boolean) => store.blackout(x), 250),
    });

    return { blackout, brightness, tab };
  },
});
</script>
