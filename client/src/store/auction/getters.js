// import { axiosInstance } from "../../boot/axios";

// export function getAuctionByUser(state, id) {
//   axiosInstance
//     .get(`auction/filter?user_id=${id}`)
//     .then(res => {
//       console.log(res);
//       return state.myAuctions;
//     })
//     .catch(err => {
//       console.log(err);
//     });
// }

// export function getAllAuctions(state) {
//   axiosInstance
//     .get(`auction/filter`)
//     .then(res => {
//       console.log(res);
//       state.auctions = res.data.data;
//       // return state.auctions;
//     })
//     .catch(err => {
//       console.log(err);
//     });
// }
// export function getMyBids(state) {
//   return state.myBids;
// }
export function getSeller(state) {
  return seller_id => {
    return state.sellers.find(x => x.user_id === seller_id);
  };
}
