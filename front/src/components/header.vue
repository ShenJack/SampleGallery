<template>
  <Header :style="{padding: 0}" style="height: 64px;width: 100%;-webkit-app-region: drag;min-width: 800px"
          class="layout-header-bar">
    <Row>
      <Col :span="6" style="min-width: 280px">
          <span style="font-size: 30px;margin-left: 24px;color: #eeeeee;">菌物标本信息管理系统</span>
      </Col>
      <Col v-if="!login" :span="3" style="min-width: 230px;margin-left: 10px">
        <breadcrumb style="color:white;"/>
      </Col>
      <div v-if="!login" style="float: right;min-width: 150px">
        <userIcon :login="login" style="margin-right: 30px;-webkit-app-region: no-drag;"></userIcon>
      </div>
    </Row>
  </Header>
</template>

<script>
  import breadcrumb from './breadcrumb'
  import userIcon from './user_icon'

  export default {
    name: 'header',
    components: {userIcon, breadcrumb},
    props: {
      login: {Boolean, default: false}
    },
    data() {
      return {}
    },
  }
</script>

<style scoped>
  .layout {
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 4px;
    width: 100%;
    height: 100%;
  }

  .layout-header-bar {
    background: rgba(97, 118, 116, 0.82);
    color: #DEDEDE;
    box-shadow: 0 1px 1px rgba(0, 0, 0, .1);
  }

  .layout-logo-left {
    width: 90%;
    height: 30px;
    background: #5b6270;
    border-radius: 3px;
    margin: 15px auto;
  }

  .menu-icon {
    transition: all .3s;
  }

  .rotate-icon {
    transform: rotate(-90deg);
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
