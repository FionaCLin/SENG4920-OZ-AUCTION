import { axiosInstance } from "../../boot/axios";

// async
export function placeBidding({ commit }, bid) {
  commit("placeBidding", bid);
}

export function createAuction({ commit }, auction, done) {
  commit("createAuction", auction, done);
}

export function getAllAuctions({ commit }) {
  console.log("fire getAllAuctions");
  return axiosInstance
    .get(`auctions`)
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
    .catch(err => console.log(err));
}

export async function getAuctionByUserId({ commit, state }, user_id) {
  console.log("getAuctionByUserId", user_id);
  let sellers = [...state.sellers];
  let user = sellers.find(x => x.user_id == user_id);
  if (!user) {
    user = await axiosInstance
      .get(`/account/manage_profile/${user_id}`)
      .then(res => res.data.data);
    sellers.push(user);
  }

  return axiosInstance
    .get(`/auctions/search/filter?user_id=${user_id}`)
    .then(res => {
      let auctions = res.data;
      auctions.map(element => {
        element["user"] = user;
        return element;
      });
      commit("updateMyAuctions", { auctions, sellers });
    })
    .catch(err => console.log(err));
}

export function getMyAutions({ commit, state }, id) {
  let sellers = [...state.sellers];
  return axiosInstance
    .get(`auctions/user/${id}/auctions`)
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
    .catch(err => console.log(err));
}

export function getMyBiddings({ commit, state }, id) {
  let sellers = [...state.sellers];
  return axiosInstance
    .get(`auctions/user/${id}/biddings`)
    .then(async res => {
      console.log(res, id);
      let bids = res.data.data.bids;
      for (let bid of bids) {
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
    .catch(err => console.log(err));
}

export function getMyFavorite({ commit, state }, id) {
  let sellers = [...state.sellers];
  return axiosInstance
    .get(`auctions/user/${id}/favorites`)
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
    .catch(err => console.log(err));
}

export function create({ commit, state }, payload) {
  let sellers = [...state.sellers];

  return axiosInstance
    .post("/auctions", payload)
    .then(res => {
      let newAuction = res.data.data;
      let user = sellers.find(x => x.user_id == payload.seller_id);
      newAuction["user"] = user;
      console.log(newAuction);
      commit("addItem", newAuction);
    })
    .catch(err => {
      console.log(err);
    });
}
