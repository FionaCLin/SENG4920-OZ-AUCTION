// async
export function placeBidding({ commit }, bid) {
  commit("placeBidding", bid);
}

export function uploadS3({ commit }, file, done) {
  commit("uploadS3", file, done);
}
