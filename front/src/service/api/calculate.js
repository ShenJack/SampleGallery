import axios from "Plugins/axios";

export const getElementMixtures = (params) => {
  return axios.post('/api/calculate/getElementMixtures', params)
}

export const getFertilizerMixtures = (params) => {
  return axios.post('/api/calculate/getFertilizerMixtures', params)
}

export const getFertilizerPrice = (params) => {
  return axios.post('/api/calculate/getFertilizerPrice', params)
}
