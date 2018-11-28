import axios from "Plugins/axios";

export const setCardId = (farmer_id, card_id) => {
  return axios.post('/api/farmer_numbers', {
    id_number: card_id,
    farmer_id: farmer_id
  })
}

export const getFarmerByCard = (card_id) => {
  return axios.get('/api/farmer_numbers/' + card_id);
}

export const getCards = (farmer_id) => {
  return axios.get('/api/farmer_numbers?farmer_id=' + farmer_id);
}
