type_select = 'select'
type_string = 'string'
type_number = 'number'
type_child = 'child'
type_json = 'json'
type_time = 'time'

class Table:
  # 允许访问的权限名 （枚举）
  ROLE_ADMIN = 'admin'
  ROLE_OWNER = 'owner'
  ROLE_OPERATOR = 'operator'
  ROLE_COLLECTOR = 'collector'
  class_name = None
  class_name_text = None
  icon = ''
  fields = [
    {
      "required": True,
      "required": False,
      "key": "example_key",  # 字段在response中的key
      "editable": True,  # or False 能否在客户端编辑
      "type": "child",  # 声明为child的type 需要额外的
      # number:数字 string:字符串 child:子结构 select:选择框
      "type": "child",  # 声明为child的type 需要额外的 childType , childClass
      # "childType": "detail", detail：是一个详细内容（dict） list：是一个列表（array）
      # "childClass": Shop(), child对应的类
      "display_key": "",  # 设置child中的一个字段用来显示在列表中
      "hide": True,  # 是否显示在列表中
      "visible": True,  # 空置
    },
    {
      "key": "id",
      "editable": False,
      "type": "select",  # 类的所有 select 字段会被汇总 用于获取select 选项
      "const_select": True,  # 下拉可选项是否为常量：True：从本地常量库获取列表 False：根据指定的 childClassName 来调用对应的api获取列表
      "childClassName": 'shop',  # 如上： childClassName
      "has_value": True,  # 可选项是简单枚举 还是 键值对
      "multiple": True,  # 在编辑时是否可以多选
      "name": "序号",
      "max": 1000000000,
      "min": 0,
    },
    {
      "key": "id",
      "editable": False,
      "type": "number",
      "name": "序号",
      "max": 1000000000,  # 对于数字的大小显示
      "min": 0,
    },
    {
      "key": "id",
      "editable": False,
      "type": "string",
      "name": "序号",
      "length": 8,  # 长度
      "search": True,  # search：True 当前字段可以在列表页被检索
    }
  ]
  # 用于检索（筛选和查找）的字段列表

  childs = [
    {
      "key": "farmlands",  # child 在 response 里的key
      "childClass": "",  # child 对应的class
      "type": "list",  # child 为 键值对 还是 列表
    },
  ]

  def selectFields(self):
    group = []
    for field in self.fields:
      if field['type'] == type_select:
        group.append(field)
    return group

  def searchFields(self):
    group = []
    for field in self.fields:
      try:
        if field['search']:
          group.append(field)
      except KeyError as error:
        print("")
    return group

  def childs(self):
    group = []
    for field in self.fields:
      try:
        if field['type'] == type_child:
          group.append(field)
      except KeyError:
        print(None)
    return group

  def jsonFields(self):
    group = []
    for field in self.fields:
      try:
        if field['type'] == type_json:
          group.append(field)
      except KeyError:
        print(None)
    return group

  def fetchSelectFields(self):
    group = []
    for field in self.fields:
      if field['type'] == type_select and 'const_select' not in field:
        group.append(field)
    return group

  def timeFields(self):
    group = []
    for field in self.fields:
      try:
        if field['type'] == type_time:
          group.append(field)
      except KeyError as error:
        print("")
    return group
