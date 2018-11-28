import Vue from 'vue'
import Echarts from 'vue-echarts'
// import 'Components'// 全局组件注册
import 'Directives' // 指令
// 引入插件
import router from 'Plugins/router'
import inject from 'Plugins/inject'
import store from 'Plugins/store'
import Print from 'Plugins/print'
import iView from 'iview';
import 'iview/dist/styles/iview.css';
// 引入根组件
import App from './App'
import {initializerConsts} from "Const/index"
window.vbus = new Vue()
import {initGlobalNotice} from "./service/notice";

// initializerConsts();

Vue.use(inject);
Vue.use(iView);
Vue.use(Print); // 注册
Vue.component('chart', Echarts);
// render
let vm = new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: {App}
});

initGlobalNotice(vm)






