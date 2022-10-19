<template>
  <q-page>
    <q-list dense>
      <q-item-label header>Raspberry PI (Spotify, YouTubeMusic und Co)</q-item-label>
      <q-item>
        <q-item-section>PI Stummschaltung</q-item-section>
        <q-item-section side>
          <q-toggle v-model="piMuted">
            <q-tooltip
              ><template v-if="piMuted">stummgeschaltet</template
              ><template v-else>Wiedergabe aktiv</template></q-tooltip
            >
          </q-toggle>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section>
          Lautstärkebegrenzung (standardmäßig an)
          <q-item-label caption
            >Limitiert die Lautstärke für einen normalen Dienst, Limit ausschalten für Spotify Partys.</q-item-label
          >
        </q-item-section>
        <q-item-section side>
          <q-toggle v-model="piLimited" color="green" aria-label="Lautstärke limitieren" />
        </q-item-section>
      </q-item>
      <q-separator />
      <q-item-label header>Raum und Bar</q-item-label>
      <q-item>
        <q-item-section>Bar Stummschaltung</q-item-section>
        <q-item-section side>
          <q-toggle v-model="barMuted">
            <q-tooltip
              ><template v-if="barMuted">stummgeschaltet</template
              ><template v-else>Wiedergabe aktiv</template></q-tooltip
            >
          </q-toggle>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section>
          Subwoofer deaktivieren*
          <q-tooltip>Die Subwoofer werden zwischen 00:00 Uhr und 07:00 Uhr automatisch herunter geregelt.</q-tooltip>
          <q-item-label caption>Diese Funktion erlaubt das vollständige Ausschalten der Subwoofer.</q-item-label>
        </q-item-section>
        <q-item-section side>
          <q-toggle v-model="subwooferMuted">
            <q-tooltip
              ><template v-if="subwooferMuted">stummgeschaltet</template
              ><template v-else>Wiedergabe aktiv</template></q-tooltip
            >
          </q-toggle>
        </q-item-section>
      </q-item>
      <q-item-label header>Balance Bar-Raum</q-item-label>
      <q-item>
        <q-item-section side>
          <strong>Bar</strong>
        </q-item-section>
        <q-item-section>
          <q-slider
            v-model="balanceBarFloor"
            :min="-12"
            :max="12"
            step="1"
            :color="balanceBarFloor == 0 ? 'grey' : balanceBarFloor < 0 ? 'primary' : 'secondary'"
          />
        </q-item-section>
        <q-item-section side>
          <strong>Raum</strong>
        </q-item-section>
      </q-item>
      <q-separator />
      <q-item-label header>Raucherraum</q-item-label>
      <q-item>
        <q-item-section side>
          <q-icon name="mdi-volume-minus" />
        </q-item-section>
        <q-item-section>
          <q-slider v-model="smokerGain" :min="-9" :max="3" step=".1" :disable="smokerMuted" label />
        </q-item-section>
        <q-item-section side>
          <q-icon name="mdi-volume-plus" />
        </q-item-section>
        <q-item-section side>
          <q-btn
            icon="mdi-volume-off"
            disable
            @click="smokerMuted = !smokerMuted"
            :color="smokerMuted ? 'primary' : 'secondary'"
            round
            dense
          >
            <q-tooltip
              ><template v-if="smokerMuted">Stummschaltung aufheben</template
              ><template v-else>Stummschalten</template></q-tooltip
            >
          </q-btn>
        </q-item-section>
      </q-item>
    </q-list>
  </q-page>
</template>

<script lang="ts">
import { computed, defineComponent, ref, onBeforeMount } from 'vue';
import { Notify, useQuasar } from 'quasar';
import {
  getBarFloorBalance,
  isBarMuted,
  isPiLimited,
  isPiMuted,
  isSubwooferMuted,
  limitPi,
  muteBar,
  mutePi,
  setBarFloorBalance,
} from 'src/components/AquaPI';

export default defineComponent({
  name: 'PageAudio',
  setup() {
    const init = ref(false);
    const $q = useQuasar();

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

    // gain smoker lounge, -9db up to +3db
    const smokerGain = ref(0);
    const smokerMuted = ref(true);

    // bar ------- 0 -------- floor
    //   -12dB ... 0 ... 12 dB
    const _balanceBarFloor = ref(0);
    const balanceBarFloor = computed({
      get: () => _balanceBarFloor.value,
      set: (x: number) => void setBarFloorBalance(x).then((resp) => (_balanceBarFloor.value = resp.data.data)),
    });

    const _barMuted = ref(false);
    const barMuted = computed({
      get: () => _barMuted.value,
      set: (x: boolean) => void muteBar(x).then((resp) => (_barMuted.value = resp.data.data)),
    });

    const _subwooferMuted = ref(false);
    const subwooferMuted = computed({
      get: () => _subwooferMuted.value,
      set: (x: boolean) => void muteBar(x).then((resp) => (_subwooferMuted.value = resp.data.data)),
    });

    const _piMuted = ref(false);
    const piMuted = computed({
      get: () => _piMuted.value,
      set: (x: boolean) => void mutePi(x).then((resp) => (_piMuted.value = resp.data.data)),
    });
    const _piLimited = ref(true);
    const piLimited = computed({
      get: () => _piLimited.value,
      set: (x: boolean) => void limitPi(x).then((resp) => (_piLimited.value = resp.data.data)),
    });

    async function loadValues() {
      try {
        _piMuted.value = await isPiMuted();
        _piLimited.value = await isPiLimited();
        _barMuted.value = await isBarMuted();
        _subwooferMuted.value = await isSubwooferMuted();
        _balanceBarFloor.value = await getBarFloorBalance();
      } catch (error) {
        Notify.create({
          message: 'Keine Kommunikation möglich, ¿Queerdenker?',
          type: 'negative',
        });
      }
    }

    return {
      barMuted,
      balanceBarFloor,
      piLimited,
      piMuted,
      subwooferMuted,
      smokerMuted,
      smokerGain,
    };
  },
});
</script>
