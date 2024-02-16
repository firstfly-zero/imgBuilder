import localeLogin from '@/views/login/locale/zh-CN';

import localeSuccess from '@/views/result/success/locale/zh-CN';
import localeError from '@/views/result/error/locale/zh-CN';

import localeSettings from './zh-CN/settings';

export default {
  'menu.gallery': '图库管理',
  'menu.image': '图片管理',
  'menu.album': '相册管理',
  'nav.logout': '退出登录',

  'menu.robot': '机器人管理',
  'menu.robot.weixin': '微信机器人',
  'menu.robot.lark': '飞书机器人',

  'menu.dashboard': '仪表盘',
  'menu.server.dashboard': '仪表盘-服务端',
  'menu.server.workplace': '工作台-服务端',
  'menu.server.monitor': '实时监控-服务端',
  'menu.list': '列表页',
  'menu.result': '结果页',
  'menu.exception': '异常页',
  'menu.form': '表单页',
  'menu.profile': '详情页',
  'menu.visualization': '数据可视化',
  'menu.user': '个人中心',
  'menu.manage': '管理中心',
  'menu.arcoWebsite': 'Arco Design',
  'menu.faq': '常见问题',
  'navbar.docs': '文档中心',
  'navbar.action.locale': '切换为中文',
  ...localeSettings,
  ...localeLogin,

  ...localeSuccess,
  ...localeError,
};
