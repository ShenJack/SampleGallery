
export const getSelectFor = (childName) => {
  console.log("asd");
  return [
    {
    "id": "ssd",
    "name": "asdas"
  },
    {
    "id": "asd",
    "name": "asdas"
  },
    {
    "id": "asaad",
    "name": "asdas"
  }
  ];
  switch (childName) {
    case "shop":
      return getShops().then((resp => {
        let list = [];
        resp.data.shops.forEach((shop) => {
          list.push({
            "id": shop.id,
            "name": shop.name
          })
        });
        return list;
      }));
    case "crop":
      return getCrops().then(resp => {
        let list = [];
        resp.data.crops.forEach((crop) => {
          list.push({
            "id": crop.id,
            "name": crop.name
          })
        });
        return list;
      });
  }
};

export const checkinStatus = [
  {
    key:"WA",
    value:"未申请"
  },
  {
    key:"",
    value:"全部"
  },
  {
    key:"AP",
    value:"等待入库"
  },
  {
    key:"IS",
    value:"已入库"
  }
]

export const reviewedSelect = [
  {
    key:"true",
    value:"已审核"
  },
  {
    key:"",
    value:"全部"
  },
  {
    key:"false",
    value:"未审核"
  }
]

export const lendStatus = [
  {
    key:"LT",
    value:"已借出"
  },
  {
    key:"WT",
    value:"等待领取"
  },
  {
    key:"AV",
    value:"可借"
  },
  {
    key:"UA",
    value:"不可借"
  },
  {
    key:"",
    value:"全部"
  }
]
