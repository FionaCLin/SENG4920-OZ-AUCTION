export function placeBidding(state, bid) {
  let i = state.myBids.findIndex(x => x.id === bid.item_id);
  state.myBids[i].bidding_info.splice(0, 0, bid);
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

export function updateItem(state, { id, payload }) {
  let aIndex = state.myAuctions.findIndex(x => x.id == id);
  let auction = state.myAuctions[aIndex];
  for (let k of Object.keys(payload)) {
    auction[k] = payload[k];
  }
  return state;
}
export function removeMyAuction(state, id) {
  let aIndex = state.myAuctions.findIndex(x => x.id == id);
  state.myAuctions.splice(aIndex, 1);
}
export function addWishList(state, id, auction) {
  console.log(id, auction);
  id = Number(id);
  if (auction) {
    state.myWishList.push(a);
    return;
  }
  let a = state.myBids.find(x => x.id == id);
  if (!a) {
    a = state.myWishList.find(x => x.id == id);
  }
  state.myWishList.push(a);
}
export function removeWishList(state, id) {
  let aIndex = state.myWishList.findIndex(x => x.id == id);
  state.myWishList.splice(aIndex, 1);
}

export function updateMyAuctionStatus(state, { id, status }) {
  let aIndex = state.myAuctions.findIndex(x => x.id == id);
  state.myAuctions[aIndex].status = status;
}
