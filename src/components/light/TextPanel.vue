<template>
  <div class="text-h5">Textanimation</div>
  <p>In diesem Modus kann ein Text angezeigt werden</p>
  <div class="row q-gutter-md justify-around">
    <q-input filled debounce="900" v-model="text" label="Text" class="col-sm-5 col-xs-12"></q-input>
    <q-input filled debounce="900" v-model="color" label="Farbe" class="col-sm-5 col-xs-12">
      <template #append>
        <q-icon name="mdi-select-color" class="cursor-pointer">
          <q-popup-proxy transition-show="scale" transition-hide="scale">
            <q-color v-model="color" />
          </q-popup-proxy>
        </q-icon>
      </template>
    </q-input>
    <div class="col-sm-5 col-xs-12">
      <q-item-label caption>Helligkeit</q-item-label>
      <q-item>
        <q-item-section side>
          <q-icon name="mdi-brightness-6" />
        </q-item-section>
        <q-item-section>
          <q-slider v-model="brightness" :min="0" :max="255" />
        </q-item-section>
      </q-item>
    </div>
    <div class="col-sm-5 col-xs-12">

    <q-item-label caption>Geschwindigkeit</q-item-label>
    <q-item>
      <q-item-section side>
        <q-icon name="mdi-play-speed" />
      </q-item-section>
      <q-item-section>
        <q-slider v-model="speed" :min="0" :max="255" />
      </q-item-section>
    </q-item>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'TextPanel',
  setup() {
    const color = ref('#FF9B00')
    const text = ref('')
    const speed = ref(0)
    const brightness = ref(127)

    return { color, text, speed, brightness };
  },
});
</script>
