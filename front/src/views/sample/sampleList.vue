<template>
  <div class="table-card-body">
    <div>
      <Form v-if="!useInside" class="form" label-position="left" inline>


        <FormItem class="search-item" label="名称">
          <Input @on-change="change" class="search-item-input" v-model="searchObject.name"
                 placeholder="请输入" clearable></Input>
        </FormItem>


        <FormItem class="search-item" label="描述">
          <Input @on-change="change" class="search-item-input" v-model="searchObject.description"
                 placeholder="请输入" clearable></Input>
        </FormItem>


        <FormItem v-if="isManager()" class="search-item" label="上传自">
          <Select @on-change="change"
                  class="search-item-input"
                  v-model="searchObject.uploader"
          >
            <Option v-for="item in uploaderList" :value="item.id"
                    :key="item.id"
            >
              {{item.name}}
            </Option>
          </Select>
        </FormItem>
        <FormItem class="search-item" label="审核状态" prop="description">
          <Select @on-change="change"
                  class="search-item-input"
                  v-model="searchObject.reviewed"
          >
            <Option v-for="item in reviewedSelect" :value="item.key"
                    :key="item.value"
                    :label="item.value"
            >
              {{item.value}}
            </Option>
          </Select>
        </FormItem>

        <FormItem class="search-item" label="提交状态" prop="description">
          <Select @on-change="change"
                  class="search-item-input"
                  v-model="searchObject.checkinStatus"
          >
            <Option v-for="item in checkinStatus" :value="item.key"
                    :key="item.value"
                    :label="item.value"
            >
              {{item.value}}
            </Option>
          </Select>
        </FormItem>

        <FormItem class="search-item" label="借阅状态" prop="description">
          <Select @on-change="change"
                  class="search-item-input"
                  v-model="searchObject.lendStatus"
          >
            <Option v-for="item in lendStatus" :value="item.key"
                    :key="item.value"
                    :label="item.value"
            >
              {{item.value}}
            </Option>
          </Select>
        </FormItem>


        <FormItem class="search-item">
          <Button id="search-button" @click="fetchData" type="primary">查询</Button>
          <Button id="reset-button" @click="resetSearch" style="margin-left: 10px">重置</Button>
        </FormItem>
      </Form>

    </div>
    <Row class="table-operator-level">
      <Button @click="add" id="add-button" size="large" type="primary" icon="plus-round">上传样本</Button>
    </Row>
    <Divider></Divider>
    <Form>
      <FormItem class="search-item" v-if="dataIsManager">
        <Input @on-search="searchCheckIn" search enter-button placeholder="接收验证码" />
      </FormItem>
    </Form>
    <Table :columns="columns" :data="data"></Table>
    <div style="margin: 10px;overflow: hidden">
      <div style="float: left;">
        <Page :page-size="20" :total="itemCount" :current="currentPage" @on-change="changePage"></Page>
      </div>
    </div>
    <addDialog
      :useInside="useInside"
      :farmer="farmer"
      :showModal="showAdd"
      @onOk="addOk"
      @onCancel="addCancel"></addDialog>

    <receiveDialog
      :useInside="useInside"
      :showModal="showReceive"
      @onOk="receiveOk"
      @onCancel="receiveCancel"></receiveDialog>
  </div>
