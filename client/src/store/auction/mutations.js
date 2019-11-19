// import { stat } from "fs";

// import { axiosInstance } from "boot/axios";

// export function getMyAuction(state) {
//   axiosInstance.get()
//   return state.myAuctions;
// }
// export function getMyBids(state) {
//   return state.myBids;
// }
// export function getMyWishList(state) {
//   return state.myWishList;
// }
export function placeBidding(state, bid) {
  let auction = null;
  for (let i of state.auctions) {
    let item = i.auction_items.find(x => x.id === bid.auction_id);
    console.log(i, item);
    if (item) {
      auction = item;
      break;
    }
  }
  auction.biddings.push({
    user_id: bid.user_id,
    price: bid.price,
    item_id: bid.auction_id,
    created: new Date()
  });
  console.log("mu", state, bid, auction);
}
//Sync
export function updateAuctions(state, { auctions, sellers }) {
  console.log(state, auctions, sellers, "updateAuctions");
  state.sellers = sellers;
  state.auctions = auctions;
}

export function updateMyAuctions(state, { auctions, sellers }) {
  console.log(state, auctions, "updateMyAuctions");
  state.sellers = sellers;

  state.myAuctions = auctions;
}

export function updateMyBiddings(state, { bids, sellers }) {
  console.log(state, bids, "updateMyBiddings");
  state.sellers = sellers;
  state.myBids = bids;
}

export function updateMyWishList(state, { favorites, sellers }) {
  console.log(state, favorites, "updateMyWishList");
  state.sellers = sellers;
  state.myWishList = favorites;
}

export function addItem(state, newAucton) {
  state.myAuctions.push(newAucton);
}
