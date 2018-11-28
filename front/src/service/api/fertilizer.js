import axios from "Plugins/axios";

export const getFertilizer = (id) => {
return axios.get("/api/fertilizers/" + id);
};

export const queryFertilizerById = (id) => {
return axios.get("/api/fertilizers?name_like=" + id);
};

export const getFertilizers = (params) => {
return axios.get("/api/fertilizers", {params: params});
};

export const addFertilizer = (params) => {
return axios.post("/api/fertilizers", params);
};

export const editFertilizer = (id, params) => {
return axios.put("/api/fertilizers/" + id, params)
};

export const deleteFertilizer = (id) => {
return axios.delete("/api/fertilizers/" + id)
};

