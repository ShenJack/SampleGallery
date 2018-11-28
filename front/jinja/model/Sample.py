from .Table import Table


class Sample(Table):
  class_name = "sample"
  class_name_text = "样本"
  list_name = "样本列表"
  icon = 'icon-tudi'
  roles = [
    Table.ROLE_ADMIN,
    Table.ROLE_OWNER,
    Table.ROLE_OPERATOR,
    Table.ROLE_COLLECTOR
  ]
  fields = [
    {
      "key": "id",
      "editable": False,
      "type": "number",
      "visible": True,
      "name": "编号",
      "search": True,
      "max": 1000000000,
      "min": 0,
    },
    {
      "key": "name",
      "editable": True,
      "hide": False,
      "type": "string",
      "required": True,
      "name": "名称",
      "search": True,
    },
    {
      "key": "description",
      "editable": True,
      "hide": False,
      "type": "string",
      "required": True,
      "name": "描述",
      "search": True,
    },
    {
      "key": "uploader",
      "hide": True,
      "editable": True,
      "required": True,
      "ruleType": 'number',
      "search": True,
      "type": "string",
      "name": "农户编号"
    },
  ]
