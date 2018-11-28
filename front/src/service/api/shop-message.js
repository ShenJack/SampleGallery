import axios from "Plugins/axios";

export const getShopMessages = (params) => {
return axios.get("/api/shop_messages", {params: params});
};

export const addShopMessage = (params) => {
return axios.post("/api/shop_messages", params);
};

export const addBatchShopMessage = (params) => {
return axios.post("/api/shop_messages/batch", params);
};
