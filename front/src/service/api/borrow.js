import axios from "Plugins/axios";


export const checkReceive = (params) => {
  return axios.post("/api/checkReceive/", params)
}

export const checkPick = (params) => {
  return axios.post("/api/checkPick/", params)
}

export const getBorrow = (id) => {
  return axios.get("/api/borrows/" + id + '/');
}

export const getBorrows = (params) => {
  return axios.get("/api/borrows/", {params: params});
}

export const finishBorrow = (id) => {
  return axios.get("/api/borrows/" + id + '/finish/')
};

export const pickBorrow = (id) => {
  return axios.get("/api/borrows/" + id + '/pick/')
};


export const borrow = (id) => {
  return axios.get("/api/samples/" + id + '/borrow/')
}
