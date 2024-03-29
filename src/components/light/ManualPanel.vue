<template>
  <div class="row justify-center" ref="container">
    <div class="col-12 text-center">
      <div class="text-h6">Kreativmodus</div>
      <blockquote>"We don't make mistakes, just happy little accidents."</blockquote>
    </div>
    <div class="col-xs-12" :class="{ 'col-md-9': sbs }">
      <div style="display: block; margin-bottom: 0.5em">
        <q-btn-group>
          <q-btn @click="zoom(-1)" dense outline color="secondary" icon="mdi-minus" />
          <q-btn @click="zoom(1)" dense outline color="primary" icon="mdi-plus"
        /></q-btn-group>
      </div>
      <canvas
        ref="canvas"
        @mousedown="setPosition"
        @touchstart="setPosition"
        @mouseenter="setPosition"
        @mousemove="draw"
        @touchmove="draw"
        width="38"
        height="8"
        :style="{ height: `${factor * 8}px`, width: `${factor * 38}px` }"
      ></canvas>
    </div>
    <div class="col-xs-12 col-lg-3" :class="{ 'col-md-3': sbs, 'col-md-5': !sbs }">
      <q-list dense>
        <q-item>
          <q-item-section side>
            <q-icon name="mdi-pen-minus" />
          </q-item-section>
          <q-item-section>
            <q-slider title="Stiftstärke" v-model="lineWidth" :min="0.025" :max="3.5" :step="0.025" label />
          </q-item-section>
          <q-item-section side>
            <q-icon name="mdi-pen-plus" />
          </q-item-section>
        </q-item>
        <q-item>
          <q-btn class="full-width" dense outline
            >Farbe <q-icon name="mdi-palette" class="cursor-pointer" />
            <q-popup-proxy cover>
              <q-color v-model="color" no-header-tabs />
            </q-popup-proxy>
          </q-btn>
        </q-item>
        <q-item>
          <q-btn class="full-width" dense outline
            >Speichern <q-icon name="mdi-download" class="cursor-pointer" />
            <q-popup-proxy cover @before-show="setDataURL">
              <div style="widht: 100%; text-align: center">
                <q-btn type="a" :href="dataURL" download="matrix.png" dense outline>Herunterladen</q-btn>
              </div>
            </q-popup-proxy>
          </q-btn>
        </q-item>
        <q-item>
          <q-btn class="full-width" @click="clickFileInput" dense outline
            >Laden <q-icon name="mdi-upload" class="cursor-pointer"
          /></q-btn>
          <input type="file" name="image" style="display: none" ref="fileInput" accept="image/*" />
        </q-item>
        <q-item>
          <q-btn class="full-width" @click="clear" dense outline color="negative"
            >Löschen <q-icon name="mdi-nuke" class="cursor-pointer"
          /></q-btn>
        </q-item>
        <q-item>
          <q-btn class="full-width" @click="send" dense outline color="primary"
            >Anzeigen <q-icon name="mdi-send" class="cursor-pointer"
          /></q-btn>
        </q-item>
      </q-list>
    </div>
  </div>
</template>

<script lang="ts">
const LED_HEIGHT = 8;
const LED_WIDTH = 38;

import { Notify } from 'quasar';
import { useMatrixStore } from 'src/stores/matrix';
import { computed, defineComponent, onMounted, onUnmounted, ref } from 'vue';

