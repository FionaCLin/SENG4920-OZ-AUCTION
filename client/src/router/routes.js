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
    path: "/myauctions",
    component: () => import("layouts/InnerLayout.vue"),
    children: [
      {
        path: "/",
        name: "myauctions",
        component: () => import("pages/MyAuctions"),
        props: true
      }
    ]
  },
  {
    path: "/mybiddings",
    component: () => import("layouts/InnerLayout.vue"),
    children: [
      {
        path: "/",
        name: "mybiddings",
        component: () => import("pages/MyBiddings"),
        props: true
      }
    ]
  },
  {
    path: "/mywishlist",
    component: () => import("layouts/InnerLayout.vue"),
    children: [
      {
        path: "/",
        name: "mywishlist",
        component: () => import("pages/MyWishlist"),
        props: true
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
        props: true
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
        props: true,
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
