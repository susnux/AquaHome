<template>
  <div class="text-h6">Kreativ</div>
  <p>Selber gestalten</p>
  <q-btn-group>
    <q-btn @click="zoom(-1)" dense outline color="secondary" icon="mdi-minus" />
    <q-btn @click="clear" dense outline icon="mdi-nuke" />
    <q-btn @click="zoom(1)" dense outline color="primary" icon="mdi-plus"
  /></q-btn-group>
  <q-btn @click="send" dense outline color="primary">Anzeigen</q-btn>
  <br />
  <canvas
    ref="canvas"
    @mousedown="setPosition"
    @mouseenter="setPosition"
    @mousemove="draw"
    width="38"
    height="8"
    :style="{ height: `${factor * 8}px`, width: `${factor * 38}px` }"
  ></canvas>
</template>

<script lang="ts">
const LED_HEIGHT = 8;
const LED_WIDTH = 38;

import { Notify } from 'quasar';
import { useMatrixStore } from 'src/stores/matrix';
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'ManualPanel',
  setup() {
    const store = useMatrixStore();
    const factor = ref(15);
    const color = ref('#ffab00');

    function zoom(i: number) {
      if (i < 0 && factor.value > 4) factor.value -= 1;
      else if (i > 0) factor.value += 1;
    }

    const canvas = ref<HTMLCanvasElement>();

    var pos = { x: 0, y: 0 };
    // new position from mouse event
    function setPosition(e: MouseEvent) {
      pos.x = e.offsetX / factor.value;
      pos.y = e.offsetY / factor.value;
    }

    function draw(e: MouseEvent) {
      var ctx = <CanvasRenderingContext2D>canvas.value?.getContext('2d');

      // mouse left button must be pressed
      if (e.buttons !== 1) return;

      ctx.beginPath(); // begin

      ctx.lineWidth = 0.3;
      ctx.miterLimit = 3;
      ctx.lineCap = 'square';
      ctx.strokeStyle = color.value;

      ctx.moveTo(pos.x, pos.y); // from
      setPosition(e);
      ctx.lineTo(pos.x, pos.y); // to

      ctx.stroke(); // draw it!
    }
    function clear() {
      var ctx = <CanvasRenderingContext2D>canvas.value?.getContext('2d');
      ctx.clearRect(0, 0, LED_WIDTH, LED_HEIGHT);
    }
    function send() {
      var ctx = <CanvasRenderingContext2D>canvas.value?.getContext('2d');
      const data = [] as number[];
      for (var y = 0; y < LED_HEIGHT; y++)
        for (var x = 0; x < LED_WIDTH; x++)
          data.push(
            ctx.getImageData(x, y, 1, 1).data.reduce((p, c, i) => {
              if (i === 3) return p;
              return (p << 8) | c;
            })
          );
      store.setData({pixels: data}).catch((e) => Notify.create({
          type: 'negative',
          message: e as string
      }));
    }

    return {
      zoom,
      canvas,
      send,
      factor,
      clear,
      draw,
      setPosition,
    };
  },
});
</script>

<style scoped>
canvas {
  border: solid 1px;
  image-rendering: -moz-crisp-edges;
  image-rendering: -webkit-crisp-edges;
  image-rendering: pixelated;
  image-rendering: crisp-edges;
}
</style>