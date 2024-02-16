import { AppRouteRecordRaw } from '../types';
import { DEFAULT_LAYOUT } from '../base';

const GALLERY: AppRouteRecordRaw = {
  path: '/gallery',
  name: 'gallery',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.gallery',
    requiresAuth: true,
    icon: 'icon-image',
    order: 1,
  },
  children: [
    {
      path: '/myimage',
      name: 'myimage',
      component: () => import('@/views/gallery/image/index.vue'),
      meta: {
        locale: 'menu.image',
        requiresAuth: true,
        roles: ['admin','userVip2','userVip3','userVip4'],
      },
    },
    {
      path: '/myalbum',
      name: 'myalbum',
      component: () => import('@/views/gallery/album/index.vue'),
      meta: {
        locale: 'menu.album',
        requiresAuth: true,
        roles: ['admin','userVip2','userVip3','userVip4'],
      },
    },
  ],
};

export default GALLERY;
