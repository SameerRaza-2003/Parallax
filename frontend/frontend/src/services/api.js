import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export const askQuestion = async (question) => {
  const res = await API.post("/query", { question });
  return res.data;
};
