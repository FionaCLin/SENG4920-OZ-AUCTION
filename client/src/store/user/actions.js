/*
export function someAction (context) {
}
*/
import { axiosInstance } from "axios";
import { LocalStorage } from "quasar";





export const login = (commit, creds) => {
  axiosInstance.post("/authentication", creds).then(res => {
    console.log(res.data.accessToken);
    LocalStorage.set("token", res.data.accessToken);
  });
};

export function identifyCurrentID(state) {
  state.user_id = JSON.parse(localStorage.getItem('user')).user_id;
}

