<template>
    <div id="table">
        <p id="tableName">{{tableName}}</p>
        <Table id="tableContent" :border="true" :columns = "tableColumns" :show-header="false" :data = "tableData"></Table>
    </div>
</template>
<script>
export default {
  data() {
    return {
    tableName:"肥料消费记录",
      tableColumns: [
        {
          width:150,
          title: "",
          key: "key",
          render: (h, params) => {
                            return h('div', [
                                h('strong', params.row.key)
                            ]);
                        }
        },
        {
          title: " ",
          key: "value"
        }
      ],
      tableData:[
          {
              key:"配肥站名称",
              value:"大坝村配肥站"
          },
          {
              key:"农户",
              value:"王大宝"
          },
          {
              key:"肥料的类别",
              value:"氮肥"
          },
          {
              key:"所属包",
              value:"XB０９８７１"
          },
          {
              key:"价格",
              value:"５７.６"
          }
      ]
    };
  }
};
</script>
<style  scoped>
#tableContent{
    margin-top: 20px;
}
#tableName{
    font-size: 20px;
}
#table{
    margin-left: 50px;
    margin-top: 50px;
    margin-right: 50px;
}
</style>

