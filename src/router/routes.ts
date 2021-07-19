import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', redirect: { name: 'overview' } },
      {
        path: 'overview',
        name: 'overview',
        component: () => import('pages/Index.vue'),
      },
      {
        path: 'audio',
        name: 'audio',
        component: () => import('pages/Audio.vue'),
      },
      {
        path: 'dj',
        name: 'djtable',
        component: () => import('pages/Light.vue'),
      },
      {
        path: 'qlcplus',
        name: 'qlcplus',
        component: () => import('pages/QLC.vue'),
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue'),
  },
];

export default routes;
