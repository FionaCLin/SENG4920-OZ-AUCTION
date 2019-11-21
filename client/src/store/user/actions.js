import { axiosInstance } from "../../boot/axios";

export const signin = ({ commit }, creds) => {
  return axiosInstance
    .post("account/signin", creds)
    .then(response => {
      let user = response.data;
      // localStorage.setItem("user", JSON.stringify(response.data));
      localStorage.setItem("token", response.data.token);
      // console.log(JSON.parse(localStorage.getItem("user")));
      commit("updateCurrentID", user);
      return response;
    })
    .catch(err => console.log(err));
};
