<template>
  <div>
    <div class="table" id="detail-table">
      <Row>
        <p class="tableName">我的信息
        </p>


        <Button @click="back" class="save-button"
        >返回
        </Button>

        <Button v-bind:disabled="!savable" @click="save_back" class="save-button"
        >保存并返回列表
        </Button>
        <Button v-bind:disabled="!savable" @click="save" class="save-button"
                type="primary">保存
        </Button>

      </Row>
      <Form ref="formValidate" class="form" label-position="right" :rules="ruleValidate" :model="currentData">
        <Divider orientation="left">基本信息</Divider>


        <div class="form-level">

          <FormItem class="form-item"
                    label="昵称" prop="name">
            <Input @on-change="change" v-model="currentData.first_name" placeholder="请输入"
                   style="width: 300px"/></FormItem>

        </div>


        <div class="form-level">

          <FormItem class="form-item"
                    label="用户名" prop="username">
            <Input @on-change="change" v-model="currentData.username" placeholder="请输入" disabled
                   style="width: 300px"/></FormItem>


        </div>


        <div class="form-level">

          <FormItem class="form-item"
                    label="电话" prop="telephone">
            <Input @on-change="change" v-model="currentData.telephone" placeholder="请输入"
                   style="width: 300px"/></FormItem>


        </div>


        <div class="form-level">

          <FormItem class="form-item"
                    label="邮箱" prop="email">
            <Input @on-change="change" v-model="currentData.email" placeholder="请输入"
                   style="width: 300px"/></FormItem>


        </div>


        <div class="form-level">

          <FormItem class="form-item"
                    label="密码">
            <Button @click="editPassword">修改密码</Button>
          </FormItem>

        </div>

      </Form>

    </div>


    <!--<div class="table children-table">-->
      <!--<Divider-->
        <!--orientation="left">店铺-->

        <!--<Icon type="ios-arrow-forward"/>-->
        <!--{{shop.srcData.name}}-->
        <!--<Button @click="this.shop.goto" style="margin:0 0 2px 10px">-->
          <!--<Icon type="md-arrow-forward"></Icon>-->
        <!--</Button>-->
      <!--</Divider>-->

      <!--<Table class="tableContent" :columns=shop.columns :data=shop.data-->
             <!--:show-header=shop.showHeader></Table>-->

    <!--</div>-->


    <br>
    <br>
    <br>

    <EditPasswordDialog :showModal="showEditPassword"
                        @ok="passwordOk"
                        @cancel="passwordCancel"
    ></EditPasswordDialog>
  </div>
</template>
<script>
  import {
    currentUser,
    editUser,
  } from "Api/user";
  import {getName} from "Const/index"
  import {updateWithinField} from "Utils/tools"
  import {getRole_namesSelect} from "Const/index"
  import EditPasswordDialog from './EditPasswordDialog'

  export default {
    components:{
      EditPasswordDialog
    },
    data() {
      return {
        savable: false,
        next_editable: true,
        srcData: {},
        loadingCount: 0,
        showEditPassword:false,
        id: '',
        currentData: {
          first_name: "",
          username: "",
          telephone: "",
          email: "",
          shop_id: "",
        },
        ruleValidate: {
          role_names: [
            {required: true, type: 'array', trigger: 'change', message: "职位有误"},
          ],
          username: [
            {required: true, trigger: 'change', message: "用户名有误"},
          ],
          telephone: [
            {required: true, trigger: 'change', message: "电话有误"},
          ],
          email: [
            {required: true, type: 'email', trigger: 'change', message: "邮箱有误"},
          ],
          password: [
            {required: true, trigger: 'change', message: "密码有误"},
          ],
          shop_id: [
            {required: true, type: 'number', trigger: 'change', message: "店铺有误"},
          ],
        },

        role_namesSelect: [],
        shop_idSelect: [],
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

        shop: {
          goto: () => {
            this.$router.push({
              name: '店铺详情',
              params: {id: this.shop.srcData.id}
            });
          },
          data:
            []
          ,

          columns: [
            {
              width: 150,
              title: "",
              key: "key",
              render: (h, params) => {
                return h("div", [h("strong", getName(params.row.key))]);
              }
            },
            {
              title: "",
              key: "value",
              render: (h, params) => {
                if (params.row.key === 'icon_url')
                  return h("div", [h("img", {
                    attrs: {
                      src: params.row.value
                    },
                    style: {
                      height: '45px',
                      width: '70px'
                    }
                  }),]);
                else return h("div", [h("p", (params.row.value))]);
              }
            }
          ],
          showHeader: false,

        },


      }
    },
    computed: {

      shopPages() {
        return {
          "_page": this.shop.currentPage
        }
      },

    },
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
          updateWithinField(this.currentData, this.srcData)
        }
      }
    },
    methods: {
      getName,
      prepare_save() {
        return editUser(this.srcData.id, this.currentData);
      },


      fetchSelect() {

      },

      fetchData() {
        currentUser().then((response) => {
          let remoteData = response.data;
          this.srcData = response.data;
          this.id = response.data.id;
          updateWithinField(this.currentData, this.srcData)
          // Object.keys(remoteData.shop).forEach((key) => {
          //   this.shop.data.push({
          //     key: key,
          //     value: remoteData.shop[key]
          //   })
          // });
          this.fetchSelect();
        })
      },
      change() {
        this.savable = true;
      },

      // 修改并返回到列表
      save_back() {
        this.$refs.formValidate.validate((valid) => {
          if (valid) {
            this.prepare_save().then((response) => {
              if (response.data.code === 200) {
                this.$Message.success("修改成功");
                this.$router.push(this.$route.matched[this.$route.matched.length - 2].path)
              } else {
                this.$Message.error("修改失败");
              }
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
              if (response.data.code === 200) {
                this.$Message.success("修改成功");
              } else {
                this.$Message.error("修改失败");
              }
            });
          } else {
            this.$Message.error('填写有误!');
          }
        })
      },

      // 修改下一个

      changePage(page) {
        this.childCurrentPage = page;
        this.fetchChild();
      },

      passwordOk(){
          this.showEditPassword = false
          this.fetchData()
      },

      passwordCancel(){
        this.showEditPassword = false
      },

      gotoDetail(name, param) {
        this.$router.push({name: name,})
      },

      editPassword(){
        this.showEditPassword = true
      }
    }
    ,
    created() {
      this.fetchData();

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

</style>

