<style scoped>
  .layout {
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 4px;
    width: 100%;
    height: 100%;
  }

  .menu-item span {
    display: inline-block;
    overflow: hidden;
    width: 69px;
    text-overflow: ellipsis;
    white-space: nowrap;
    vertical-align: bottom;
    transition: width .2s ease .2s;
  }

  .menu-item i {
    transform: translateX(0px);
    transition: font-size .2s ease, transform .2s ease;
    vertical-align: middle;
    font-size: 16px;
  }

  .collapsed-menu span {
    width: 0px;
    transition: width .2s ease;
  }

  .collapsed-menu i {
    transform: translateX(5px);
    transition: font-size .2s ease .2s, transform .2s ease .2s;
    vertical-align: middle;
    font-size: 22px;
  }
</style>

<style>
  .menu .ivu-menu-light {
    height: -webkit-fill-available;
  }
</style>
<template>
  <div class="layout">
    <Layout style="height: 100%">
      <myheader></myheader>
      <Layout>
        <Sider
          style="width: 200px;position: fixed;min-height: 100%;background:white;overflow-y: scroll;height: -webkit-fill-available"
          ref="side1" hide-trigger collapsible :collapsed-width="78" v-model="isCollapsed">
          <side-menu accordion ref="sideMenu" :active-name="$route.name" :menu-list="routes">
          </side-menu>
        </Sider>
        <Content style="padding:20px 20px 0 220px;background: white">
          <router-view></router-view>
          <loadingPage/>
        </Content>
      </Layout>
    </Layout>
    <BackTop></BackTop>
  </div>
</template>
<script>
  import loadingPage from 'Components/LoadingPage/LoadingPage'
  import sideMenu from '../components/menu/side-menu'
  import breadcrumb from '../components/breadcrumb'
  import userIcon from '../components/user_icon'
  import store from '../service/store/common'
  import {currentUser} from "../service/api/user";
  import minLogo from '@/assets/fertilizer.png'
  import myheader from 'Components/header'

  export default {
    name: "base_layout",
    components: {sideMenu, myheader, userIcon, breadcrumb, loadingPage, navigator},
    created() {
    },
    data() {
      return {
        isCollapsed: false,
        minLogo
      }
    },
    computed: {
      rotateIcon() {
        return [
          'menu-icon',
          this.isCollapsed ? 'rotate-icon' : ''
        ];
      },
      menuitemClasses() {
        return [
          'menu-item',
          this.isCollapsed ? 'collapsed-menu' : ''
        ]
      },
      routes() {
        return this.$router.options.routes
      },
      currentUser() {
        return store.state.userInfo
      }
    },
    methods: {
      collapsedSider() {
        this.$refs.side1.toggleCollapse();
      },
    }
  }
</script>
<style>
  @import '../style.css';

  .ivu-form-item .ivu-form-item-label {
    min-width: 80px;
  }

  .ivu-input-wrapper {
    width: 200px;
  }

  *::-webkit-scrollbar {
    width: 2px;
    height: 2px;
    background-color: #F5F5F5;
  }

  /*定义滚动条轨道 内阴影+圆角*/
  *::-webkit-scrollbar-track {
    border-radius: 2px;
  }

  /*定义滑块 内阴影+圆角*/
  *::-webkit-scrollbar-thumb {
    border-radius: 1px;
    -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, .3);
    background-color: rgba(85, 85, 85, 0.39);
  }

  .ivu-input-wrapper {
    width: 90%;
  }

</style>
