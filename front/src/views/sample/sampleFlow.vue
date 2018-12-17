<template lang="pug">
  vue-waterfall-easy(ref="waterfall",:imgsArr="imgsArr",@scrollReachBottom="getData", @click="clickFn")
    div.detail(slot-scope="props")
      h3.title {{props.value.name}}
      p.name 沈季康
      div.avatar
        Avatar(:src='props.value.icon')
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
  .title {
    height: 100%;
    width: 204px;
    text-align: center;
    margin-top: 15px;
    color: #44484b;
  }
  .avatar{
    margin-top: 15px;
    margin-right: 10px;

  }
  .detail{
    height: 60px;
    display: flex;
    .name{
      margin-top: 21px;
      width: 60px;
      font-size: smaller;
      color: #6b6b6e;
    }
  }
</style>
