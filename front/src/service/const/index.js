import other from './other'
import {getFertilizerKinds} from 'Api/const'
import store from 'Plugins/store'

export default {
  other
}

const CONST = {
  id: "编号",
  name: "名字",

  //审核状态
  NR: "待审核",
  RJ: "审核未通过",
  PS: "审核通过",

  //借阅状态
  UA: "不可借",
  AV: '可借',
  WT: '等待领取',
  LT: '已借出',

  //申请提交状态
  WA: '未申请',
  AP: '等待入库',
  IS: '已入库',

};


export const getColor = (key) => {
  switch (key) {
    case 'NR':
      return 'rgb(81, 90, 110)'
    case 'RJ':
      return 'red'
    case 'PS':
      return 'green'
  }
}

export const getName = (key) => {
  if (key instanceof Array) {
    return key.map(key => getName(key)).join('  ')
  }
  return CONST[key] ? CONST[key] : key;
};


export const getRole_namesSelect = () => {
  let role_names = store.state.userInfo.role_names;
  if (role_names.some(item => item === 'admin')) {
    return role_names_for_admin;
  } else if (role_names.some(item => item === 'owner')) {
    return role_names_for_owner;
  } else if (role_names.some(item => item === 'operator')) {
    return role_names_for_operator;
  }
};


