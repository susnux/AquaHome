<template>
  <q-page>
    <q-toggle label="DMX Steuerung" disable v-model="dmxControlled"></q-toggle>
    <q-toggle label="Alles aus (Blackout)" :disable="dmxControlled" v-model="blackout"></q-toggle>
    <q-card>
      <q-tabs v-model="tab" dense align="justify" narrow-indicator>
        <q-tab :disable="dmxControlled" name="animations" label="Animationen" />
        <q-tab :disable="dmxControlled" name="colors" label="Farben" />
        <q-tab :disable="dmxControlled" name="music" label="Musik" />
        <q-tab :disable="dmxControlled" name="text" label="Text" />
      </q-tabs>

      <q-separator />

      <q-tab-panels :model-value="dmxControlled ? 'dmx' : tab" animated>
        <q-tab-panel name="dmx">
          <div class="text-h6">DMX gesteuert</div>
          Aktuell wird die Beleuchtung über DMX gesteuert.
        </q-tab-panel>
        <q-tab-panel name="animations">
          <div class="text-h5">aquarium</div>
          Lorem ipsum dolor sit amet consectetur adipisicing elit.
        </q-tab-panel>
        <q-tab-panel name="colors">
          <color-panel />
        </q-tab-panel>
        <q-tab-panel name="music">
          <div class="text-h6">aquarium</div>
          Lorem ipsum dolor sit amet consectetur adipisicing elit.
        </q-tab-panel>
        <q-tab-panel name="text">
          <text-panel />
        </q-tab-panel>
      </q-tab-panels>
    </q-card>
  </q-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import ColorPanel from 'src/components/light/ColorPanel.vue';
import TextPanel from 'src/components/light/TextPanel.vue';

export default defineComponent({
  name: 'PageAudio',
  components: { ColorPanel, TextPanel },
  setup() {
    const dmxControlled = ref(true);
    const tab = ref('colors');
    const blackout = ref(true);

    return { blackout, dmxControlled, tab };
  },
});
</script>
