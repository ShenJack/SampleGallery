<style lang="less">
  @import './login.less';
</style>

<template>
  <Layout style="height: 100%">
    <myheader :login="true"></myheader>
    <div class="login">
      <div class="login-con">
        <Card icon="log-in" title="欢迎登录" :bordered="false">
          <div class="form-con">
            <login-form @on-success-valid="handleSubmit"></login-form>
          </div>
        </Card>
      </div>
    </div>
  </Layout>
</template>
<script>
  import LoginForm from './components/LoginForm'
  import {loginUser} from '../../service/api/user'
  import {hasPermission} from "Utils/auth";
  import {manage_routes} from "Routes";
  import {currentUser} from "Api/user";
  import {setToken} from "Utils/auth";
  import myheader from 'Components/header'

  export default {
    components: {
      LoginForm, navigator, myheader
    },

    computed: {
      userInfo() {
        return this.$store.state.userInfo
      }
    },
    methods: {
      setToken,

      handleSubmit({userName, password}) {
        loginUser({
          "username": userName,
          "password": password
        }).then((resp) => {
            if (resp.data.code === 500) {
              this.$Message.error('用户名错误密码错误');
            } else {
              this.$Message.success('登陆成功');
              this.setToken(resp.data.token);
              currentUser().then((resp) => {
                this.$store.commit('SET_USER_INFO', resp.data.user);

                if (this.$route.query && this.$route.query.next && this.$route.query.next !== '') {
                  this.$router.push({path: this.$route.query.next})
                } else {
                  this.$router.push({path: '/'})
                }
              }).catch(() => {

              })
            }
          }
        ).catch(() => {

        })
      },


    },
    mounted() {
      this.$route.query.manual = false
    }
  }
</script>

<style>
</style>
