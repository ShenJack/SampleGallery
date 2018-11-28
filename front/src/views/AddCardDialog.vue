<template>
  <Modal
    v-model="showModalLocal"
    title="Common Modal dialog box title"
    v-bind:ok-text=okText
    cancel-text="取消"
    :closable="false"
    :mask-closable="false"
    @on-visible-change="onShowChange"
  >
    <p slot="header" style="color:#529bff;text-align:center">
      <Icon type="information-circled"></Icon>
      <span>{{title}}</span>
    </p>

    <Form ref="formValidate" class="form" label-position="left" :rules="formValidate">

      <FormItem
        class="select-item" label="农户卡  "
        prop="card"
      >
        <Input ref="input" v-model="card" placeholder="请刷卡"
               style="width: 300px" @keyup.enter.native="setCard"/>
      </FormItem>

    </Form>
    <div slot="footer">
      <i-button type="text" size="large" @click.native="cancel">{{ cancelText }}</i-button>
    </div>
  </Modal>
</template>

<script>

  import {setCardId} from "Api/card"

  export default {
    name: "addCardDialog",
    props: {
      showModal: Boolean,
      onOk: Function,
      onCancel: Function,
      farmerId:Number
    },
    data() {
      const cardValidator = (rule, value, callback) => {
        switch (this.cardIdState) {
          case 0:
            callback(new Error("请刷卡"));
            break;
          case 1:
            callback(new Error("验证中"));
            break;
          case 2:
            callback();
            break;
        }
        callback();
      }
      return {
        title: "添加卡片",
        okText: "添加",
        cancelText: "取消",
        cardIdState: 0,// 0 :未绑定（绑定错误） 1:等待结果 2:绑定完成
        card:"",
        formValidate:{
          card: [
            {validator: cardValidator, trigger: 'change', message: "请刷卡"},
          ]
        }
      }
    },
    computed: {
      showModalLocal() {
        return this.showModal;
      }
    },
    methods: {
      ok() {
        this.$refs.formValidate.validate((valid) => {
          if (valid) {
            this.$emit('ok');
          } else {
            this.$Message.error('有误!');
          }
        })
      },
      cancel() {
        this.$emit('cancel');
      },
      onShowChange() {
        if(this.showModal){
          this.card = '';
          this.$refs.input.focus()
          console.log('focus')
        }
      },


      setCard() {
        this.cardIdState = 1;
        setCardId(this.farmerId, this.card).then(resp => {
          console.log(resp.data);
          this.cardIdState = 2;
          this.ok()
          this.$Message.success('绑定成功')
        });
      },
    },
  };
</script>

<style scoped>
  .form-level {
    margin-bottom: 10px;
  }

  .json-pair {
    margin-bottom: 10px;
  }


</style>

<style>
  .ivu-modal-body {
    padding-left: 30px;
    padding-right: 30px;
  }

  .ivu-select {
    width: 300px;
  }

  .ivu-select-input {
    width: 300px;
  }

  .ivu-input-wrapper {
    width: 200px;
  }
</style>
