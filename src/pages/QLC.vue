<template>
  <q-page>
    <iframe :src="url" frameBorder="0" style="width: 100vw; height: 100vh"></iframe>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  setup() {
    return {
      url: `${window.location.protocol}//${window.location.host}:9999`
    }
  },
})
</script>
