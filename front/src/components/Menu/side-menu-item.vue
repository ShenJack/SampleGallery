<template>
  <Submenu :name="`${parentName}`">
    <template slot="title">
      <i class="iconfont" :class="parentItem.icon"></i>
      <span>{{ showTitle(parentItem) }}</span>
    </template>
    <template v-for="item in children">
      <side-menu-item v-persi="[sdf]" v-if="showChildren(item)" :key="`menu-${item.name}`" :parent-item="item"></side-menu-item>
      <menuItem v-else-if="item.name&&hasPermission(item.meta.roles)" :name="`${item.name}`" :key="`menu-${item.name}`"><i class="iconfont" :class="item.icon"/><span>{{ showTitle(item) }}</span></menuItem>
    </template>
  </Submenu>
</template>
<script>
import mixin from './mixin'
import menuItem from './menu-item'
import itemMixin from './item-mixin'
import Submenu from './submenu'
import {hasPermission} from "Utils/auth";

export default {
  name: 'sideMenuItem',
  components:{
    menuItem,
    Submenu
  },
  methods:{
    hasPermission
  },
  mixins: [ mixin, itemMixin ]
}
</script>
