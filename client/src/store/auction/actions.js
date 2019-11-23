import { axiosInstance } from "../../boot/axios";

// async
export function placeBidding({ commit }, { bid, buyer }) {
  //TODO
  return axiosInstance
    .post("bidding", bid)
    .then(res => {
      bid.bid_id = res.data.data.bid_id;
      bid.created = res.data.data.created;
      bid.buyer = buyer;
      commit("placeBidding", bid);
      return res;
    })
    .catch(err => err.response);
}

export function getAllAuctions({ commit }) {
  //DONE
  console.log("fire getAllAuctions");
  return axiosInstance
    .get(`auction`)
    .then(res => {
      let auctions = res.data.result;
      console.log(auctions, "###1##");
      commit("updateAuctions", auctions);
      return res;
    })
    .catch(err => console.log(err.response));
}

export function getMyAutions({ commit }, id) {
  return axiosInstance
    .get(`account/get_user_auctions/${id}`)
    .then(res => {
      let auctions = res.data.data;
      console.log(auctions, "####2#");
      commit("updateMyAuctions", res.data.data);
      return res;
    })
    .catch(err => console.log(err.response));
}

export function getMyBiddings({ commit }, id) {
  return axiosInstance
    .get(`account/get_user_biddings/${id}`)
    .then(res => {
      let auctions = res.data;
      console.log(auctions, "##3###");
      commit("updateMyBiddings", res.data.data);
      return res;
    })
    .catch(err => console.log(err.response));
}

export function getMyFavorite({ commit }, id) {
  return axiosInstance
    .get(`account/get_user_favorites/${id}`)
    .then(res => {
      let auctions = res.data.data;
      console.log(auctions, "###4##");
      commit("updateMyWishList", res.data.data);
      return res;
    })
    .catch(err => console.log(err.response));
}

export function create({ commit }, payload) {
  return axiosInstance
    .post("/auction", payload)
    .then(res => {
      let newAuction = res.data.data;
      commit("addItem", newAuction);
      return res;
    })
    .catch(err => {
      console.log(err.response);
      return err;
    });
}

export function update({ commit }, { id, payload }) {
  console.log(payload, id);
  return axiosInstance
    .put(`/auction/${id}`, payload)
    .then(res => {
      commit("updateItem", { id, payload });
      return res;
    })
    .catch(err => {
      console.log(err.response);
      return err.response;
    });
}

export function deleteAuction({ commit }, auction_id) {
  return axiosInstance.delete(`/auction/${auction_id}`).then(res => {
    commit("removeMyAuction", auction_id);
    return res;
  });
}
