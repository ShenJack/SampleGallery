from .Table import Table


class Farmland(Table):
  class_name = "farmland"
  class_name_text = "土地"
  list_name = "土地列表"
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
      "name": "田名",
      "search": True,
    },
    {
      "key": "shop_id",
      "childClassName": 'shop',
      "editable": True,
      "hide": True,
      "ruleType": 'number',
      "required": True,
      "search": True,
      "type": "select",
      "name": "店铺编号"
    },
    {
      "key": "crop_id",

      "editable": True,
      "hide": True,
      "required": True,
      "type": "select",
      "childClassName": 'crop',
      "ruleType": 'number',
      "name": "作物编号",
      "search": True,
    },
    {
      "key": "farmer_id",
      "hide": True,

      "childClassName": 'farmer',
      "editable": True,
      "required": True,
      "ruleType": 'number',
      "search": True,
      "type": "select",
      "name": "农户编号"
    },
    {
      "key": "farmer",
      "editable": False,
      "type": "child",
      "display_key": "name",
      "hideInDetail": True,
      "childType": "detail",
      "array": False,
      "link": "/crop/:id",
      "name": "农户"
    },
    {
      "key": "elements",
      "editable": True,
      "required": True,
      "hide": True,
      "display_key": "name",
      "select_key": "element",
      "type": "json",
      "name": "元素",
    },

  ]
