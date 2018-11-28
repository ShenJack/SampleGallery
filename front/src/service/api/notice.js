import axios from "Plugins/axios";

export const getNotices = (params) => {
return axios.get("/api/notices", {params: params});
};

export const addNotice = (params) => {
return axios.post("/api/notices", params);
};

export const addBatchNotice = (params) => {
return axios.post("/api/notices/batch", params);
};
