"use strict";
var moment = require("moment");
const auctions = require("./auctions.json");

let mk_email = name =>
  name.length % 2 ? `${name}@gmail.com` : `${name}@yahoo.com`;
let mk_string = length => {
  var result = "";
  var characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  var charactersLength = characters.length;
  for (var i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
};

let generatePaymentMethod = () => {
  let methods = ["Visa", "Master", "WeChat", "PayPal", "AliPay"];
  return methods.slice(Math.floor(Math.random() * methods.length));
};

let generatePhone = () => {
  var phone = 437462648;
  phone++;
  return "0" + phone;
};

function randomDate(start, end) {
  return new Date(
    start.getTime() + Math.random() * (end.getTime() - start.getTime())
  );
}

var biddings = [
  new Set([]),
  new Set([]),
  new Set([]),
  new Set([]),
  new Set([]),
  new Set([])
];

let users_detail = [];
let mkup_biddings = (seller_id, auction, i) => {
  // pick a user
  let user_id = Math.floor(Math.random() * 5);
  if (user_id === seller_id) {
    user_id++;
  }

  auction.bidding_info.push({
    user_id: user_id,
    item_id: auction.id,
    proposal_price: auction.price + i * Math.random(),
    created: moment(auction["created"], "YYYY-MM-DD h:mm:ss")
      .add(auction.bidding_info.length, "hour")
      .format("YYYY-MM-DD h:mm:ss")
  });
  biddings[user_id].add(auction.id);
};

let auction_items = [];
let index = 0;
let uIndex = 0;
auctions.forEach(element => {
  let seller = {
    user_id: uIndex,
    email: mk_email(element.seller.shop_name),
    payment_method: generatePaymentMethod(),
    password: mk_string(10),
    first_name: "",
    last_name: "",
    phone_number: generatePhone(),
    dob: randomDate(
      new Date(2012, 0, 1),
      new Date(
        moment()
          .subtract(18, "year")
          .format("YYYY-MM-DD h:mm:ss")
      )
    ),
    avatar: element.seller.avatar,
    location: element.seller.location,
    rating: Math.floor(Math.random() * 5 + 1),
    token: mk_string(28),
    favorites: [],
    auctions: [],
    bids: []
  };
  users_detail.push(seller);
  uIndex++;

  element.products.forEach(e => {
    let a = moment(e["add_date"]);
    seller.first_name = e["seller_name"];
    seller.last_name = e["seller_name"];
    let item = {
      id: index,
      seller_name: seller.first_name,
      seller_id: seller.user_id,
      category: "Crafts",
      title: e["title"],
      description: e["alt_title"],
      created: a.format("YYYY-MM-DD h:mm:ss"),
      updated: a.add(1, "day").format("YYYY-MM-DD h:mm:ss"),
      end_time: a.add(1, "week").format("YYYY-MM-DD h:mm:ss"),
      location: seller.location,
      price: e["price"],
      image: [e["image"]],
      status: "bidding",
      bidding_info: []
    };
    for (let i = 1, ii = Math.random() * 50 + 1; i < ii; i++) {
      mkup_biddings(seller.user_id, item, i);
    }
    index++;
    seller.auctions.push(item);
    auction_items.push(item);
  });
});

for (let i in biddings) {
  for (const v of biddings[i]) {
    users_detail[i].bids.push(auction_items[v]);
  }
  let len = biddings[i].size;
  users_detail[i].favorites = users_detail[i].bids.splice(Math.floor(len / 2));
}

console.log(
  JSON.stringify(
    {
      auctions: auction_items,
      users: users_detail
    },
    null,
    2
  )
);
