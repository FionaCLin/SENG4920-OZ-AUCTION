import { axiosInstance } from "../../boot/axios";
import { LocalStorage } from "quasar";

export const signin = (commit, creds) => {
  return axiosInstance
    .post("account/signin", creds)
    .then(response => {
      let user = response;
      // localStorage.setItem("user", JSON.stringify(response.data));
      LocalStorage.set("token", response.token);
      // console.log(JSON.parse(localStorage.getItem("user")));
      commit("user/updateCurrentID", user);
      return response;
    })
    .catch(err => console.log(err.response));
};
