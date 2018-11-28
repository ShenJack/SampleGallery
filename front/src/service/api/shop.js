import axios from "Plugins/axios";

export const getShop = (id) => {
return axios.get("/api/shops/" + id);
};

export const queryShopById = (id) => {
return axios.get("/api/shops?name_like=" + id);
};

export const getShops = (params) => {
return axios.get("/api/shops", {params: params});
};

export const addShop = (params) => {
return axios.post("/api/shops", params);
};

export const editShop = (id, params) => {
return axios.put("/api/shops/" + id, params)
};

export const deleteShop = (id) => {
return axios.delete("/api/shops/" + id)
};

