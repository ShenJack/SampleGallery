// 全局state 存放所有模块，业务线都有可能调用的状态
// 把state放入mutations是为了方便开发，观察状态 ，和状态对应的相关方法

export const state = {
    userInfo: {},
    fertilizerInfo:{
      fertilizer_choose: [], //选择的肥料
      farmer: undefined,
      farmland_id: undefined, // 选择的参考田,
      crop_id: undefined, //选中的作物
      crop: {},
      elements: [], //土地元素,
      ele_mixtures: [], //目标元素配比
      package_weight: 0, //总重量
      pre_weight: 0, // 单包重量
      package_price: 0, // 总价格
      package_num: 0, //总包数
      fertilizer_mixtures: [],  //肥料配比
      element_contain: [],
      farmland: {},
      farmlandSelected: false,
      cropSelected: false,
      price: 0,
      fill_type: 0,
      upMode: 0,
      downMode: 0,
      advance_quantity: [],
      belt_config: {},
    }
};

//全局mutations
export const mutations = {
  ['SET_USER_INFO'](state, resData) {
    state.userInfo = resData
  },
  ['SET_FERTILIZER_INFO'](state, resData) {
    state.fertilizerInfo = resData
  },
  setFarmer(state, farmer) {
    state.fertilizerInfo.farmer = farmer;
  },
  setFarmland(state, farmland) {
    state.fertilizerInfo.farmland = farmland;
  },
  setElements(state, elements) {
    state.fertilizerInfo.elements = elements
  },
  setFertilizerMixture(state, mixtures) {
    state.fertilizerInfo.fertilizer_mixtures = mixtures
  },
  setFertilizerChoose(state, fertilizers) {
    state.fertilizerInfo.fertilizer_choose = fertilizers
  },
  setPackageDetail(state, packageDetail) {
    state.fertilizerInfo.package_num = packageDetail.package_num
    state.fertilizerInfo.package_num = packageDetail.package_weight
  },
  setElementMixtures(state, ele_mixtures) {
    state.fertilizerInfo.ele_mixtures = ele_mixtures
  },
  setElementContain(state, element_contain) {
    state.fertilizerInfo.element_contain = element_contain;
  },
  ['RESET_USER_INFO'](state) {
    state.fertilizerInfo = {
      fertilizer_choose: [], //选择的肥料
      farmer: undefined,
      crop_id: undefined, //选中的作物
      crop: {},
      elements: [], //土地元素,
      ele_mixtures: [], //目标元素配比
      package_weight: 0, //总重量
      pre_weight: 0, // 单包重量
      package_price: 0, // 总价格
      package_num: 0, //总包数
      fertilizer_mixtures: [],  //肥料配比
      element_contain: [],
      farmland: {},
      farmlandSelected: false,
      cropSelected: false,
      price: 0,
      fill_type: 0,
      upMode: 0,
      downMode: 0,
      advance_quantity: [],
      belt_config: {},
    }
  }


}
