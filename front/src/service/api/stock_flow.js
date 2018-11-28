import axios from "Plugins/axios";

export const getStock_flow = (id) => {
return axios.get("/api/stock_flows/" + id);
};

export const queryStock_flowById = (id) => {
return axios.get("/api/stock_flows?name_like=" + id);
};

export const getStock_flows = (params) => {
return axios.get("/api/stock_flows", {params: params});
};

export const addStock_flow = (params) => {
return axios.post("/api/stock_flows", params);
};

export const editStock_flow = (id, params) => {
return axios.put("/api/stock_flows/" + id, params)
};

export const deleteStock_flow = (id) => {
return axios.delete("/api/stock_flows/" + id)
};

