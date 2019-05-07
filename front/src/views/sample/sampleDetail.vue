<template>
  <div>
    <div class="table" id="detail-table">
      <Row>
        <p class="tableName">样本
          <span v-if="editableData.name">
                <Icon type="ios-arrow-forward"/>
                {{editableData.name}}
            </span>
          <span v-else-if="editableData.id">
                <Icon type="ios-arrow-forward"/>
                {{editableData.id}}
            </span>
          <span v-else></span>
        </p>


        <Button @click="back" class="save-button"
        >返回
        </Button>

        <Button v-if="isOwner || isManager" v-bind:disabled="!savable" @click="save_back" class="save-button"
        >保存并返回列表
        </Button>
        <Button v-if="isOwner || isManager" v-bind:disabled="!savable" @click="save" class="save-button"
                type="primary">保存
        </Button>

        <Button v-if="!srcData.reviewed && isManager" type="error" @click="reject" class="save-button"
        >拒绝
        </Button>
        <Button v-if="!srcData.reviewed && isManager" w @click="pass" class="save-button"
                type="primary">通过
        </Button>
        <template v-if="srcData.reviewed  && srcData.lendStatus!=='UA' && !isManager && !isOwner"  >
          <Button v-if="srcData.lendStatus!=='LT' && srcData.lendStatus!=='WT'" @click="borrow" class="save-button"
                  type="primary">申请借阅
          </Button>
          <Button v-else @click="borrow" class="save-button"
                  disabled>已借出
          </Button>
        </template>

      </Row>
      <Form ref="formValidate" class="form" label-position="left" :rules="ruleValidate" :model="editableData">
        <Divider orientation="left">基本信息</Divider>


        <div class="form-level">


          <FormItem class="form-item"
                    label="名称" prop="name">
            <Input :disabled="!isOwner" @on-change="change" v-model="editableData.name" placeholder="请输入"
                   style="width: 300px"/></FormItem>


        </div>


        <div class="form-level">


          <FormItem class="form-item"
                    label="描述" prop="description">
            <Input :disabled="!isOwner" type="textarea" @on-change="change" v-model="editableData.description"
                   placeholder="请输入"
                   style="width: 300px"/></FormItem>


        </div>
        <div class="form-level">
          <FormItem class="search-item" label="可以提交实物样本" prop="isEntity">
            <Checkbox :disabled="!isOwner" @on-change="change" v-model="editableData.isEntity" placeholder="请输入"
                      style="width: 30px"/>
            <Button @click="getCode" v-if="editableData.isEntity && srcData.checkinStatus === 'WA' && isOwner">获取验证码</Button>
          </FormItem>
        </div>

        <div class="form-level">
          <FormItem class="search-item" label="菌种" prop="bacteria">
            <AutoComplete :disabled="!isOwner" @on-change="change" v-model="editableData.bacteria" placeholder="请输入"
                          style="width: 300px"/>
          </FormItem>
        </div>
        <div class="form-level">
          <FormItem class="search-item" label="培养基" prop="bacteria">
            <AutoComplete :disabled="!isOwner" @on-change="change" v-model="editableData.medium" placeholder="请输入"
                          style="width: 300px"/>
          </FormItem>
        </div>


        <div class="form-level">


          <FormItem class="form-item" style="display: flex"
                    label="分享自">
            <Tooltip :content="'联系方式:' + srcData.uploader.email" placement="right-end">
              <p
                style="" disabled>{{srcData.uploader.name}}</p>
              <Avatar :src='srcData.uploader.icon'></Avatar>
            </Tooltip>


          </FormItem>


        </div>


        <Divider orientation="left">图片</Divider>

        <div class="form-level">

          <FormItem class="form-item">
            <div style="    display: flex; flex-wrap: wrap;">
              <div class="demo-upload-list" v-for="item in uploadList">
                <template v-if="item.status === 'finished'">
                  <img width="100" height="100" :src="item.url" style="object-fit: cover">
                  <div class="demo-upload-list-cover">
                    <Icon type="ios-eye-outline" @click.native="handleView(item)"></Icon>
                    <Icon v-if="isOwner" type="ios-trash-outline" @click.native="handleRemove(item)"></Icon>
                  </div>
                </template>
                <template v-else>
                  <Progress v-if="item.showProgress" :percent="item.percentage" hide-info></Progress>
                </template>
              </div>
              <Upload
                v-if="isManager||isOwner"
                class="upload"
                ref="upload"
                :show-upload-list="false"
                :on-success="handleSuccess"
                :format="['jpg','jpeg','png']"
                :on-format-error="handleFormatError"
                :on-exceeded-size="handleMaxSize"
                :before-upload="handleBeforeUpload"
                multiple
                type="drag"
                action="/upload/image"
                style="display: inline-block;width:150px;height: 150px">
                <div style="width: 150px;height:150px;line-height: 150px;">
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

    </div>

    <br>
    <br>
    <br>

  </div>
