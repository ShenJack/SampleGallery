<template>
  <div class="side-menu-wrapper">
    <slot></slot>
    <Menu style="min-height: 100%;height: auto" ref="menu" v-show="!collapsed" :active-name="activeName" :open-names="openedNames" :accordion="accordion" :theme="theme" width="auto" @on-select="handleSelect">
      <template v-for="item in menuList">
        <side-menu-item @on-click="handleSelect" v-if="showChildren(item) && hasPermission($store.state.userInfo.role_names,item.meta.roles)" :key="`menu-${item.name}`" :parent-item="item"></side-menu-item>
        <menu-item v-else-if="item.name && hasPermission($store.state.userInfo.role_names,item.meta.roles)" :name="`${item.name}`" :key="`menu-${item.name}`"><i class="iconfont" :class="item.icon"/><span>{{ showTitle(item) }}</span></menu-item>
      </template>
    </Menu>
    <div class="menu-collapsed" v-show="collapsed" :list="menuList">
      <collapsed-menu @on-click="handleSelect" hide-title :root-icon-size="rootIconSize" :icon-size="iconSize" :theme="theme" v-for="item in menuList" :parent-item="item" :key="`drop-menu-${item.name}`"></collapsed-menu>
    </div>
  </div>
</template>
<script>
import sideMenuItem from "./side-menu-item.vue";
import Menu from "./menu";
import collapsedMenu from "./collapsed-menu.vue";
import { getIntersection } from "../../libs/tools";
import {hasPermission} from "Utils/auth";
import mixin from "./mixin";
export default {
  name: "sideMenu",
  mixins: [mixin],
  components: {
    sideMenuItem,
    collapsedMenu,
    Menu
  },
  props: {
    menuList: {
      type: Array,
      default() {
        return [];
      }
    },
    collapsed: {
      type: Boolean
    },
    theme: {
      type: String,
      default: "light"
    },
    rootIconSize: {
      type: Number,
      default: 20
    },
    iconSize: {
      type: Number,
      default: 16
    },
    accordion: {
      type:Boolean,
      default:false,
    },
    openNames: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      openedNames: [],
      activeName:-1,
    };
  },
  methods: {
    hasPermission,
    handleSelect(name) {
      this.$router.push({ name: name });
    },
    getOpenedNamesByActiveName(name) {
      return this.$route.matched
        .map(item => item.name)
        .filter(item => item !== name);
    }
  },
  watch: {
    activeName(name) {
      if (this.accordion)
        this.openedNames = this.getOpenedNamesByActiveName(name);
      else
        this.openedNames = getIntersection(
          this.openedNames,
          this.getOpenedNamesByActiveName(name)
        );
    },
    openNames(newNames) {
      this.openedNames = newNames;
    },
    openedNames() {
      this.$nextTick(() => {
        this.$refs.menu.updateOpened();
      });
    },
    $route(to,from){
      let name = to.name;
      this.activeName = name;
    }
  },
  mounted() {
    this.openedNames = getIntersection(
      this.openedNames,
      this.getOpenedNamesByActiveName(name)
    );
  }
};
</script>
<style lang="less">
@import "side-menu.less";
</style>