export default defineComponent({
  name: 'ManualPanel',
  setup() {
    const store = useMatrixStore();
    const factor = ref(15);
    const color = ref('#ffab00');
    const lineWidth = ref(0.3);
    const container = ref<HTMLDivElement>();
    const canvas = ref<HTMLCanvasElement>();
    const fileInput = ref<HTMLInputElement>();
    const dataURL = ref('#');

    onMounted(() => {
      // Activate manual mode
      void store.setMode('manual');

      // Resize canvas to match container
      resize();
      window.addEventListener('resize', resize);

      // Register draw function to FileInput
      fileInput.value?.addEventListener('change', loadImage);

      // Register events tp prevent scrolling when touching the canvas
      document.body.addEventListener(
        'touchstart',
        function (e) {
          if (e.target == canvas.value) {
            e.preventDefault();
          }
        },
        false
      );
      document.body.addEventListener(
        'touchend',
        function (e) {
          if (e.target == canvas.value) {
            e.preventDefault();
          }
        },
        false
      );
      document.body.addEventListener(
        'touchmove',
        function (e) {
          if (e.target == canvas.value) {
            e.preventDefault();
          }
        },
        false
      );
    });

    onUnmounted(() => window.removeEventListener('resize', resize));

    function resize() {
      if (container.value !== undefined)
        factor.value = Math.floor(((window.innerWidth > 1023 ? 0.75 : 1) * container.value.clientWidth) / LED_WIDTH);
    }
  
    const sbs = computed(() => {
      const a = (factor.value * 38) / (container.value?.offsetWidth || 0);
      console.log(a);
      return a < 0.75;
    });

    function clickFileInput() {
      fileInput.value?.click();
    }

    function setDataURL(e: Event) {
      dataURL.value = canvas.value?.toDataURL() || '#';
    }

    function loadImage(ev: Event) {
      var ctx = <CanvasRenderingContext2D>canvas.value?.getContext('2d');
      const img = new Image();
      const input = <HTMLInputElement>fileInput.value;
      if (input.files) {
        const f = input.files[0],
          url = window.URL || window.webkitURL,
          src = url.createObjectURL(f);

        img.src = src;
        img.onload = function () {
          clear();
          var cc = 38 / img.width;
          if (cc * img.height > 8) cc = 8 / img.height;

          const h = img.height * cc;
          const w = img.width * cc;
          console.log(w, h);
          ctx.drawImage(img, 0, 0, img.width, img.height, Math.floor((38 - w) / 2), Math.floor((8 - h) / 2), w, h);
          url.revokeObjectURL(src);
        };
      }
    }

    function zoom(i: number) {
      if (i < 0 && factor.value > 4) factor.value -= 1;
      else if (i > 0 && (factor.value + 2) * LED_WIDTH < (container.value?.offsetWidth || 1)) factor.value += 1;
    }

    var pos = { x: 0, y: 0 };
    // new position from mouse event
    function setPosition(e: MouseEvent | TouchEvent) {
      if (e instanceof MouseEvent) {
        pos.x = e.offsetX / factor.value;
        pos.y = e.offsetY / factor.value;
      } else if (e.touches.length > 0) {
        const rect = (<HTMLCanvasElement>canvas.value).getBoundingClientRect();
        pos.x = Math.round((e.touches[0].clientX - rect.left) / factor.value);
        pos.y = Math.round((e.touches[0].clientY - rect.top) / factor.value);
      }
    }

    function draw(e: MouseEvent | TouchEvent) {
      var ctx = <CanvasRenderingContext2D>canvas.value?.getContext('2d');

      // mouse left button must be pressed
      if (e instanceof MouseEvent && e.buttons !== 1) return;

      ctx.beginPath(); // begin

      ctx.lineWidth = lineWidth.value;
      ctx.miterLimit = 3;
      ctx.lineCap = 'square';
      ctx.strokeStyle = color.value;

      ctx.moveTo(pos.x, pos.y); // from
      console.log(pos)
      setPosition(e);
      ctx.lineTo(pos.x, pos.y); // to
      console.log(pos)

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
        for (var x = 0; x < LED_WIDTH; x++) {
          const d = ctx.getImageData(x, y, 1, 1).data;
          data.push(
            (Math.floor((d[0] * d[3]) / 255) << 16) |
              (Math.floor((d[1] * d[3]) / 255) << 8) |
              Math.floor((d[2] * d[3]) / 255)
          );
        }
      store.setData({ pixels: data }).catch((e) =>
        Notify.create({
          type: 'negative',
          message: e as string,
          timeout: 1000,
        })
      );
    }

    return {
      sbs,
      canvas,
      clear,
      clickFileInput,
      color,
      container,
      dataURL,
      draw,
      factor,
      fileInput,
      lineWidth,
      send,
      setDataURL,
      setPosition,
      zoom,
    };
  },
});
</script>

<style scoped>
.body--dark canvas {
  border: solid 1px white;
}

canvas {
  background-color: black;
  image-rendering: -moz-crisp-edges;
  image-rendering: -webkit-crisp-edges;
  image-rendering: pixelated;
  image-rendering: crisp-edges;
}

blockquote {
  quotes: '“' '”' '‘' '’';
}
</style>