</template>
<script>
  import {
    getSamples,
    getSample,
    editSample
  } from "Api/sample";
  import {getName} from "Const/index"
  import {updateWithinField} from "Utils/tools"
  import {getCodeForSample, passSample, rejectSmple} from "../../service/api/sample";
  import {isManager} from "../../utils/auth";
  import {borrow} from "../../service/api/borrow";


  export default {


    data() {
      return {
        isManager: false,
        isOwner: false,
        visibleItem: {},
        visible: false,
        pics: [],
        uploadList: [],
        loaded: false,
        savable: false,
        next_editable: true,
        srcData: {},
        loadingCount: 0,
        id: '',
        editableData: {


          name: "",
          description: "",
          isEntity: false,
          bacteria: "",
          medium: "",


        },
        ruleValidate: {


          name: [
            {required: true, trigger: 'change', message: "名称有误"},
          ],


          description: [
            {required: true, trigger: 'change', message: "描述有误"},
          ],


          uploader: [
            {required: true, type: 'number', trigger: 'change', message: "农户编号有误"},
          ],


        },


        tableColumns:
          [
            {
              width: 150,
              title: "",
              key: "key",
              render: (h, params) => {
                return h("div", [h("strong", getName(params.row.key))]);
              }
            },
            {
              title: " ",
              key: "value",
              render: (h, params) => {
                return h("div", [h("p", (params.row.value))]);
              }
            }
          ],


      }
    },
    computed: {},
    watch: {
      $route(to, from) {
        this.fetchData();
        this.fetchSelect();
        if (!to.query.next) {
          this.next_editable = false;
        }
      },
      loadingCount: function (newValue, oldValue) {
        if (newValue === 0 && oldValue === 1) {
          updateWithinField(this.editableData, this.srcData)
          this.loaded = true;
        }
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
        this.change()
      },
      handleSuccess(res, file) {
        let image = {}
        image.url = res.path;
        image.name = res.id;
        image.id = res.id;
        image.status = 'finished';
        this.uploadList.push(image)
        this.change();
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
      getName,
      prepare_save() {

        this.editableData.pics = this.uploadList;
        return editSample(this.$route.params.id, this.editableData);

      },


      fetchSelect() {


        updateWithinField(this.editableData, this.srcData)
        this.loaded = true


      },


      fetchData() {

        getSample(this.$route.params.id).then((response) => {
          let remoteData = response.data;
          this.srcData = response.data;
          this.isOwner = this.$store.state.userInfo.id === this.srcData.uploader.id || isManager();
          this.id = response.data.id;
          this.editableData.id = response.data.id;
          this.fetchChild();
          this.fetchSelect();

          this.pics = response.data.pics;

          this.pics.forEach(pic => {
            let image = {}
            image.url = pic.path;
            image.id = pic.id;
            image.status = 'finished';
            this.uploadList.push(image)
          })

        })

      },
      change() {
        if (this.loaded) {
          this.savable = true;
        }
      },

      reject() {
        rejectSmple(this.$route.params.id).then((resp) => {
          this.$Message.warning("已拒绝")
        })
      },

      pass() {
        passSample(this.$route.params.id).then(resp => {
          this.$Message.warning("已通过")
        })
      },
      // 修改并返回到列表
      save_back() {
        this.$refs.formValidate.validate((valid) => {
          if (valid) {
            this.prepare_save().then((response) => {
              this.$Message.success("修改成功");
              this.$router.push(this.$route.matched[this.$route.matched.length - 2].path)
            });
          } else {
            this.$Message.error('填写有误!');
          }
        })
      },

      //返回
      back() {
        if (this.savable) {
          this.$Modal.confirm({
            title: '提示',
            content: '<p>放弃修改并返回？</p>',
            onOk: () => {
              this.$router.go(-1)
            },
            onCancel: () => {
            }
          });
        } else {
          this.$router.go(-1)
        }

      },


      save() {
        this.$refs.formValidate.validate((valid) => {
          if (valid) {
            this.prepare_save().then((response) => {
              this.$Message.success("修改成功");
              this.$router.go(-1)
              this.savable = false
            }).catch(err => {
              this.$Message.error("修改失败");
            });
          } else {
            this.$Message.error('填写有误!');
          }
        })
      },

      // 修改下一个
      edit_next() {
        if (this.$route.query.next) {
          this.$router.push({name: this.$route.matched.name, params: {id: this.$route.query.next}});
        }
      },

      changePage(page) {
        this.childCurrentPage = page;
        this.fetchChild();
      },

      borrow(){
        borrow(this.srcData.id).then(resp=>{
          this.$Modal.success({
            title: '借阅成功',
            content: "请前往我的外借查看详细的借阅信息",
            onOk: () => {
              // this.$Message.info('Clicked ok');
            },
          })
          this.fetchData()
        })
      },

      gotoDetail(name, param) {
        this.$router.push({name: name,})
      },

      fetchChild() {

      },

      getCode() {
        getCodeForSample(this.srcData.id).then(resp => {
          let content = []
          content.push('<p>您的验证码：</p>');
          content.push('<h2>')
          content.push(resp.data.checkinCode+'</h2>');
          this.$Modal.info({
            title: '使用下方验证码到博物馆提交样本',
            content: content.join(" "),
            onOk: () => {
              // this.$Message.info('Clicked ok');
            },
          })
          ;
        })
      },

    }
    ,
    created() {
      this.fetchData();
      this.isManager = isManager();
    }
  }
</script>
<style>

  .form {
    margin-top: 10px;
    margin-left: 10px;
  }

  .form-item {
    margin-bottom: 12px;
  }

  .tableContent {
    margin-top: 20px;
  }

  .tableName {
    font-size: 20px;
    width: 200px;
    float: left;
  }

  .save-button {
    float: right;
    margin-left: 10px;
  }

  .table {
    margin-left: 50px;
    margin-top: 50px;
    margin-right: 50px;
  }

  .children-table-name {
    font-size: 15px;
    margin-bottom: 10px;
  }

  .json-pair {
    margin-bottom: 10px;
  }

  .upload .ivu-upload-drag {
    width: 150px;
  }

</style>
<style scoped>
  .demo-upload-list {
    display: inline-block;
    width: 150px;
    height: 150px;
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

