<template lang="pug">
  vue-waterfall-easy(ref="waterfall",:imgsArr="imgsArr",@scrollReachBottom="getData", @click="clickFn")
    .img-info(slot-scope="props")
      p.some-info {{props.value.name}}
      p.some-info {{props.value.info}}

    //-div(slot="waterfall-head")
      h1 waterfall-head
      h1 waterfall-head
</template>
<script>

  import vueWaterfallEasy from './vue-waterfall-easy'
  import {getSamples} from "../../service/api/sample";

  export default {
    name: 'app',
    components: {
      vueWaterfallEasy
    },
    data() {
      return {
        imgsArr: [],
      }
    },
    methods: {
      getData() {
        // In the real environment,the backend will return a new image array based on the parameter group.
        // Here I simulate it with a stunned json file.
        let params = {};
        getSamples(params).then((response) => {
          response.data.results.forEach(item => {
            this.imgsArr.push({
              ...item,
              src: item.pics.length > 0 ? item.pics[0].path : '',
              info: item.description,
            })
          })
          // this.data = response.data.results;
          // this.itemCount = response.data.count;

          // this.imgsArr = this.imgsArr.concat(res.data)
          // this.group++
        })
      },
      clickFn(event, { index, value }) {
        debugger

        this.$router.push({
          name: "样本详情",
          params: {id: value.id}})
      },
      goto(id) {
        this.$router.push({
          path: "/sample",
          params: id})
      }
    },
    mounted() {
      this.getData();
    }
  }
</script>
<style lang="scss">
  .some-info {
    line-height: 1.6;
    text-align: center;
    color: #474b4e;
    font-size: larger;
  }
</style>
