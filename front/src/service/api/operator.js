import axios from "Plugins/axios";

export const getOperator = (id) => {
return axios.get("/api/operators/" + id);
};

export const queryOperatorById = (id) => {
return axios.get("/api/operators?name_like=" + id);
};

export const getOperators = (params) => {
return axios.get("/api/operators", {params: params});
};

export const addOperator = (params) => {
return axios.post("/api/operators", params);
};

export const editOperator = (id, params) => {
return axios.put("/api/operators/" + id, params)
};

export const deleteOperator = (id) => {
return axios.delete("/api/operators/" + id)
};

