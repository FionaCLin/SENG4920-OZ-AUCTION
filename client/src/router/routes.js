const routes = [
  {
    path: "/",
    component: () => import("layouts/LoginLayout.vue"),
    props: {
      logged: false
    },
    children: [
      {
        path: "",
        component: () => import("pages/Login")
      },
      {
        path: "/login",
        component: () => import("pages/Login")
      },
      {
        path: "/register",
        component: () => import("pages/Register")
      }
    ]
  },
  {
    path: "/dashboard",
    component: () => import("layouts/InnerLayout.vue"),
    children: [
      {
        path: "/",
        component: () => import("pages/DashBoard")
      }
    ]
  },
  {
    path: "/profile",
    component: () => import("layouts/InnerLayout.vue"),

    children: [
      {
        path: "",
        component: () => import("pages/Profile")
      },
      {
        path: "/avatar",
        component: () => import("pages/Profile")
      },
      {
        path: "/inbox",
        component: () => import("pages/Profile")
      }
    ]
  },
  {
    path: "/create",
    component: () => import("layouts/InnerLayout.vue"),

    children: [
      {
        path: "/",
        component: () => import("pages/AuctionForm")
      }
    ]
  },
  {
    path: "/auctions",
    component: () => import("layouts/InnerLayout.vue"),

    children: [
      {
        path: "/",
        component: () => import("pages/Auctions")
      },
      {
        path: "/auctions/:id",
        name: "auctionItem",
        component: () => import("pages/Auction"),
        props: {
          pageTitle: "My Auctions"
        }
      },
      {
        path: "/bids/:id",
        name: "biddingItem",
        component: () => import("pages/Bid"),
        props: {
          pageTitle: "My Bids"
        }
      },
      {
        path: "/auctions/edit/:id",
        name: "auctiionItemEdit ",
        component: () => import("pages/AuctionForm"),
        props: {
          edit: true
        }
      }
    ]
  },
  {
    path: "/users",
    component: () => import("layouts/InnerLayout.vue"),

    children: [
      {
        path: "/users/:id",
        name: "userProfile",
        component: () => import("pages/UserProfile")
      }
    ]
  },
  {
    path: "/search",
    component: () => import("layouts/InnerLayout.vue"),

    children: [
      {
        path: "/",
        component: () => import("pages/SearchAuction")
      }
    ]
  },
  {
    path: "/user",
    component: () => import("layouts/InnerLayout.vue"),

    children: [
      {
        path: "/user/myAuctions",
        name: "myAuctions",
        component: () => import("pages/MyAuctions")
      },
      {
        path: "/user/myBiddings",
        name: "myBiddings",
        component: () => import("pages/MyBiddings")
      },
      {
        path: "/user/myWishlist",
        name: "myWishlist",
        component: () => import("pages/MyWishlist")
      }
    ]
  }
];

// Always leave this as last one
if (process.env.MODE !== "ssr") {
  routes.push({
    path: "*",
    component: () => import("pages/Error404.vue")
  });
}

export default routes;
