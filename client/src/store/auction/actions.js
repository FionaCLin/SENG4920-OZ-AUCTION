import { axiosInstance } from "../../boot/axios";

// async
export function placeBidding({ commit }, bid) {
  //TODO
  return axiosInstance
    .post("bidding", bid)
    .then(res => {
      bid.bid_id = res.data.data.bid_id;
      bid.created = res.data.data.created;
      commit("placeBidding", bid);
    })
    .catch(err => console.log(err.response));
}

export function getAllAuctions({ commit }) {
  //DONE
  console.log("fire getAllAuctions");
  return axiosInstance
    .get(`auction`)
    .then(res => {
      let auctions = res.data.result;
      console.log(auctions, "#####");
      commit("updateAuctions", auctions);
    })
    .catch(err => console.log(err.response));
}

export function getMyAutions({ commit }, id) {
  return axiosInstance
    .get(`account/get_user_auctions/${id}`)
    .then(async res => {
      commit("updateMyAuctions", res.data.data);
    })
    .catch(err => console.log(err.response));
}

export function getMyBiddings({ commit }, id) {
  return axiosInstance
    .get(`account/get_user_biddings/${id}`)
    .then(async res => {
      commit("updateMyBiddings", res.data.data);
    })
    .catch(err => console.log(err.response));
}

export function getMyFavorite({ commit }, id) {
  return axiosInstance
    .get(`account/get_user_favorites/${id}`)
    .then(async res => {
      commit("updateMyWishList", res.data.data);
    })
    .catch(err => console.log(err.response));
}

export function create({ commit }, payload) {
  return axiosInstance
    .post("/auction", payload)
    .then(async res => {
      let newAuction = res.data.data;
      // let user = await axiosInstance
      //   .get(`/account/manage_profile/${payload.seller_id}`)
      //   .then(res => res.data.data);
      // console.log(user, "#####@@#$@!#RFEWRGVEDSFVSDFVSDF");
      // newAuction["user"] = user;
      // console.log(newAuction);
      commit("addItem", newAuction);
    })
    .catch(err => {
      console.log(err.response);
      return err.response;
    });
}

export function update({ commit }, id, payload) {
  return axiosInstance
    .put(`auction/${id}`, payload)
    .then(async res => {
      let newAuction = res.data.data;
      console.log(newAuction);
      commit("updateItem", payload);
      return res.data;
    })
    .catch(err => {
      console.log(err.response);
      return err.response;
    });
}

export function deleteAuction({ commit, state }, auction_id) {
  let auctions = [...state.myAuctions];

  let sellers = null;
  return axiosInstance
    .delete(`/auction/${auction_id}`)
    .then(res => {
      console.log(auctions, auction_id);
      let index = auctions.findIndex(i => i.id === auction_id);
      auctions.splice(index, 1);
      console.log(auctions, index);
      console.log(res);

      commit("updateMyAuctions", { auctions, sellers });
    })
    .catch(err => console.log(err.response));
}
