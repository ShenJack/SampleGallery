import axios from "Plugins/axios";

export const getConsume_record = (id) => {
return axios.get("/api/consume_records/" + id);
};

export const queryConsume_recordById = (id) => {
return axios.get("/api/consume_records?name_like=" + id);
};

export const getConsume_records = (params) => {
return axios.get("/api/consume_records", {params: params});
};

export const addConsume_record = (params) => {
return axios.post("/api/consume_records", params);
};

export const editConsume_record = (id, params) => {
return axios.put("/api/consume_records/" + id, params)
};

export const deleteConsume_record = (id) => {
return axios.delete("/api/consume_records/" + id)
};

