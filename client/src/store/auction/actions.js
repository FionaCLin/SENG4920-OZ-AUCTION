import { axiosInstance } from "../../boot/axios";

// async
export function placeBidding({ commit }, bid) {
  commit("placeBidding", bid);
}

export function createAuction({ commit }, auction, done) {
  commit("createAuction", auction, done);
}

export function getAllAuctions({ commit }) {
  axiosInstance
    .get(`auction/search/filter`)
    .then(res => {
      // console.log(res.data);
      commit("updateAuctions", res.data);
    })
    .catch(err => console.log(err));
}

export function getMyAuctions({ commit }, id) {
  console.log("mitty");
  axiosInstance
    .get(`/account/${id}`)
    .then(res => {
      console.log(res.data.auctions);
      commit("updateMyAuctions", res.data.auctions);
    })
    .catch(err => console.log(err));
}

export function getMyBiddings({ commit }, id) {
  console.log("mitty");
  axiosInstance
    .get(`auction/search/filter?user_id=${id}`)
    .then(res => {
      console.log(res.data);
      commit("updateMyBiddings", res.data);
    })
    .catch(err => console.log(err));
}

export function getMyFavorite({ commit }, id) {
  console.log("mitty");
  axiosInstance
    .get(`auction/search/filter?user_id=${id}`)
    .then(res => {
      console.log(res.data);
      commit("updateMyWishList", res.data);
    })
    .catch(err => console.log(err));
}
