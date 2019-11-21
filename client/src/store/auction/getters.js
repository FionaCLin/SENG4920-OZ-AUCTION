export function getSeller(state) {
  return seller_id => {
    return state.sellers.find(x => x.user_id === seller_id);
  };
}

export function getAuction(state) {
  return auction_id => {
    return state.auctions.find(x => x.id === auction_id);
  };
}
