export default  {
  Info(msg){
    window.vbus.$emit('global.message.info',msg);
  },
  Success(msg){
    window.vbus.$emit('global.message.success',msg);
  },
  Error(msg){
    window.vbus.$emit('global.message.error',msg);
  },
  Warning(msg){
    window.vbus.$emit('global.message.warning',msg);
  }
}

export const initGlobalNotice = (vm)=>{
  window.vbus.$on('global.message.info', (msg) => {
  if (!msg) return
  vm.$Message.info(msg);
})
window.vbus.$on('global.message.success', (msg) => {
  if (!msg) return
  vm.$Message.success(msg);
})
window.vbus.$on('global.message.error', (msg) => {
  if (!msg) return
  vm.$Message.error(msg);
})
window.vbus.$on('global.message.warning', (msg) => {
  if (!msg) return
  vm.$Message.warning(msg);
})
}
