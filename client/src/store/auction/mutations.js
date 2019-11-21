export function placeBidding(state, bid) {
  let auction = state.myBids.find(x => x.id === bid.item_id);
  auction.bidding_info.slice(0, bid);
}
//Sync
export function updateAuctions(state, auctions) {
  state.auctions = auctions;
}

export function updateMyAuctions(state, auctions) {
  state.myAuctions = auctions;
}

export function updateMyBiddings(state, bids) {
  state.myBids = bids;
}

export function updateMyWishList(state, favorites) {
  state.myWishList = favorites;
}

export function addItem(state, newAucton) {
  state.myAuctions.push(newAucton);
}

export function updateItem(state, id, data) {
  let auction = state.myAuctions.find(x => x.id == id);
  for (let k of Object.keys(auction)) {
    console.log(k);
    auction[k] = data[k];
  }
  return state;
}
