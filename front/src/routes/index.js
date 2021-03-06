export default [
  {
    path: "/",
    icon: "icon-home",
    redirect: '/sample',
    meta: {
      roles: [
        'manager',
        'user'
      ]
    },
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
    name: "标本馆",
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
      name: "标本列表",
      path: "", // xzl
      component: resolve => require(['Views/sample/sampleFlow'], resolve),
      meta: {
        visible: false,
        roles: [

          'manager',
          'user'

        ]
      }
    },
      {
        name: "标本详情",
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
  }
  , {
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
      name: "标本列表",
      path: "", // xzl
      component: resolve => require(['Views/sample/sampleList'], resolve),
      meta: {
        visible: false,
        roles: [
          'user'

        ]
      }
    },
    ]
  },
  {
    name: "标本管理",
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
      name: "标本列表",
      path: "", // xzl
      component: resolve => require(['Views/sample/sampleList'], resolve),
      meta: {
        visible: false,
        roles: [

          'manager',

        ]
      }
    },

    ]
  },
  {
    name: "外借管理",
    path: "/lend",
    component: resolve => require(['Views/index'], resolve),
    redirect: "/lend",
    meta: {
      visible: true,
      roles: [
        'manager',
      ]
    },
    icon: "icon-tudi",
    children: [{
      name: "外借管理",
      path: "", // xzl
      component: resolve => require(['Views/borrow/borrowList'], resolve),
      meta: {
        visible: false,
        roles: [
          'manager',
        ]
      }
    },

    ]
  },
  {
    name: "我的外借",
    path: "/lend",
    component: resolve => require(['Views/index'], resolve),
    redirect: "/lend",
    meta: {
      visible: true,
      roles: [
        'user'
      ]
    },
    icon: "icon-tudi",
    children: [{
      name: "外借列表",
      path: "", // xzl
      component: resolve => require(['Views/borrow/borrowList'], resolve),
      meta: {
        visible: false,
        roles: [
          'user'
        ]
      }
    },
    ]
  }
]


