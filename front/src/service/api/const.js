import axios from "Plugins/axios"

export const getFertilizerKinds = () => {
  return axios.get('/api/fertilizer_kinds')
};
