export default {
  getSystemState() {
    return 268439560
  }
  ,
  getWeight1() {
    return Math.random()*10 + 20
  }
  ,
  getWeight2() {
    return Math.random()*10 + 40
  }
  ,
  setUpMode(upMode) {
    return true
  }
// 设置下料模式.
// 输入 downMode: 0 = 精准模式（默认）, 1 = 快速模式
// 返回设置成功（true）或设置失败（false）
  ,
  setDownMode(downMode) {
    return true
  }
// 设置各料斗下料重量.
// 输入 W1: 第一料斗下料重量
// 输入 W2: 第二料斗下料重量
// 输入 W3: 第三料斗下料重量
// 输入 W4: 第四料斗下料重量
// 输入 W5: 第五料斗下料重量
// 输入 W6: 第六料斗下料重量
// 返回设置成功（true）或设置失败（false）
  ,

  setWeightList(W1, W2, W3, W4, W5, W6) {
    console.log(W1);
    console.log(W2);
    console.log(W3);
    console.log(W4);
    console.log(W5);
    console.log(W6);
    return true
  }

// 连接PLC控制系统.
// 返回成功（true）或失败（false）
  ,

  connect_plc() {
    return true
  }

// 断开PLC控制系统.
// 返回成功（true）或失败（false）
  ,

  disconnect_plc() {
    return true
  }

// 运行PLC控制系统. 按照目标下料重量开始下料.
// 返回成功（true）或失败（false）
  ,

  run_plc() {
    return true
  }

// 暂停PLC控制系统. 记录当前已下料重量.
// 返回成功（true）或失败（false）
  ,

  pause_plc() {
    return true
  }

// 继续PLC控制系统. 根据当前已下料重量, 按照目标下料重量恢复下料进程.
// 返回成功（true）或失败（false）
  ,

  resume_plc() {
    return true
  }

// 停止PLC控制系统. 重置所有料斗的下料进程.
// 返回成功（true）或失败（false）
  ,

  stop_plc() {
    return true
  },

  print(text){
    console.log(text)
  }

}
