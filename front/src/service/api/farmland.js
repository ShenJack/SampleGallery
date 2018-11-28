import axios from "Plugins/axios";

export const getFarmland = (id) => {
return axios.get("/api/farmlands/" + id);
};

export const queryFarmlandById = (id) => {
return axios.get("/api/farmlands?name_like=" + id);
};

export const getFarmlands = (params) => {
return axios.get("/api/farmlands", {params: params});
};

export const addFarmland = (params) => {
return axios.post("/api/farmlands", params);
};

export const editFarmland = (id, params) => {
return axios.put("/api/farmlands/" + id, params)
};

export const deleteFarmland = (id) => {
return axios.delete("/api/farmlands/" + id)
};

