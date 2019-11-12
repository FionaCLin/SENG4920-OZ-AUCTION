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
import aws from "aws-sdk";
import secret from "../../../src/awsconfig.json";

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

export function uploadS3(file, done) {
  console.log(file);
  const s3 = new aws.S3(secret);

  let data = file[0];
  s3.upload(
    {
      Bucket: "seng4920album",
      Key: `${this.title}-${Date.now()}-${data.name}`,
      Body: data,
      ACL: "public-read"
    },
    (err, res) => {
      console.log(err, res);
      done(err, res);
    }
  );
}
//Sync
