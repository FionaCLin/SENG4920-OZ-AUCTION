import {axiosInstance} from "../../boot/axios";

export const signin = ({commit}, creds) => {
  return new Promise((resolve, reject) => {
    axiosInstance
      .post("account/signin", creds)
      .then(response => {
        let user = response.data;
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("user", JSON.stringify(user));
        commit("updateCurrentID", user);
        resolve(response);
        return response;
      })
      .catch(err => reject(err));
  });
};

export const updateProfile = ({commit, state}, data) => {
  return axiosInstance
    .put(`account/manage_profile/${state.user_id}`, data)
    .then(res => {
      commit("updateUserDetail", data);
      return res;
    })
    .catch(err => {
      return err;
    });
};

export const updateUserDetail = ({commit, state}) => {
  return axiosInstance
    .get(`/account/manage_profile/${state.user_id}`)
    .then(res => {
      commit("updateUserDetail", res.data.data);
      return res;
    });
};
