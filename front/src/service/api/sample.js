import axios from "Plugins/axios";

export const getSample = (id) => {
return axios.get("/api/samples/" + id +'/');
};

export const querySampleById = (id) => {
return axios.get("/api/samples/?name_like=" + id);
};

export const getSamples = (params) => {
return axios.get("/api/samples/", {params: params});
};

export const addSample = (params) => {
return axios.post("/api/samples/", params);
};

export const editSample = (id, params) => {
return axios.put("/api/samples/" + id +'/', params)
};

export const deleteSample = (id) => {
return axios.delete("/api/samples/" + id +'/')
};

export const passSample = (id) =>{
  return axios.get("/api/samples/" + id + '/passed/')
};

export const rejectSmple = (id) =>{
  return axios.get("/api/samples/" + id + '/reject/')
};

export const getCodeForSample = (id)=>{
  return axios.get("/api/checkinCode/" + id + '/')
}

export const checkReceive = (params)=>{
  return axios.post("/api/checkReceive/",params)
}

export const checkPick = (params)=>{
  return axios.post("/api/checkPick/",params)
}
