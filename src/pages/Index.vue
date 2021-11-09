<template>
  <q-page class="row">
    <div class="col-12 row q-gutter-sm items-center justify-center">
      <div class="col-2 text-right">
        <q-btn round color="secondary" @click="mute" :icon="muteIcon" aria-label="RaspberryPI stummschalten" />
      </div>
      <div class="col-9">Raspberry (Spotify+Co) stummschalten</div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { mutePi, isPiMuted } from 'src/components/AquaPI';
import { defineComponent, ref, onBeforeMount } from 'vue';
import { Notify, useQuasar } from 'quasar';

export default defineComponent({
  name: 'PageIndex',
  setup() {
    const $q = useQuasar();
    const init = ref(false);
    const muteIcon = ref('mdi-volume-mute');
    const _piMuted = ref(false);
    function mute() {
      void mutePi(!_piMuted.value).then((resp) => (_piMuted.value = resp.data.data));
      if (_piMuted.value) muteIcon.value = 'mdi-volume-mute';
      else muteIcon.value = 'mdi-volume-high';
    }
    onBeforeMount(() => {
      if (!init.value) {
        $q.loading.show({
          delay: 300, // ms
        });
        loadValues().finally(() => {
          init.value = true;
          $q.loading.hide();
        });
      }
    });
    async function loadValues() {
      try {
        _piMuted.value = await isPiMuted();
      } catch (error) {
        Notify.create({
          message: 'Keine Kommunikation möglich, ¿Queerdenker?',
          type: 'negative',
        });
      }
    }

    return { muteIcon, mute };
  },
});
</script>
