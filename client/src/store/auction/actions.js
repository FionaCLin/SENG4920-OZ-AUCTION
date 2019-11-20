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
      let seller_ids = new Set(res.data.result.map(item => item.seller_id));

      let gets = [];
      for (let id of seller_ids) {
        gets.push(
          axiosInstance
            .get(`/account/manage_profile/${id}`)
            .then(res => res.data.data)
        );
      }
      return Promise.all(gets).then(sellers => {
        console.log(sellers, "sellers");
        auctions.map(k => {
          k["user"] = sellers.find(x => {
            return x.user_id === k.seller_id;
          });
        });
        commit("updateAuctions", { auctions, sellers });
      });
    })
    .catch(err => console.log(err.response));
}

export async function getAuctionByUserId({ commit, state }, user_id) {
  // NOT SURE IF WE NEED IT
  console.log("getAuctionByUserId", user_id);
  let sellers = [...state.sellers];
  let user = sellers.find(x => x.user_id == user_id);
  if (!user && user_id) {
    user = await axiosInstance
      .get(`/account/manage_profile/${user_id}`)
      .then(res => res.data.data);
    sellers.push(user);
  }

  return axiosInstance
    .get(`/auction/search/filter?user_id=${user_id}`)
    .then(res => {
      let auctions = res.data;
      auctions.map(element => {
        element["user"] = user;
        return element;
      });
      commit("updateMyAuctions", { auctions, sellers });
    })
    .catch(err => console.log(err.response));
}

export function getMyAutions({ commit, state }, id) {
  let sellers = [...state.sellers];
  return axiosInstance
    .get(`auctions/user/${id}/auction`)
    .then(async res => {
      console.log(res, id);
      let auctions = res.data.data.auctions;
      for (let auction of auctions) {
        let user = sellers.find(x => x.user_id == auction.seller_id);
        if (!user) {
          user = await axiosInstance
            .get(`/account/manage_profile/${auction.seller_id}`)
            .then(res => res.data.data);
          sellers.push(user);
        }
        auction["user"] = user;
      }
      commit("updateMyAuctions", { auctions, sellers });
    })
    .catch(err => console.log(err.response));
}

export function getMyBiddings({ commit, state }, id) {
  let sellers = [...state.sellers];
  return axiosInstance
    .get(`account/get_user_biddings/${id}`)
    .then(async res => {
      console.log(res, id);
      let bids = res.data.data.bids;
      for (let bid of bids) {
        console.log(bid);
        let user = sellers.find(x => x.user_id == bid.seller_id);
        if (!user) {
          user = await axiosInstance
            .get(`/account/manage_profile/${bid.seller_id}`)
            .then(res => res.data.data);
          sellers.push(user);
        }
        bid["user"] = user;
      }
      commit("updateMyBiddings", { bids, sellers });
    })
    .catch(err => console.log(err.response));
}

export function getMyFavorite({ commit, state }, id) {
  let sellers = [...state.sellers];
  return axiosInstance
    .get(`account/get_user_biddings/${id}`)
    .then(async res => {
      console.log(res, id);
      let favorites = res.data.data.favorites;
      for (let fav of favorites) {
        let user = sellers.find(x => x.user_id == fav.seller_id);
        if (!user) {
          user = await axiosInstance
            .get(`/account/manage_profile/${fav.seller_id}`)
            .then(res => res.data.data);
          sellers.push(user);
        }
        fav["user"] = user;
      }
      commit("updateMyWishList", { favorites, sellers });
    })
    .catch(err => console.log(err.response));
}

export function create({ commit, state }, payload) {
  let sellers = [...state.sellers];

  return axiosInstance
    .post("/auction", payload)
    .then(async res => {
      let newAuction = res.data.data;
      let user = sellers.find(x => x.user_id == payload.seller_id);
      if (!user) {
        user = await axiosInstance
          .get(`/account/manage_profile/${payload.seller_id}`)
          .then(res => res.data.data);
        console.log(user, "#####@@#$@!#RFEWRGVEDSFVSDFVSDF");
        sellers.push(user);
      }
      newAuction["user"] = user;
      console.log(newAuction);
      commit("addItem", newAuction);
    })
    .catch(err => {
      console.log(err);
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
