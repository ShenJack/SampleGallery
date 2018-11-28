import axios from "Plugins/axios";

export const getFarmer = (id) => {
return axios.get("/api/farmers/" + id);
};

export const queryFarmerById = (id) => {
return axios.get("/api/farmers?name_like=" + id);
};

export const getFarmers = (params) => {
return axios.get("/api/farmers", {params: params});
};

export const addFarmer = (params) => {
return axios.post("/api/farmers", params);
};

export const editFarmer = (id, params) => {
return axios.put("/api/farmers/" + id, params)
};

export const deleteFarmer = (id) => {
return axios.delete("/api/farmers/" + id)
};

