import axios from "Plugins/axios";

export const getFarmtype = (id) => {
return axios.get("api/farmtypes/" + id);
};

export const queryFarmtypeById = (id) => {
return axios.get("api/farmtypes/id_like=" + id);
};

export const getFarmtypes = (params) => {
return axios.get("api/farmtypes", {params: params});
};

export const addFarmtype = (params) => {
return axios.post("api/farmtypes", params);
};

export const editFarmtype = (id, params) => {
return axios.put("api/farmtypes/" + id, params)
};

export const deleteFarmtype = (id) => {
return axios.delete("api/farmtypes/" + id)
};

