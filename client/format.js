"use strict";

const auctions = require("./auctions.json");
const users = require("./users.json");

let auction_items = [];
auctions.forEach(element => {
  let seller = {};
  ["seller_id", "location", "avatar"].forEach(k => {
    seller[k] = element.seller[k];
  });

  // console.log(element.products);
  let items = [];

  element.products.forEach(e => {
    let item = {};
    [
      "id",
      "seller_name",
      "seller_id",
      "category_id",
      "title",
      "alt_title",
      "updated",
      "created",
      "price",
      "image",
      "status",
      "biddings"
    ].forEach(k => {
      if (e.hasOwnProperty(k)) {
        if (k === "alt_title") {
          item["description"] = e[k];
        } else if (k === "updated") {
          item["end_time"] = e[k];
        } else {
          item[k] = e[k];
        }
      } else {
        item[k] = [];
      }
    });

    items.push(item);
  });
  auction_items.push({
    sellers: seller,
    auction_items: items
  });
});

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
  return methods[Math.floor(Math.random * methods.length)];
};

let users_detail = [];
users.forEach(element => {
  let item = {};
  ["username", "avatar", "favorites"].forEach(k => {
    item[k] = element[k];
  });
  item.userId = mk_string(16);
  item.email = mk_email(item.username);
  item.rating = Math.floor(Math.random() * 5) + 1;
  item.password = mk_string(8);
  item.age = Math.floor(Math.random() * 60) + 1;
  item.paymentMethod = [generatePaymentMethod()];
  users_detail.push(item);
});

console.log(
  auction_items
    .map(i => {
      return JSON.stringify(i);
    })
    .join(", ")
);

// users_detail.forEach(i => {
//   console.log(JSON.stringify(i));
// });
