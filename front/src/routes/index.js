
export default [
  {
    name: "首页",
    path: "/",
    icon: "icon-home",
    redirect: '/',
    meta: {
      roles: [
        'admin',
        'owner',
        'collector',
        'operator'
      ]
    },
    component: resolve => require(['Views/index'], resolve),
    children: [{
      path: "",
      name: "首页",
      component: resolve => require(['Views/Home'], resolve),
      meta: {
        roles: [
          'admin',
          'owner',
          'collector',
          'operator'
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
        'admin',
        'owner',
        'collector',
        'operator'
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
            'admin',
            'owner',
            'collector',
            'operator'
          ]
        }
      },
    ]
  },
  {
    name: "样本",
    path: "/sample",
    component: resolve => require(['Views/index'], resolve),
    redirect: "/sample",
    meta: {
      visible: true,
      roles: [

        'admin',

        'owner',

        'operator',

        'collector',

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

          'admin',

          'owner',

          'operator',

          'collector',

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

            'admin',

            'owner',

            'operator',

            'collector',

          ]
        }
      }
    ]
  }
]


