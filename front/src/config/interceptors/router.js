import router from 'Plugins/router'
import store from 'Plugins/store'
import {currentUser} from '../../service/api/user'
import {getToken} from 'Utils/auth'
import {manage_routes} from "../../routes";
import {hasPermission} from "Utils/auth"


export function routerBeforeEachFunc(to, from, next) {
  // 这里可以做页面拦截，很多后台系统中也非常喜欢在这里面做权限处理
  if (to.path !== '/login') {
    currentUser().then(resp => {
      if (hasPermission(store.getters.userinfoGetter.role_names, to.meta.roles)) {
        next()
      } else {
        //没有权限
        next({path: '/401', replace: true, query: {noGoBack: true}})
      }
    }).catch(() => {
      next({path: '/login', query: {next: to.path, manual: true}},)
    })

    if (getToken()) {
      if (hasPermission(store.getters.userinfoGetter.role_names, to.meta.roles)) {
        next()
      } else {
        //没有权限
        next({path: '/401', replace: true, query: {noGoBack: true}})
      }
    } else {
      //  token 失效
      next({path: '/login', query: {manual: true}})
    }

  } else if (to.query.manual) {
    next()
  } else {

  }
}
