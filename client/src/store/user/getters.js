import { axiosInstance } from "../../boot/axios";

export function getUser(id) {
  axiosInstance
    .get(`account/manage_profile/${id}`)
    .then(res => {
      console.log(res);
    })
    .catch(err => {
      console.log(err);
    });
}
