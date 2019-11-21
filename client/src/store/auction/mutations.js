export function placeBidding(state, bid) {
  let auction = state.myBids.find(x => x.id === bid.item_id);
  auction.bidding_info.slice(0, bid);
  console.log("mu", state, bid, auction.bidding_info.length);
}
//Sync
export function updateAuctions(state, { auctions, sellers }) {
  console.log(state, auctions, sellers, "updateAuctions");
  state.sellers = sellers;
  state.auctions = auctions;
}

export function updateMyAuctions(state, { auctions, sellers }) {
  console.log(state, auctions, "updateMyAuctions");
  if (sellers) {
    state.sellers = sellers;
  }

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
