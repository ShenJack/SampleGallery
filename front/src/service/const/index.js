import other from './other'
import {getFertilizerKinds} from 'Api/const'
import store from 'Plugins/store'
export default {
  other
}

const CONST = {
  id: "编号",
  name: "名字",
  address: "地址",
  telephone: "电话",
  shop_id: "店铺编号",
  icon_url: "图片链接",
  note: "备注",
  open: "营业",
  close: "关闭",
  status: "状态",
  unsent: "待发送",
  email: "邮箱",
  operator:'操作员',
  owner:'店主',
  collector:'化验员',
  admin:'管理员',
  in:'入库',
  out:'出库',
  formula:'配方',
  kind:'种类',
  shop:'店铺',
  elements:'元素',
  NR:"待审核",
  RJ:"审核未通过",
  PS:"审核通过",
};

const shop_status = [{
  "key": "open",
  "value": "营业",
}, {
  "key": "close",
  "value": "关闭"
}];

const role_names_for_admin = [{
  "key": "admin",
  "value": "管理员",
},
  {
    "key": "owner",
    "value": "店主",
  },
  {
    "key": "operator",
    "value": "操作员",
  },
  {
    "key": "collector",
    "value": "化验员",
  }
]

const role_names_for_owner = [
  {
    "key": "operator",
    "value": "操作员",
  },
  {
    "key": "collector",
    "value": "化验员",
  }
]

const role_names_for_operator = [
  {
    "key": "collector",
    "value": "化验员",
  }
]

const directions = [
  {
    "key": "in",
    "value": "入",
  },
  {
    "key": "out",
    "value": "出",
  }
]



export const fertilizer_kinds = ['氮肥','磷肥','钾肥','微量肥','特效肥','调理剂'];

export const Elements = ["N", "P", "K"];

export const getName = (key) => {
  if(key instanceof Array){
      return key.map(key=>getName(key)).join('  ')
  }
  return CONST[key] ? CONST[key] : key;
};

export const getElementSelect = () => {
  return Elements;
};

export const getKindSelect = () => {
  return fertilizer_kinds;
};

export const getStatusSelect = () => {
  return shop_status;
};

export const getDirectionSelect = ()=>{
  return directions;
}

export const getRole_namesSelect = () => {
  let role_names = store.state.userInfo.role_names;
  if(role_names.some(item=>item==='admin')){
    return role_names_for_admin;
  }else if(role_names.some(item=>item==='owner')){
    return role_names_for_owner;
  }else if (role_names.some(item => item === 'operator')) {
    return role_names_for_operator;
  }
};


