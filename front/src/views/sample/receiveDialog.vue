<template>
  <Modal
    v-model="showModalLocal"
    title="Common Modal dialog box title"
    v-bind:ok-text=okText
    cancel-text="取消"
    :closable="false"
    :mask-closable="false"
  >
    <p slot="header" style="color:#529bff;text-align:center">
      <Icon type="information-circled"></Icon>
      <span>{{title}}</span>
    </p>

    <Form ref="formValidate" class="form" label-position="left" :rules="ruleValidate">
      <Divider orientation="left">验证码 <small>（不区分大小写）</small></Divider>
      <div class="form-level">
        <FormItem class="search-item" prop="name">
          <Input v-model="code" placeholder="请输入"
                 style="width: 300px"/>
        </FormItem>
      </div>
    </Form>
    <div slot="footer">
      <i-button type="text" size="large" @click.native="cancel">{{ cancelText }}</i-button>
      <i-button type="primary" size="large" @click.native="ok">{{okText}}</i-button>
    </div>
  </Modal>
</template>

<script>

  export default {

    name: "addDialog",
    props: {
      useInside: Boolean,
      farmer: Object,
      showModal: Boolean,
      onOk: Function,
      onCancel: Function,
    },
    data() {
      return {
        code:"",
        ruleValidate: {
          code: [
            {required: true, trigger: 'blur', message: "验证码有误"},
          ],

        },
        title: "输入验证码",
        okText: "确定",
        cancelText: "取消",
      }
    },
    computed: {
      showModalLocal() {
        return this.showModal;
      }
    },
    methods: {
      handleView(item) {
        this.visibleItem = item;
        this.visible = true;
      },
      handleRemove(file) {
        const fileList = this.uploadList;
        this.uploadList.splice(fileList.indexOf(file), 1);
      },
      ok() {
        this.$refs.formValidate.validate((valid) => {
          if (valid) {
            this.$emit('onOk', this.code);
          } else {
            this.$Message.error('有误!');
          }
        })
      },
      cancel() {
        this.$emit('onCancel');
      },
      onShowChange() {
        if (this.showModal) {
        }
      },
      fetchSelect() {
      },
      change() {
        this.savable = true;
      },
    },
    mounted: function () {
    }
  };
</script>

<style scoped>
  .form-level {
    margin-bottom: 10px;
  }

  .json-pair {
    margin-bottom: 10px;
  }

  .demo-upload-list {
    display: inline-block;
    width: 60px;
    height: 60px;
    text-align: center;
    line-height: 60px;
    border: 1px solid transparent;
    border-radius: 4px;
    overflow: hidden;
    background: #fff;
    position: relative;
    box-shadow: 0 1px 1px rgba(0, 0, 0, .2);
    margin-right: 4px;
  }

  .demo-upload-list img {
    width: 100%;
    height: 100%;
  }

  .demo-upload-list-cover {
    display: none;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(0, 0, 0, .6);
  }

  .demo-upload-list:hover .demo-upload-list-cover {
    display: block;
  }

  .demo-upload-list-cover i {
    color: #fff;
    font-size: 20px;
    cursor: pointer;
    margin: 0 2px;
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
