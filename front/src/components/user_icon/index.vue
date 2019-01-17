<template>
  <div class="user-avator-dropdown" style="display: flex">
    <div style="margin-right: 10px">
      <Avatar :src="$store.state.userInfo.icon"/>
    </div>
    <Dropdown v-show="!login" @on-click="handleClick">
      <span style="margin-right: 3px">{{ $store.state.userInfo.name}} <tag v-if="isManager()">管理员</tag></span>
      <Icon :size="18" type="md-arrow-dropdown"></Icon>
      <DropdownMenu slot="list">
        <DropdownItem name="logout">退出登录</DropdownItem>
        <DropdownItem name="info">我的信息</DropdownItem>
      </DropdownMenu>
    </Dropdown>

  </div>
</template>

<script>
  import {logoutUser} from '../../service/api/user'
  import {clearToken, isManager, setToken} from "../../utils/auth";
  import Notice from "Notice"

  export default {
    name: 'User',
    props: {
      currentUser: Object,
      login: {Boolean, default: false}
    },
    methods: {
      isManager,
      handleClick(name) {
        switch (name) {
          case 'logout':
            clearToken();
            this.$router.push({path: '/login', query: {manual: true}});
            Notice.Info('请重新登录');
            break
          case "shop":
            this.$router.push({path: '/my_shop'});
            break
          case "info":
            this.$router.push({path: '/my_info'});
            break

        }
      },
      minimize() {
        window.electron.minimize()
      },
      maximize() {
        window.electron.maximize()
      },
      close() {
        window.electron.close()
      }
    }
  }
</script>

