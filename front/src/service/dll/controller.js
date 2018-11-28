const mock = false;
import mockController from './mockController.js'
import {print} from "../printer/printer";

const controller = mock ? mockController : window.Dll;

export function getSystemState() {
  let state = controller.getSystemState()
  console.log('controller getSystemState' + state)
  return state
}

export function setUpMode(upMode) {
  let result = controller.setUpMode(upMode)
  console.log(result)
  return result
}

// 设置下料模式.
// 输入 downMode: 0 = 精准模式（默认）, 1 = 快速模式
// 返回设置成功（true）或设置失败（false）
export function getWeight1() {
  let result = controller.getWeight1() * 0.0025
  console.log(result)
  return result
}

export function getWeight2() {
  let result = controller.getWeight2() * 0.0025
  console.log(result)
  return result
}

export function setDownMode(downMode) {
  let result = controller.setDownMode(downMode)
  console.log(result)
  return result
}

// 设置各料斗下料重量.
// 输入 W1: 第一料斗下料重量
// 输入 W2: 第二料斗下料重量
// 输入 W3: 第三料斗下料重量
// 输入 W4: 第四料斗下料重量
// 输入 W5: 第五料斗下料重量
// 输入 W6: 第六料斗下料重量
// 返回设置成功（true）或设置失败（false）
export function setWeightList(W1, W2, W3, W4, W5, W6) {
  let result = controller.setWeightList(W1, W2, W3, W4, W5, W6)
  console.log(result)
  return result
}

// 连接PLC控制系统.
// 输入 N1: 与PLC控制器连接的串口号
// 输入 N2: 与第一组压力传感器连接的串口号
// 输入 N3: 与第二组压力传感器连接的串口号
// 返回成功（true）或失败（false）
export function connect_plc(N1, N2, N3) {
  N1 = window.ports[0]
  N2 = window.ports[1]
  N3 = window.ports[2]
  console.log('PORT')
  console.log(N1)
  console.log(N2)
  console.log(N3)
  let result = controller.connect_plc(N1, N2, N3)
  console.log(result)
  return result
}

// 断开PLC控制系统.
// 返回成功（true）或失败（false）
export function disconnect_plc() {
  let result = controller.disconnect_plc()
  console.log(result)
  return result
}

// 运行PLC控制系统. 按照目标下料重量开始下料.
// 返回成功（true）或失败（false）
export function run_plc() {
  let result = controller.run_plc()
  console.log(result)
  return result
}

// 暂停PLC控制系统. 记录当前已下料重量.
// 返回成功（true）或失败（false）
export function pause_plc() {
  let result = controller.pause_plc()
  console.log(result)
  return result
}

// 继续PLC控制系统. 根据当前已下料重量, 按照目标下料重量恢复下料进程.
// 返回成功（true）或失败（false）
export function resume_plc() {
  let result = controller.resume_plc()
  console.log(result)
  return result
}

// 停止PLC控制系统. 重置所有料斗的下料进程.
// 返回成功（true）或失败（false）
export function stop_plc() {
  let result = controller.stop_plc()
  console.log(result)
  return result
}

export function printText(fertilizerInfo) {
  let receipt = [];
  receipt.push("        ");
  receipt.push("北京傲禾测土全国连锁");
  receipt.push("客户姓名: " + fertilizerInfo.farmer.name)
  receipt.push("客户电话:" + fertilizerInfo.farmer.telephone);
  receipt.push("客户地址: " + fertilizerInfo.farmer.address);
  if (fertilizerInfo.farmland.crop_id) {
    receipt.push("田名: " + fertilizerInfo.farmland.name);
    receipt.push("作物: " + fertilizerInfo.farmland.crop.name);
  }
  receipt.push("元素详情：")
  let elements = [];
  fertilizerInfo.element_contain.forEach(item => {
    elements.push(item.name + ': ' + item.value);
  });
  receipt.push(elements.join('  '));
  receipt.push("化肥详情：")
  fertilizerInfo.fertilizer_mixtures.forEach(fertilizer => {
    receipt.push(fertilizer.kind + ":" + fertilizer.fertilizer_name + ":" + fertilizer.weight + " 千克")
  });
  receipt.push("价格：" + fertilizerInfo.package_price + " 元");
  receipt.push("单包重量：" + fertilizerInfo.package_weight + " 千克");
  receipt.push("包数：" + fertilizerInfo.package_num + " 包");
  receipt.push("配肥日期:" + new Date().toLocaleString());
  receipt.push(fertilizerInfo.farmer.shop.name + "智能配肥站");
  receipt.push("联系电话: " + fertilizerInfo.farmer.shop.telephone);
  receipt.push("配肥员: " + fertilizerInfo.farmer.shop.telephone);
  let text = receipt.join("\n  ");
  if (mock) {
    controller.print(text)
  } else {
    print(text)
  }
}
