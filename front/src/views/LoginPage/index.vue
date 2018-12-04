<style lang="less">
  @import './login.less';
</style>

<template>
  <Layout style="height: 100%">
    <myheader :login="true"></myheader>
    <div class="login">
      <div class="login-con">
        <Card icon="log-in" :title="login?'欢迎登录':'欢迎注册'" shadow :bordered="true">
          <div class="form-con" >
            <transition name="slide-fade">
            <login-form :username="providedUsername" v-if="login" @on-success-valid="handleLogin"></login-form>
            <RegistrationForm v-else @on-success-valid="handleRegistry"></RegistrationForm>
            </transition>
            <Button @click="login = false" type="text" long v-if="login">注册</Button>
            <Button @click="login = true" type="text" long v-if="!login">返回登录</Button>
          </div>
        </Card>
      </div>
    </div>
  </Layout>
</template>
<script>
  import LoginForm from './components/LoginForm'
  import RegistrationForm from './components/RegistrationForm'
  import {loginUser,registerUser} from '../../service/api/user'
  import {hasPermission} from "Utils/auth";
  import {manage_routes} from "Routes";
  import {currentUser} from "Api/user";
  import {setToken} from "Utils/auth";
  import myheader from 'Components/header'

  export default {
    components: {
      LoginForm, navigator, myheader,RegistrationForm
    },

    computed: {
      userInfo() {
        return this.$store.state.userInfo
      }
    },
    data(){
      return {
        login:true,
        providedUsername:"",
      }
  },
    methods: {
      setToken,

      handleLogin({userName, password}) {
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
                this.$store.commit('SET_USER_INFO', resp.data);

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
      handleRegistry(params){
        registerUser(params).then(resp=>{
          this.$Message.success('注册成功');
          this.providedUsername = resp.data.username;
          this.login = true

        }).catch(error=>{
          if(error.response.status === 400){
            this.$Message.error('用户名已存在');
          }
        })
      }


    },
    mounted() {
      this.$route.query.manual = false
    }
  }
</script>

<style>
</style>
