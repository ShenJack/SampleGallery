<template>
  <div class="table-card-body">
    <div>
      <Form v-if="!useInside" class="form" label-position="left" inline>

        <template v-if="isManager()">
          <FormItem class="search-item">
            <Input v-model="code" @on-search="searchBorrow" search enter-button placeholder="借阅验证码"/>
          </FormItem>
          <FormItem class="search-item">
            <Button id="reset-button" @click="resetSearch" style="margin-left: 10px">重置</Button>
          </FormItem>
        </template>
      </Form>
    </div>

    <Table :columns="columns" :data="data"></Table>
    <div style="margin: 10px;overflow: hidden">
      <div style="float: left;">
        <Page :page-size="20" :total="itemCount" :current="currentPage" @on-change="changePage"></Page>
      </div>
    </div>
  </div>
</template>
<script>
  // import addDialog from "./addDialog"
  import {getName, getState} from "Const"
  import {
    getSamples,
    deleteSample,
    editSample,
    addSample
  } from "Api/sample"
  import {getColor, getTime} from "../../service/const";
  import {reviewedSelect} from "../../service/const/select";
  import {getUsers} from "../../service/api/user";
  import {isManager, isUser} from "../../utils/auth";
  import {checkPick, checkReceive} from "../../service/api/sample";
  import {finishBorrow, getBorrows, passLend, pickBorrow, rejectLend} from "../../service/api/borrow";

  export default {
    components: {},
    props: {
      query: Object,
      useInside: Boolean,
      farmer: Object,
    },
    data() {
      return {
        code: "",
        showReceive: false,
        showPick: false,
        reviewedSelect: reviewedSelect,
        itemCount: 0,
        currentPage: 1,
        showEdit: false,
        showAdd: false,
        editingId: "",
        searchObject: {

          reviewed: undefined,
          id: "",
          name: "",
          description: "",
          uploader: undefined,


        },
        uploaderList: [],
        loading: false,

        columns: [
          {
            title: "借阅人",
            key: "name",
            render: (h, params) => {
              return h("div", [h("p", getName(params.row.from_user.name))]);
            }
          },
          {
            title: "最晚归还日期",
            width: 200,
            key: "latestPickTime",
            render: (h, params) => {
              return h("div", [h("p", getTime(params.row.latestPickTime))]);
            }
          },
          {
            title: "标本名称",
            key: "name",
            render: (h, params) => {
              return h("div", [h("p", getName(params.row.to_sample.name))]);
            }
          },
          {
            title: "状态",
            key: "description",
            render: (h, params) => {
              return h("div", [h("p", getName(params.row.lendState))]);
            }
          },
          {
            title: "审核状态",
            key: "description",
            render: (h, params) => {
              return h("div", [h("p", getName(params.row.checkState))]);
            }
          },
          {
            title: "操作",
            width: 200,
            align: "center",
            render: (h, params) => {
              if (isManager()) {
                let result = []
                if (params.row.checkState === 'NR') {
                  result.push(h(
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
                          this.pass(params.row.id);
                        }
                      }
                    },
                    "通过"
                  ))
                  result.push(h(
                    "Button",
                    {
                      props: {
                        type: "error",
                        size: "small"
                      },
                      on: {
                        click: () => {
                          this.reject(params.row.id);
                        }
                      }
                    },
                    "拒绝"
                    )
                  )
                } else if (params.row.checkState === 'PS') {
                  if (params.row.to_sample.lendStatus === 'LT') {
                    result.push(h(
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
                            this.return(params.row.id);
                          }
                        }
                      },
                      "归还"
                    ))
                  } else if (params.row.to_sample.lendStatus === 'WT') {
                    result.push(h(
                      "Button",
                      {
                        props: {
                          type: "error",
                          size: "small"
                        },
                        on: {
                          click: () => {
                            this.pick(params.row.id);
                          }
                        }
                      },
                      "借出"
                      )
                    )
                  }

                }
                return h("div", result);
              } else {
                if (params.row.checkState === 'PS') {
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
                            this.showCode(params.row.code);
                          }
                        }
                      },
                      "查看借阅码"
                    ),
                  ]);
                } else if (params.row.checkState === 'RJ') {
                  return h("div", "审核未通过");
                } else {
                  return h("div", "等待审核");
                }
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
      }
    },
    methods: {
      searchBorrow(value) {
        this.fetchData({pickCode: value})
      },
      isManager,
      show(index) {
        this.$router.push({
          name: "标本详情",
          params: {id: this.data[index].code},
        });
      },
      showCode(code) {
        let content = []
        content.push('<p>您的验证码：</p>');
        content.push('<h2>')
        content.push(code + '</h2>');
        this.$Modal.info({
          title: '使用下方验证码到领取点领取标本',
          content: content.join(" "),
          onOk: () => {
            // this.$Message.info('Clicked ok');
          }
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
        this.code = "";
        this.fetchData();
      }
      ,
      fetchData(addOnArgs = {}) {
        if (!addOnArgs.hasOwnProperty("checkInCode")) {
          this.searchTarget = "general"
        }
        let args = {...this.searchObject, ...this.pages, ...addOnArgs};
        getBorrows(args).then((response) => {
          this.data = response.data;
        })
      }
      ,
      change() {
        this.fetchData();
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
        if (isManager()) {
          this.getUploaderList();
        }
      }
      ,

      getUploaderList(name) {
        let params = {name: name};
        getUsers(params).then(resp => {
          this.uploaderList = resp.data.results;
        })
      },


      changePage(page) {
        this.currentPage = page;
        this.fetchData();
      },

      pick(id) {
        pickBorrow(id).then(resp => {
          this.$Message.success("借阅成功")
          this.fetchData();

        }).catch(err => {
          this.$Message.error("借阅失败")
          this.fetchData();

        })
      },

      reject(id) {
        rejectLend(id).then((resp) => {
          this.$Message.warning("已拒绝")
          this.fetchData()
        })
      },

      pass(id) {
        passLend(id).then(resp => {
          this.$Message.warning("已通过")
          this.fetchData()
        })
      },
      return(id) {
        finishBorrow(id).then(resp => {
          this.$Message.success("归还成功")
          this.fetchData();

        }).catch(err => {
          this.$Message.error("归还失败")
          this.fetchData();

        })
      },
    },


    mounted: function () {
      if (isUser()) {
        this.columns.splice(0, 1)
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


