<template>
  <Modal
    v-model="showModal"
    title="修改密码"
  >
    <Form ref="formValidate" class="form" label-position="left" :rules="ruleValidate">
      <FormItem label="新密码" style="margin-bottom: 30px;" prop="firstPassword">
        <Input type="password" v-model="firstPassword" placeholder="请输入"
               style="width: 300px"/>
      </FormItem>
      <FormItem label="再次输入" style="margin-bottom: 10px;" prop="secondPassword">
        <Input type="password" v-model="secondPassword" placeholder="请输入"
               style="width: 300px"/>
      </FormItem>
    </Form>
    <div slot="footer">
      <i-button type="text" size="large" @click.native="cancel">取消</i-button>
      <i-button type="primary" size="large" @click.native="ok">修改</i-button>
    </div>
  </Modal>
</template>
<script>
  import {currentUser,editUser} from "../../service/api/user";


  export default {
    name: 'edit_password',
    props: {
      showModal: {Boolean, default: false}
    },
    data() {
      return {
        srcData: {},
        firstPassword: "",
        secondPassword: "",
        ruleValidate: {
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
          secondPassword: [
            {
              required: true, validator: (rule, value, callback) => {
                if (this.firstPassword === this.secondPassword) {
                  callback();
                } else {
                  callback(new Error("两次密码不一致"))
                }
              },
              trigger: 'change'
            }
          ]
        }
      }
    },
    computed: {},
    methods: {
      ok() {
        this.$refs.formValidate.validate((result) => {
          if (result) {
            currentUser().then(resp => {
              this.srcData = resp.data.user;
              this.srcData.password = this.secondPassword;
              editUser(this.srcData.name,this.srcData).then(
                (response)=>{
                this.$Message.success("密码修改成功")
                this.$emit('ok')
              }
            )
            })

          } else {
            this.$Message.error("密码填写有误")
          }
        })

      },
      onShowChange(){
        if(this.showModal){

        }else{
          this.firstPassword = ""
          this.secondPassword = ""
        }
      },
      cancel() {
        this.$emit('cancel')
      }
    }
  }
</script>
