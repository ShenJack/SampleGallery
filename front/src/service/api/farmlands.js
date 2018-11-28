import axios from "Plugins/axios";

export const getAllFarmlands = ()=>{
    return axios.get('/api/farmers')
}

export const getFarmland = (id)=>{
    return axios.get('/api/farmers/'+id)
}