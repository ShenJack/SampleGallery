import axios from "Plugins/axios";

export const getStock = (id) => {
return axios.get("/api/stocks/" + id);
};

export const queryStockById = (id) => {
return axios.get("/api/stocks?name_like=" + id);
};

export const getStocks = (params) => {
return axios.get("/api/stocks", {params: params});
};

export const addStock = (params) => {
return axios.post("/api/stocks", params);
};

export const editStock = (id, params) => {
return axios.put("/api/stocks/" + id, params)
};

export const deleteStock = (id) => {
return axios.delete("/api/stocks/" + id)
};

