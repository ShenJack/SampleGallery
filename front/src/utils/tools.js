import qs from 'qs'

export function getNumb() {
    var num = new Array();
    for (var i = 0; i < 10; i++) {
        var val = Math.ceil(Math.random() * 30);
        var isEqu = false;
        for (var idx in num) {
            if (num[idx] == val) {
                isEqu = true;
                break;
            }
        }
        if (isEqu) i--;
        else num[num.length] = val;
    }
    return num;
};

// scrollTop animation
export function scrollTop(el, from = 0, to, duration = 500) {
    if (!window.requestAnimationFrame) {
        window.requestAnimationFrame = (
            window.webkitRequestAnimationFrame ||
            window.mozRequestAnimationFrame ||
            window.msRequestAnimationFrame ||
            function(callback) {
                return window.setTimeout(callback, 1000 / 60);
            }
        );
    }
    const difference = Math.abs(from - to);
    const step = Math.ceil(difference / duration * 50);

    function scroll(start, end, step) {
        if (start === end) return;

        let d = (start + step > end) ? end : start + step;
        if (start > end) {
            d = (start - step < end) ? end : start - step;
        }

        if (el === window) {
            window.scrollTo(d, d);
        } else {
            el.scrollTop = d;
        }
        window.requestAnimationFrame(() => scroll(d, end, step));
    }
    scroll(from, to, step);
}

export function assert(condition, msg) {
    if (!condition) throw new Error(`[Apior] ${msg}`)
}

export function updateWithinField(src_obj, des_obf) {
  /* 用于更新src_obj的字典用另一个*/
  for (let item in src_obj) {
    if (des_obf.hasOwnProperty(item)){
      // 存在更新src
      src_obj[item] = des_obf[item]
    } else {
      // 不存在至空
      src_obj[item] = undefined
    }
  }
}

export function calculateChangedFields(src_object,new_object) {
  let changedFields = {};
  Object.keys(new_object).forEach((key)=>{
    if(new_object[key]!==src_object[key]){
      changedFields[key] = new_object[key];
    }
  })
  return changedFields;
}

export function cleanEmptyFields(object) {
  Object.keys(object).forEach((key)=>{
    if( object[key]===undefined || object[key]===""){
      delete object[key];
    }
  });
  return object;
}

// stringifyQuery

export function stringifyQuery(args) {
  return qs.stringify(args, {
    arrayFormat: 'repeat',
    allowDots: true
})
}

// parseQuery
export function parseQuery(str) {
  return qs.parse(str, {
    arrayFormat: 'repeat',
    allowDots: true
  })
}

//时间转换
export function dateToString (date, format) {
  let args = {
    "M+": date.getMonth() + 1,
    "d+": date.getDate(),
    "h+": date.getHours(),
    "m+": date.getMinutes(),
    "s+": date.getSeconds(),
    "q+": Math.floor((date.getMonth() + 3) / 3),  //quarter
    "S": date.getMilliseconds()
  };
  if (/(y+)/.test(format))
    format = format.replace(RegExp.$1, (date.getFullYear() + "").substr(4 - RegExp.$1.length));
  for (let i in args) {
    let n = args[i];
    if (new RegExp("(" + i + ")").test(format))
      format = format.replace(RegExp.$1, RegExp.$1.length === 1 ? n : ("00" + n).substr(("" + n).length));
  }
  return format;
};

export function cut_string (src, len) {

  // 按照len分割字符src
  let buf = []
  let res = []
  for (let i in src){
    buf.push(src[i])
    if (buf.length === len){
      res.push(buf.slice())
      buf.length = 0
    }
  }
  if(buf.length !==0){
    res.push(buf.slice())
  }
  return res
}
