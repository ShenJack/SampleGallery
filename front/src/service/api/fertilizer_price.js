import axios from "Plugins/axios";

export const getFertilizer_price = (id) => {
return axios.get("/api/fertilizer_prices/" + id);
};

export const queryFertilizer_priceById = (id) => {
return axios.get("/api/fertilizer_prices?name_like=" + id);
};

export const getFertilizer_prices = (params) => {
return axios.get("/api/fertilizer_prices", {params: params});
};

export const addFertilizer_price = (params) => {
return axios.post("/api/fertilizer_prices", params);
};

export const editFertilizer_price = (id, params) => {
return axios.put("/api/fertilizer_prices/" + id, params)
};

export const deleteFertilizer_price = (id) => {
return axios.delete("/api/fertilizer_prices/" + id)
};

