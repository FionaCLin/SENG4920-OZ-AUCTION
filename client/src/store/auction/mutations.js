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
