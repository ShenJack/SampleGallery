import axios from "Plugins/axios";

export const consume = (params)=>{
  return axios.post('/api/consumes',params)
}

