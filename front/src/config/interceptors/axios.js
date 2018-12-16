import {CONSOLE_REQUEST_ENABLE} from '../index.js'
import {cleanEmptyFields} from "Utils/tools"
import {eventBus} from "Plugins/eventbus"
import {API_URL, NODE_ENV} from "../index";
import router from "Plugins/router"
import store from "Plugins/store"

export function requestSuccessFunc(requestObj) {
  CONSOLE_REQUEST_ENABLE && console.info('requestInterceptorFunc', `url: ${requestObj.url}`, requestObj)
  // 自定义请求拦截逻辑，可以处理权限，请求发送监控等
  // ...

  // 清除空项时 给 非 admin的用户 加上默认的 查询 店铺id
  if (requestObj.method === "get" && requestObj.params
  ) {
    if (requestObj.params.shop_id === '' && !store.state.userInfo.role_names.some(item => item === 'admin')) {
      requestObj.params.shop_id = store.state.userInfo.shop_id;
    }
    requestObj.params = cleanEmptyFields(requestObj.params);
  }
  // 清除 get时 值为空 的项

  if (requestObj.method === "post") {
    requestObj.data = cleanEmptyFields(requestObj.data);
  }

  //通知 eventBus 开始加载
  eventBus.$emit("loading", true);

  //重写 product环境下的 api url
  if (NODE_ENV === 'prod') {
    requestObj.url = API_URL + requestObj.url;
  }

  return requestObj
}

export function requestFailFunc(requestError) {
  // 自定义发送请求失败逻辑，断网，请求发送监控等
  // ...
  return Promise.reject(requestError);
}

export function responseSuccessFunc(responseObj) {
  // 自定义响应成功逻辑，全局拦截接口，根据不同业务做不同处理，响应成功监控等
  // ...
  // 假设我们请求体为
  // {
  //     code: 1010,
  //     msg: 'this is a msg',
  //     data: null
  // }

  let resData = responseObj;
  let {code} = resData;
  eventBus.$emit("loading", false);
  switch (code) {
    case 200: // 如果业务成功，直接进成功回调
      resData.success = true;
      return resData;
    case 401:
      // 如果业务失败，根据不同 code 做不同处理
      // 比如最常见的授权过期跳登录
      // 特定弹窗
      // 跳转特定页面等

      // location.href = xxx // 这里的路径也可以放到全局配置里
      return resData;
    default:
      // 业务中还会有一些特殊 code 逻辑，我们可以在这里做统一处理，也可以下方它们到业务层
      // !responseObj.config.noShowDefaultError && GLOBAL.vbus.$emit('global.$dialog.show', resData.msg);
      return resData;

  }
}

export function responseFailFunc(responseError) {
  // 响应失败，可根据 responseError.message 和 responseError.response.status 来做监控处理
  // ...
  let stauts = responseError.response.status;
  switch (stauts) {
    case 401:
      if (router.currentRoute.path === '/login') {
        window.vbus.$emit('global.message.warning', "用户名或密码错误");
      } else {
        window.vbus.$emit('global.message.warning', "请登录");
        router.push({path: "/login"});
      }
      break;
    case 400:
      window.vbus.$emit('global.message.error', responseError.response.data.error);
      break;
    default:
      CONSOLE_REQUEST_ENABLE && console.info('requestInterceptorFunc', `url: ${responseError.url}`, responseError)
      window.vbus.$emit('global.message.error', "系统异常");
      eventBus.$emit("error");

  }

  return Promise.reject(responseError);
}
