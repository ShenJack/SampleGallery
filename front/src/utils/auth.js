import axios from 'Plugins/axios'

const TokenKey = 'Authorization';

import store from '../plugins/store'

export function getToken() {
  return axios.defaults.headers.common[TokenKey]
}


export function hasPermission(permissionRoles) {
  return store.state.userInfo.groups.some(role => permissionRoles.indexOf(role) >= 0)
}

export function setToken(token) {
  axios.defaults.headers.common[TokenKey] = "Token " + token;
}

export function clearToken() {
  delete axios.defaults.headers.common[TokenKey]
}
