<template>
  <div>
    <Modal
      v-model="showModel"
      title="Common Modal dialog box title"
      v-bind:ok-text=okText
      cancel-text="取消"
      @on-ok="ok"
      @on-cancel="cancel">
      <p slot="header" style="color:#529bff;text-align:center">
        <Icon type="information-circled"></Icon>
        <span>{{this.title}}</span>
      </p>
      <div style="text-align:center">
        <div class="form-level">
          名字
          <Input v-model="data.name" prefix="ios-contact" placeholder="请输入名字" style="width: 300px"/>
        </div>
        <div class="form-level">
          地址
          <Input v-model="data.address" prefix="ios-contact" placeholder="请输入名字" style="width: 300px"/>
        </div>
        <div class="form-level">
          电话
          <Input v-model="data.telephone" prefix="ios-contact" placeholder="请输入名字" style="width: 300px"/>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script>
  import {addFarmer,editFarmer} from "Api/farmers"
  import {calculateChangedFields} from "Utils/tools"
  export default {
    name: "new-farmer-dialog",
    props: ["dialogEventHandler"],
    data() {
      return {
        title: "新建农户",
        showModel: false,
        okText: "新建",
        data: {},
        srcData:{},
        type: "add",
      };
    },
    methods: {
      handleRender() {
        this.$Modal.confirm({
          render: h => {
            return h("Input", {
              props: {
                value: this.value,
                autofocus: true,
                placeholder: "请输入"
              },
              on: {
                input: val => {
                  this.value = val;
                }
              }
            });
          }
        });
      },
      ok() {
        if (this.type === "add") {
          addFarmer(this.data).then();
        }else if(this.type === "edit"){
          let changedData = calculateChangedFields(this.srcData,this.data);
          editFarmer(this.srcData.id,changedData).then();
        }
      },
      cancel() {
        // this.hide();
      },
      show() {
        this.showModel = true;
        this.title = "新建农户";
        this.okText = "新建";
        this.type = "add";
      },
      showEdit(params) {
        this.showModel = true;
        this.title = "编辑农户";
        this.okText = "修改";
        this.type = "edit";
        Object.keys(params).forEach((key)=>{
          this.data[key] = params[key];
        });
        this.srcData = params;
      },
      hide() {
        // this.dialogEventHandler.hide();
      }
    },
    created: function () {
    }
  };
</script>

<style scoped>
  .form-level {
    margin-bottom: 10px;
  }
</style>
