<template>
</template>
<script>
  import {eventBus} from "Plugins/eventbus"

  export default {
    name: "loadingPage",
    data() {
      return {
      }
    },
    mounted() {
      this.$Loading.config({
          color: '#2d8cf0',
          failedColor: '#f0ad4e',
          height: 7
      });
      eventBus.$on('loading', (show) => {
        if(show){
          this.$Loading.start();
        }else {
          this.$Loading.finish();
        }
      });
      eventBus.$on("error",()=>{
        this.$Loading.error();
      });

    }
  }
</script>
<style>
  .ivu-spin-fix{
    z-index: 1008;
  }
</style>
