// 全局state 存放所有模块，业务线都有可能调用的状态
// 把state放入mutations是为了方便开发，观察状态 ，和状态对应的相关方法

export const state = {
  userInfo: {},
};

//全局mutations
export const mutations = {
  ['SET_USER_INFO'](state, resData) {
    state.userInfo = resData
  },
}

