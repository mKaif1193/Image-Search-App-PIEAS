import axios from "axios";

const baseURL = "http://127.0.0.1:8000/";

const AxiosInstance = axios.create({
  baseURL: baseURL,
  headers: {
    Accept: "application/json",
  },
});

AxiosInstance.interceptors.request.use(
  (config) => {
    if (config.data instanceof FormData) {
      delete config.headers["Content-Type"];
    } else {
      config.headers["Content-Type"] = "application/json";
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default AxiosInstance;
