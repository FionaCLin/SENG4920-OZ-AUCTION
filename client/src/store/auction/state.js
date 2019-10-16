import auction_items from "./auctionItem.json";

export default {
  myAuctions: auction_items[0],
  auctions: auction_items.slice(1)
};
