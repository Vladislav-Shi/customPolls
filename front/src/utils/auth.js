import store from "../store";
import axios from "axios";

export let authAxios = axios.create({
  baseURL: `http://${process.env.VUE_APP_API_HOST}:${process.env.VUE_APP_API_PORT}/`,
  headers: {
    Authorization: `Bearer ${store.state.auth.access_token}`,
  },
});

authAxios.interceptors.request.use(
  (config) => {
    config.headers["Authorization"] = `Bearer ${store.state.auth.access_token}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Перехватчик, который будет проверять каждый ответ сервера
authAxios.interceptors.response.use(
  (response) => {
    // Если ответ успешный, просто возвращаем его
    return response;
  },
  async (error) => {
    let originalRequest = error.config;
    if (
      (error.response.status === 401 || error.response.status == 403) &&
      !originalRequest._retry
    ) {
      // Если получили ответ с кодом 401 или 403 и это не повторный запрос
      originalRequest._retry = true;
      let dispatchResponse = await store
        .dispatch("refresh")
        .then(() => {
          return null;
        })
        .catch((err) => {
          return err;
        }); // Обновляем токен
      // Обновляем заголовки запроса с новым токеном
      if (dispatchResponse === null) {
        originalRequest.headers[
          "Authorization"
        ] = `Bearer ${store.state.auth.access_token}`;
        return authAxios(originalRequest); // Повторяем исходный запрос
      }
    }
    return Promise.reject(error).catch((err) => {
      return err.response;
    });
  }
);
