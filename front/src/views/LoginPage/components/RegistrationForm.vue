<template>
  <Form ref="registrationForm" :model="form" :rules="rules" @keydown.enter.native="handleRegistration">
    <FormItem prop="username">
      <Input v-model="form.username" placeholder="请输入用户名">
      <span slot="prepend">
          <Icon :size="16" type="ios-person"></Icon>
        </span>
      </Input>
    </FormItem>
    <FormItem prop="email">
      <Input v-model="form.email" placeholder="请输入邮箱"
      >
      <span slot="prepend">
          <Icon :size="14" type="md-mail"></Icon>
        </span>
      </Input>
    </FormItem>
    <FormItem prop="firstPassword">
      <Input type="password" v-model="firstPassword" placeholder="请输入密码"
      >
      <span slot="prepend">
          <Icon :size="14" type="md-lock"></Icon>
        </span>
      </Input>
    </FormItem>

    <FormItem prop="password">
      <Input type="password" v-model="form.password" placeholder="再次输入"
      >
      <span slot="prepend">
          <Icon :size="14" type="md-lock"></Icon>
        </span>
      </Input>
    </FormItem>
    <FormItem>
      <Button @click="handleRegistration" type="primary" long>注册</Button>
    </FormItem>
  </Form>
</template>
<script>
  export default {
    name: 'registryForm',
    props: {

    },
    data() {
      return {
        form: {
          username: '',
          password: '',
          email:"",
        },
        firstPassword: "",

        rules:{
          username: [
            {
              required: true,
              message:"请输入用户名",
              trigger: 'change',
            }
          ],
          firstPassword: [
            {
              required: true,
              validator: (rule, value, callback) => {
                if (this.firstPassword === '') {
                  callback(new Error("请输入密码"))
                } else {
                  callback();
                }
              },
              trigger: 'change',
            }
          ],
          password: [
            {
              required: true, validator: (rule, value, callback) => {
                if (this.firstPassword === this.form.password) {
                  callback();
                } else {
                  callback(new Error("两次密码不一致"))
                }
              },
              trigger: 'change'
            }
          ],
          email:[
            { required: true, validator: (rule, value, callback) => {
                if (!/^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/.test(this.form.email)) {
                  callback(new Error("邮箱格式错误"));
                } else if(this.form.email.length<=0) {
                  callback(new Error("请输入邮箱"))
                } else {
                  callback()
                }
              },
              trigger: 'change'
            },
          ]

        }

      }
    },
    computed: {
    },
    methods: {
      handleRegistration() {
        this.$refs.registrationForm.validate((valid) => {
          if (valid) {
            this.$emit('on-success-valid',
              this.form
            )
          }
        })
      }

    }
  }
</script>
