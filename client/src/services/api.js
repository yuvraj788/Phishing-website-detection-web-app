import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000/api",
});

export const predictUrl = async (url) => {
  const response = await API.post("/predict", { url });
  return response.data;
};