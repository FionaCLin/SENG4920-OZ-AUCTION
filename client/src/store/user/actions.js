import { axiosInstance } from "../../boot/axios";

export const signin = ({ commit }, creds) => {
  return new Promise((resolve, reject) => {
    axiosInstance
      .post("account/signin", creds)
      .then(response => {
        let user = response.data;
        localStorage.setItem("token", response.data.token);
        commit("updateCurrentID", user);
        resolve();
        return response;
      })
      .catch(err => reject(err));
  });
};

