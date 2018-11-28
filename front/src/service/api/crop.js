import axios from "Plugins/axios";

export const getCrop = (id) => {
return axios.get("/api/crops/" + id);
};

export const queryCropById = (id) => {
return axios.get("/api/crops?name_like=" + id);
};

export const getCrops = (params) => {
return axios.get("/api/crops", {params: params});
};

export const addCrop = (params) => {
return axios.post("/api/crops", params);
};

export const editCrop = (id, params) => {
return axios.put("/api/crops/" + id, params)
};

export const deleteCrop = (id) => {
return axios.delete("/api/crops/" + id)
};

