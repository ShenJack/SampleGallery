import axios from "Plugins/axios";

export const getFarm_type = (id) => {
return axios.get("/api/farm_types/" + id);
};

export const queryFarm_typeById = (id) => {
return axios.get("/api/farm_types?name_like=" + id);
};

export const getFarm_types = (params) => {
return axios.get("/api/farm_types", {params: params});
};

export const addFarm_type = (params) => {
return axios.post("/api/farm_types", params);
};

export const editFarm_type = (id, params) => {
return axios.put("/api/farm_types/" + id, params)
};

export const deleteFarm_type = (id) => {
return axios.delete("/api/farm_types/" + id)
};

