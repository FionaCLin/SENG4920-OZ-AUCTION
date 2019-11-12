export function getMyAuction(state) {
  return state.myAuctions;
}
export function getMyBids(state) {
  return state.myBids;
}
export function getMyWishList(state) {
  return state.myWishList;
}

export function getAuction(state, id) {
  for (let i of state.auctions) {
    let auction = i.auction_items.find(x => x.id === id);
    console.log(i, auction);
    if (auction) {
      return auction;
    }
  }
}