</template>
<script>
  import addDialog from "./addDialog"
  import {getName, getState} from "Const"
  import {
    getSamples,
    deleteSample,
    editSample,
    addSample
  } from "Api/sample"
  import {getColor} from "../../service/const";
  import {reviewedSelect,lendStatus,checkinStatus} from "../../service/const/select";
  import {getUsers} from "../../service/api/user";
  import {isManager, isUser} from "../../utils/auth";

  import receiveDialog from './receiveDialog'
  import {checkReceive, dismissReceive} from "../../service/api/sample";


  export default {
    components: {
      addDialog,receiveDialog
    },
    props: {
      query: Object,
      useInside: Boolean,
      farmer: Object,
    },
    data() {
      return {
        searchTarget:"general",
        reviewedSelect: reviewedSelect,
        checkinStatus: checkinStatus,
        lendStatus:lendStatus,
        itemCount: 0,
        currentPage: 1,
        showReceive:false,
        showEdit: false,
        showAdd: false,
        editingId: "",


        searchObject: {

          reviewed: undefined,
          lendStatus:undefined,
          checkinStatus:undefined,


          id: "",


          name: "",


          description: "",


          uploader: undefined,


        },
        uploaderList: [],
        loading: false,

        columns: [

          {
            title: "分享者",
            key: "uploader",
            render: (h, params) => {
              return h("div", [h("p", getName(params.row.uploader.name))]);
            }
          },
          {
            title: "编号",
            width: 60,
            key: "id",
            render: (h, params) => {
              return h("div", [h("p", getName(params.row.id))]);
            }
          },
          {
            title: "名称",
            key: "name",
            render: (h, params) => {
              return h("div", [h("p", getName(params.row.name))]);
            }
          },
          {
            title: "描述",
            key: "description",
            render: (h, params) => {
              return h("div", [h("p", getName(params.row.description))]);
            }
          },
          {
            title: "提交状态",
            key: "checkinStatus",
            render: (h, params) => {
              return h("div", [h("p", getName(params.row.checkinStatus))]);
            }
          },
          {
            title: "借阅状态",
            key: "lendStatus",
            render: (h, params) => {
              return h("div", [h("p", getName(params.row.lendStatus))]);
            }
          },

          {
            title: "审核状态",
            key: "reviewState",
            render: (h, params) => {
              return h("div", [h("p", {style: {color: getColor(params.row.reviewState)}}, getName(params.row.reviewState))]);
            }
          },
          {
            title: "操作",
            width: 200,
            align: "center",
            render: (h, params) => {
              if(this.searchTarget === "general"){
                return h("div", [
                  h(
                    "Button",
                    {
                      props: {
                        type: "primary",
                        size: "small"
                      },
                      style: {
                        marginRight: "5px"
                      },
                      on: {
                        click: () => {
                          this.show(params.index);
                        }
                      }
                    },
                    "查看"
                  ),
                  h(
                    "Button",
                    {
                      props: {
                        type: "error",
                        size: "small"
                      },
                      on: {
                        click: () => {
                          this.remove(params.index);
                        }
                      }
                    },
                    "删除"
                  )
                ]);
              }else if(this.searchTarget==="checkInCode"){
                return h("div", [
                  h(
                    "Button",
                    {
                      props: {
                        type: "primary",
                        size: "small"
                      },
                      style: {
                        marginRight: "5px"
                      },
                      on: {
                        click: () => {
                          this.receiveOk(params.row.id);
                        }
                      }
                    },
                    "接收"
                  ),
                  h(
                    "Button",
                    {
                      props: {
                        type: "error",
                        size: "small"
                      },
                      on: {
                        click: () => {
                          this.dismissCheckIn(params.row.id);
                        }
                      }
                    },
                    "拒绝"
                  )
                ]);
              }
            }
          }


        ],
        data: []
      };
    },
    computed: {
      pages() {
        return {
          "_page": this.currentPage
        }
      },
      dataIsManager(){
        return this.isManager()
      },
    },
    methods: {
      isManager,
      isUser,
      show(index) {
        this.$router.push({
          name: "样本详情",

          params: {id: this.data[index].id},

        });
      },
      remove(index) {
        this.$Modal.confirm({
          title: '提示',
          content: '<p>确认删除？</p>',
          onOk: () => {
            deleteSample(this.data[index].id).then((response) => {
                this.$Message.success("删除成功");
                this.fetchData();
            });
          },
          onCancel: () => {

          }
        });

      },
      searchCheckIn(checkInCode){
        this.searchTarget = "checkInCode";
        this.fetchData({checkInCode:checkInCode})
      },
      receiveOk(id){
        checkReceive(id).then(resp=>{
          this.$Message.success("接收成功")
        }).catch(err=>{
          this.$Message.error("接收失败")
        })
        this.fetchData()
      },
      dismissCheckIn(id){
        dismissReceive(id).then(resp=>{
          this.$Message.success("已拒绝")
        }).catch(err=>{
          this.$Message.error("拒绝失败请重试")
        })
        this.fetchData()
      },
      add() {
        this.showAdd = true;
      }
      ,
      resetSearch() {
        Object.keys(this.searchObject).forEach((key) => {
            this.searchObject[key] = "";
        });
        this.fetchData();
      }
      ,
      fetchData(addOnArgs={}) {
        if(!addOnArgs.hasOwnProperty("checkInCode")){
          this.searchTarget = "general"
        }
        let args = {...this.searchObject, ...this.pages,...addOnArgs};
        if(isUser()){
          args.personal = true;
        }
        getSamples(args).then(
          (response) => {
          this.data = response.data;
        })
      }
      ,
      change() {
        // this.fetchData();
      },
      addOk(data) {
        this.showAdd = false;
        addSample(data).then((response) => {
              this.$Message.success("新建成功");
              this.fetchData();
          }
        );
      }
      ,
      addCancel() {
        this.showAdd = false;
      }
      ,
      fetchSelect() {
        if(isManager()){
          this.getUploaderList();
        }
      }
      ,

      getUploaderList(name) {
        let params = {name:name};
        getUsers(params).then(resp=>{
          this.uploaderList = resp.data.results;
        })
      },


      changePage(page) {
        this.currentPage = page;
        this.fetchData();
      },

    },


    mounted: function () {
      if(isUser()){
        this.columns.splice(0,1)
        this.searchObject.uploader = this.$store.state.userInfo.id;
      }
      this.fetchData();
      this.fetchSelect();
    },
  }
  ;
</script>
<style>
  .table-card-body {
    padding: 24px;
  }
</style>
<style scoped>
  .search-item {
    width: 32%;
  }

  .search-item-text {
    float: left;
  }

  .search-item-input {
    float: left;
    margin-left: 10px;
    width: 60%;
  }

  .table-card-body {
    padding: 24px;
  }

  #search-button,
  #add-button {
  }

  .search-bar {
  }

  .table-operator-level {
    margin-bottom: 10px;
  }
</style>


