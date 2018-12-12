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

    <Form ref="formValidate" class="form" label-position="left" :rules="ruleValidate" :model="editableData">
      <Divider orientation="left">基本信息</Divider>
      <div class="form-level">
        <FormItem class="search-item" label="名称" prop="name">
          <Input v-model="editableData.name" placeholder="请输入"
                 style="width: 300px"/>
        </FormItem>
      </div>


      <div class="form-level">
        <FormItem class="search-item" label="描述" prop="description">
          <Input v-model="editableData.description" placeholder="请输入"
                 style="width: 300px"/>
        </FormItem>
      </div>

      <div class="form-level">
        <FormItem label="图片">
          <div style="    display: flex; width: 300px; height: 150px; flex-wrap: wrap;">
            <div class="demo-upload-list" v-for="item in uploadList">
              <template v-if="item.status === 'finished'">
                <img width="58" height="58" :src="item.url">
                <div class="demo-upload-list-cover">
                  <Icon type="ios-eye-outline" @click.native="handleView(item)"></Icon>
                  <Icon type="ios-trash-outline" @click.native="handleRemove(item)"></Icon>
                </div>
              </template>
              <template v-else>
                <Progress v-if="item.showProgress" :percent="item.percentage" hide-info></Progress>
              </template>
            </div>
            <Upload
              ref="upload"
              :show-upload-list="false"
              :default-file-list="defaultList"
              :on-success="handleSuccess"
              :format="['jpg','jpeg','png']"
              :on-format-error="handleFormatError"
              :on-exceeded-size="handleMaxSize"
              :before-upload="handleBeforeUpload"
              type="drag"
              action="/upload/image"
              style="display: inline-block;width:58px;">
              <div style="width: 58px;height:58px;line-height: 58px;">
                <Icon type="ios-camera" size="20"></Icon>
              </div>
            </Upload>
            <Modal title="查看图片" v-model="visible">
              <img :src="visibleItem.url" v-if="visible" style="width: 100%">
            </Modal>
          </div>
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
        visibleItem: {},
        defaultList: [],
        imgName: '',
        visible: false,
        uploadList: [],
        files: [],
        ruleValidate: {
          name: [
            {required: true, trigger: 'blur', message: "名称有误"},
          ],
          description: [
            {required: true, trigger: 'blur', message: "描述有误"},
          ],

        },
        loadingStatus: false,
        title: "新建样本",
        okText: "新建",
        cancelText: "取消",
        editableData: {
          name: "",
          description: "",
          uploader: "",
        },
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
      handleSuccess(res, file) {
        let image = {}
        image.url = res.path;
        image.name = res.id;
        image.id = res.id;
        image.status = 'finished';
        this.uploadList.push(image)
      },
      handleFormatError(file) {
        this.$Notice.warning({
          title: 'The file format is incorrect',
          desc: 'File format of ' + file.name + ' is incorrect, please select jpg or png.'
        });
      },
      handleMaxSize(file) {
        this.$Notice.warning({
          title: 'Exceeding file size limit',
          desc: 'File  ' + file.name + ' is too large, no more than 2M.'
        });
      },
      handleBeforeUpload() {
        const check = this.uploadList.length < 9;
        if (!check) {
          this.$Notice.warning({
            title: '最多上传九张照片'
          });
        }
        return check;
      },
      handleUpload(fileList) {
        this.files = fileList;
        return false;
      },
      upload() {

      },
      ok() {
        this.editableData.pics = this.uploadList;
        this.$refs.formValidate.validate((valid) => {
          if (valid) {
            this.$emit('onOk', this.editableData);
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
          this.fetchData();
        }
      },
      fetchSelect() {
      },
      change() {
        this.savable = true;
      },
    },
    mounted: function () {
      this.fetchSelect();
      if (this.useInside) {
        this.editableData.farmer_id = this.farmer.id;
        this.editableData.shop_id = this.farmer.shop_id;
      }
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
