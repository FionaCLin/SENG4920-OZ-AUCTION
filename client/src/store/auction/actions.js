// async
export function placeBidding({ commit }, bid) {
  commit("placeBidding", bid);
}

export function createAuction({ commit }, auction, done) {
  commit("createAuction", auction, done);
}
