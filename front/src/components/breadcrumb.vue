<template>
  <div>
    <Breadcrumb >
      <BreadcrumbItem style="-webkit-app-region: no-drag;" class="breadcrumb-item" v-for="(item, index) in routes" :key="index" :to="item.path">{{item.name}}</BreadcrumbItem>
    </Breadcrumb>
  </div>
</template>
<script>
  export default {
    name: "Breadcrumbs",
    mounted() {
      this.updateList();
    },
    watch: {
      $route(from, to) {
        this.updateList();
      }
    },
    data() {
      return {
        routes: [] // 路由集合
      };
    },
    methods: {
      updateList() {
        this.routes = [];
        var lastRoute = {
          name: '首页',
          path: '/'
        };
        this.routes.push(lastRoute);
        this.$route.matched.forEach(item => {
          if (item.name !== lastRoute.name) {
            this.routes.push(item);
          }
          lastRoute = item
        })
      },
    }
  };
</script>
<style>
  .ivu-breadcrumb a{
    color: white;

  }
  .ivu-breadcrumb a:hover{
    color:#cccccc
  }
</style>
