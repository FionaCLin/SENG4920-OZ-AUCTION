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
      // console.log(res);
      commit("updateItem", payload);
      return res;
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
