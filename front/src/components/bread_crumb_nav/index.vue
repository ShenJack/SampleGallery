<template>
  <Breadcrumb>
    <BreadcrumbItem v-for="(item, index) in routes" :key="index" :to="item.path">{{item.name}}</BreadcrumbItem>
  </Breadcrumb>
</template>

<script>
    export default {
        name: "bread_crumb_nav",
        data: function () {
          return {
            routes: this.$route.matched
          }
        }
    }
</script>

<style scoped>

</style>
