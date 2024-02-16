import { AppRouteRecordRaw } from '../types';
import { DEFAULT_LAYOUT } from '../base';

const ROBOT: AppRouteRecordRaw = {
    path: '/robot',
    name: 'robot',
    component: DEFAULT_LAYOUT,
    meta: {
        locale: 'menu.robot',
        requiresAuth: true,
        icon: 'icon-robot',
        roles: ['admin','userVip1','userVip2','userVip3','userVip4'],
        order: 2
    },
    children: [
        {
            path: '/weixin',
            name: 'weixin',
            component: () => import('@/views/robot/weixin/index.vue'),
            meta: {
                locale: 'menu.robot.weixin',
                requiresAuth: true,
                roles: ['admin','userVip1','userVip2','userVip3','userVip4'],
            },
        },
        {
            path: '/lark',
            name: 'lark',
            component: () => import('@/views/robot/lark/index.vue'),
            meta: {
                locale: 'menu.robot.lark',
                requiresAuth: true,
                roles: ['admin','userVip1','userVip2','userVip3','userVip4'],
            },
        },
    ],
};

export default ROBOT;
