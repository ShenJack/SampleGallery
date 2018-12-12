<template>
  <div class="table-card-body">
    <div>
      <Form v-if="!useInside" class="form" label-position="left" inline>


        <FormItem class="search-item" label="名称">
          <Input class="search-item-input" v-model="searchObject.name"
                 placeholder="请输入" clearable></Input>
        </FormItem>


        <FormItem class="search-item" label="描述">
          <Input class="search-item-input" v-model="searchObject.description"
                 placeholder="请输入" clearable></Input>
        </FormItem>


        <FormItem class="search-item" label="上传自">
          <Input class="search-item-input" v-model="searchObject.uploader"
                 placeholder="请输入" clearable></Input>
        </FormItem>


        <FormItem class="search-item">
          <Button id="search-button" @click="search" type="primary">查询</Button>
          <Button id="reset-button" @click="resetSearch" style="margin-left: 10px">重置</Button>
        </FormItem>
      </Form>

    </div>

    <Row class="table-operator-level">
      <Button @click="add" id="add-button" size="large" type="primary" icon="plus-round">上传样本</Button>
    </Row>

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
  </div>
</template>
<script>
  import addDialog from "./addDialog"
  import {getName,getState} from "Const"
  import {
    getSamples,
    deleteSample,
    editSample,
    addSample
  } from "Api/sample"
  import {getColor} from "../../service/const";


  export default {
    components: {
      addDialog
    },
    props: {
      query: Object,
      useInside: Boolean,
      farmer: Object,
    },
    data() {
      return {
        itemCount: 0,
        currentPage: 1,
        showEdit: false,
        showAdd: false,
        editingId: "",
        searchObject: {

          id: "",


          name: "",


          description: "",


          uploader: "",


        },
        loading: false,

        columns: [


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
            title: "分享者",
            key: "uploader",
            render: (h, params) => {
              return h("div", [h("p", getName(params.row.uploader))]);
            }
          },
          {
            title: "审核状态",
            key: "reviewState",
            render: (h, params) => {
              return h("div", [h("p",{style:{color:getColor(params.row.reviewState)}} ,getName(params.row.reviewState))]);
            }
          },
          {
            title: "操作",
            width: 200,
            align: "center",
            render: (h, params) => {
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
      }
    },
    methods: {
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
              if (response.data.code === 200) {
                this.$Message.success("删除成功");
                this.fetchData();
              }
            });
          },
          onCancel: () => {

          }
        });


      },
      add() {
        this.showAdd = true;
      }
      ,
      resetSearch() {
        Object.keys(this.searchObject).forEach((key) => {
          this.searchObject[key] = "";
        });
        this.search();
      }
      ,
      search() {
        let args = {...this.searchObject, ...this.pages};
        getSamples(args).then((response) => {
          this.data = response.data.results;
        })
      }
      ,
      refresh() {
        this.search();
      }
      ,
      fetchData() {
        let args = {...this.searchObject, ...this.pages};
        getSamples(args).then((response) => {
          this.data = response.data.results;
          this.itemCount = response.data.count;
        })
      }
      ,
      addOk(data) {
        this.showAdd = false;
        addSample(data).then((response) => {
            if (response.data.code === 200) {
              this.$Message.success("新建成功");
              this.fetchData();
            }
          }
        );
      }
      ,
      addCancel() {
        this.showAdd = false;
      }
      ,
      fetchSelect() {

      }
      ,


      changePage(page) {
        this.currentPage = page;
        this.fetchData();
      },

    },


    mounted: function () {

      this.fetchData();
      this.fetchSelect();
    }
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


