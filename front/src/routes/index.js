
export default [
  {
    name: "首页",
    path: "/",
    icon: "icon-home",
    redirect: '/',
    meta: {
      roles: [
        'manager',
        'user'
      ]
    },
    component: resolve => require(['Views/index'], resolve),
    children: [{
      path: "",
      name: "首页",
      component: resolve => require(['Views/Home'], resolve),
      meta: {
        roles: [
          'manager',
          'user'
        ]
      },
    },]
  },
  {
    path: "/login",
    component: resolve => require(['Views/LoginPage/index'], resolve),
  },
  {
    path: "/my_info",
    icon: 'icon-info',
    redirect: "/my_info",
    component: resolve => require(['Views/index'], resolve),
    meta: {
      roles: [
        'manager',
        'user'
      ],
    },
    children: [
      {
        path: "",
        name: "我的信息",
        icon: 'icon-info',
        component: resolve => require(['Views/MyInfo/MyInfo'], resolve),
        meta: {
          roles: [
            'manager',
            'user'
          ]
        }
      },
    ]
  },
  {
    name: "样本馆",
    path: "/sample",
    component: resolve => require(['Views/index'], resolve),
    redirect: "/sample",
    meta: {
      visible: true,
      roles: [
        'manager',
        'user'
      ]
    },
    icon: "icon-tudi",
    children: [{
      name: "样本列表",
      path: "", // xzl
      component: resolve => require(['Views/sample/sampleList'], resolve),
      meta: {
        visible: false,
        roles: [

          'manager',
          'user'

        ]
      }
    },
      {
        name: "样本详情",
        path: ":id", // xzl
        component: resolve => require(['Views/sample/sampleDetail'], resolve),
        meta: {
          visible: false,
          roles: [

            'manager',
            'user'

          ]
        }
      }
    ]
  },{
    name: "我的上传",
    path: "/my_sample",
    component: resolve => require(['Views/index'], resolve),
    redirect: "/my_sample",
    meta: {
      visible: true,
      roles: [
        'user'
      ]
    },
    icon: "icon-tudi",
    children: [{
      name: "样本列表",
      path: "", // xzl
      component: resolve => require(['Views/sample/sampleList'], resolve),
      meta: {
        visible: false,
        roles: [
          'user'

        ]
      }
    },
      {
        name: "样本详情",
        path: ":id", // xzl
        component: resolve => require(['Views/sample/sampleDetail'], resolve),
        meta: {
          visible: false,
          roles: [
            'user'

          ]
        }
      }
    ]
  },
  {
    name: "审核",
    path: "/review",
    component: resolve => require(['Views/index'], resolve),
    redirect: "/review",
    meta: {
      visible: true,
      roles: [
        'manager',
      ]
    },
    icon: "icon-tudi",
    children: [{
      name: "样本列表",
      path: "", // xzl
      component: resolve => require(['Views/sample/sampleList'], resolve),
      meta: {
        visible: false,
        roles: [

          'manager',

        ]
      }
    },
      {
        name: "样本详情",
        path: ":id", // xzl
        component: resolve => require(['Views/sample/sampleDetail'], resolve),
        meta: {
          visible: false,
          roles: [

            'manager',

          ]
        }
      }
    ]
  }
]


