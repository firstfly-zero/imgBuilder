import localeLogin from '@/views/login/locale/en-US';

import localeSuccess from '@/views/result/success/locale/en-US';
import localeError from '@/views/result/error/locale/en-US';

import localeSettings from './en-US/settings';

export default {
  'menu.gallery': 'gallery',
  'menu.image': 'image',
  'menu.album': 'album',
  'nav.logout': 'logout',

  'menu.robot': 'robot',
  'menu.robot.weixin': 'weixin',
  'menu.robot.lark': 'lark',


  'menu.dashboard': 'Dashboard',
  'menu.server.dashboard': 'Dashboard-Server',
  'menu.server.workplace': 'Workplace-Server',
  'menu.server.monitor': 'Monitor-Server',
  'menu.list': 'List',
  'menu.result': 'Result',
  'menu.exception': 'Exception',
  'menu.form': 'Form',
  'menu.profile': 'Profile',
  'menu.visualization': 'Data Visualization',
  'menu.user': 'User Center',
  'menu.manage': 'Manage Center',
  'menu.arcoWebsite': 'Arco Design',
  'menu.faq': 'FAQ',
  'navbar.docs': 'Docs',
  'navbar.action.locale': 'Switch to English',
  ...localeSettings,
  ...localeLogin,

  ...localeSuccess,
  ...localeError,
};
