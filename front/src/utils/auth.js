import axios from 'Plugins/axios'

const TokenKey = 'Authorization';

export function getToken() {
  return axios.defaults.headers.common[TokenKey]
}


export function hasPermission(roles, permissionRoles) {
  if (roles.indexOf('manager') >= 0) return true // admin permission passed directly
  if (!permissionRoles) return true
  return roles.some(role => permissionRoles.indexOf(role) >= 0)
}

export function setToken(token) {
  axios.defaults.headers.common[TokenKey] = "Token " + token;
}

