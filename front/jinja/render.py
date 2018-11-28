from jinja2 import Environment, FileSystemLoader

from front.jinja.model.Sample import Sample

env = Environment(loader=FileSystemLoader('.'))
listTemplate = env.get_template('./template/list.vue.j2')
dialogTemplate = env.get_template('./template/editDialog.vue.j2')
addDialogTemplate = env.get_template('./template/addDialog.vue.j2')
apiTemplate = env.get_template('./template/api.js.j2')
detailTemplate = env.get_template('./template/detail.vue.j2')
routeTemplate = env.get_template('./template/route.js.j2')
class_list = []
class_list.append(Sample())
for data_class in class_list:
  listPageResult = listTemplate.render({
    "data": data_class
  })
  dialogResult = dialogTemplate.render({
    "data": data_class
  })
  apiResult = apiTemplate.render({
    "data": data_class
  })
  detailResult = detailTemplate.render({
    "data": data_class
  })
  routeResult = routeTemplate.render({
    "data": data_class
  })
  addDialogResult = addDialogTemplate.render(
    {
      "data": data_class
    }
  )
  with open(
    "C:/Users/sjjkk/PycharmProjects/SampleGallery/front/src/views/" + data_class.class_name + "/" + data_class.class_name + "List.vue",
    "w",
    encoding='utf-8') as listFile:
    listFile.write(listPageResult)
  with open("C:/Users/sjjkk/PycharmProjects/SampleGallery/front/src/views/" + data_class.class_name + "/editDialog.vue",
            "w",
            encoding='utf-8') as dialogFile:
    dialogFile.write(dialogResult)
  with open("C:/Users/sjjkk/PycharmProjects/SampleGallery/front/src/views/" + data_class.class_name + "/addDialog.vue",
            "w",
            encoding='utf-8') as addDialogFile:
    addDialogFile.write(addDialogResult)
  with open("C:/Users/sjjkk/PycharmProjects/SampleGallery/front/src/service/api/" + data_class.class_name + ".js", "w",
            encoding='utf-8') as apiFile:
    apiFile.write(apiResult)
  with open(
    "C:/Users/sjjkk/PycharmProjects/SampleGallery/front/src/views/" + data_class.class_name + "/" + data_class.class_name + "Detail.vue",
    "w",
    encoding='utf-8') as detailFile:
    detailFile.write(detailResult)
  with open("C:/Users/sjjkk/PycharmProjects/SampleGallery/front/src/routes/" + data_class.class_name + ".js",
            "w",
            encoding='utf-8') as routeFile:
    routeFile.write(routeResult)
