<template>
  <q-splitter v-model="splitterWidth">
    <template #before>
      <q-tabs v-model="modeTab" vertical class="text-secondary">
        <q-tab name="staticColor" label="Einfarbig" />
        <q-tab name="fadingColor" label="Farbwechsel" />
        <q-tab name="rainbow" label="Regenbogen" />
      </q-tabs>
    </template>

    <template #after>
      <q-tab-panels v-model="modeTab" animated transition-prev="slide-down" transition-next="slide-up">
        <q-tab-panel name="staticColor">
          <div class="text-h5">Einfarbig</div>
          <p>In dieser Einstellung wird eine statische Farbe angezeigt.</p>
          <div class="row">
            <div class="col-sm-6 col-xs-12">
              <div class="text-h6">Farbe</div>
              <q-color
                v-model="singleColor.color"
                default-value="#ff9b00"
                default-view="palette"
                style="max-width: 25vw; margin: auto"
              />
            </div>
            <div class="col-sm-6 col-xs-12">
              <div class="text-h6">Helligkeit</div>
              <q-item>
                <q-item-section side>
                  <q-icon name="mdi-brightness-6" />
                </q-item-section>
                <q-item-section>
                  <q-slider v-model="singleColor.brightness" :min="0" :max="255" />
                </q-item-section>
              </q-item>
            </div>
          </div>
        </q-tab-panel>

        <q-tab-panel name="fadingColor">
          <div class="text-h5">Farbwechsel</div>
          <p>In dieser Einstellung werden alle Farben durchgewechselt.</p>
        </q-tab-panel>

        <q-tab-panel name="rainbow">
          <div class="text-h5">Regenbogen</div>
          <p>In dieser Einstellung wird ein Regenbogen angezeigt.</p>
        </q-tab-panel>
      </q-tab-panels>
    </template>
  </q-splitter>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'ColorPanel',
  setup() {
    const modeTab = ref('staticColor');
    const splitterWidth = ref(20)

    const singleColor = {
      color: '#ff9b00',
      brightness: 100,
    };

    return { singleColor, modeTab, splitterWidth };
  },
});
</script>
