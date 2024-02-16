import { AppRouteRecordRaw } from '../types';
import { DEFAULT_LAYOUT } from '../base';

const USER: AppRouteRecordRaw = {
    path: '/user',
    name: 'user',
    component: DEFAULT_LAYOUT,
    redirect: "/usercenter",
    meta: {
        locale: 'menu.user',
        requiresAuth: true,
        icon: 'icon-user',
        hideChildrenInMenu: true,
        order: 8
    },
    children: [
        {
            path: '/usercenter',
            name: 'usercenter',
            component: () => import('@/views/user/index.vue'),
            meta: {
                locale: 'menu.user',
                requiresAuth: true,
                roles: ['admin','userVip0','userVip1','userVip2','userVip3','userVip4'],
            },
        },
    ],
};

export default USER;
