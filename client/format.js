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

let users_detail = [];

let auction_items = [];
let index = 0;
let uIndex = 0;
auctions.forEach(element => {
  let seller = {
    user_id: uIndex,
    email: mk_email(element.seller.shop_name),
    paymentMethod: generatePaymentMethod(),
    password: mk_string(10),
    first_name: "",
    last_name: "",
    phone_number: generatePhone(),
    DOB: randomDate(
      new Date(2012, 0, 1),
      new Date(
        moment()
          .subtract(18, "year")
          .format()
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
      created: a.format(),
      updated: a.add(1, "day").format(),
      end_time: a.add(1, "week").format(),
      location: seller.location,
      price: e["price"],
      image: [e["image"]],
      status: "bidding",
      bidding_info: []
    };
    index++;
    auction_items.push(item);
  });
});

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
