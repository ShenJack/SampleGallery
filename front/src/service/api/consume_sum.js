import axios from "Plugins/axios";

export const queryConsumeRecordSum = (params) =>{
  return axios.get("/api/consume_record_sums", {params: params})
}
