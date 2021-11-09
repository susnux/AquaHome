<template>
  <q-layout view="hHh lpr fff">
    <q-header elevated class="bg-primary text-black" height-hint="98">
      <q-toolbar>
        <q-toolbar-title>
          <q-btn v-if="mobile" flat @click="drawer = !drawer" round dense icon="mdi-menu" />
          <q-avatar square>
            <img src="/icons/logo.svg" />
          </q-avatar>
        </q-toolbar-title>

        <q-tabs v-if="!mobile" shrink>
          <q-route-tab v-for="(entry, index) in menuList" :key="index" :to="{ name: entry.name }" :label="entry.text" />
        </q-tabs>
      </q-toolbar>
    </q-header>

    <q-drawer v-if="mobile" v-model="drawer" show-if-above :width="200" :breakpoint="500" bordered>
      <q-scroll-area class="fit">
        <q-list>
          <template v-for="(menuItem, index) in menuList" :key="index">
            <q-item clickable :to="{ name: menuItem.name }" v-ripple>
              <q-item-section>
                {{ menuItem.text }}
              </q-item-section>
            </q-item>
          </template>
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';

const menuList = [
  {
    name: 'overview',
    text: 'Überblick',
  },
  {
    name: 'audio',
    text: 'Audio',
  },
  {
    name: 'djtable',
    text: 'DJ Pult',
  },
  {
    name: 'qlcplus',
    text: 'Party beleuchtung',
  },
];

export default {
  setup() {
    const mobile = ref(false);

    onMounted(() => {
      resized();
      window.addEventListener('resize', resized);
    });
    onUnmounted(() => window.removeEventListener(resized));

    function resized() {
      mobile.value = window.innerWidth < 600;
    }

    return {
      drawer: ref(false),
      mobile,
      menuList,
    };
  },
};
</script>
