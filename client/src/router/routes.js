const menu_list = {
  dashboard: [
    {
      icon: "fiber_new",
      name: "New Auctions",
      href: "newAuctions"
    },
    {
      icon: "gavel",
      name: "My Auctions",
      href: "myAuctions"
    },
    {
      icon: "collections_bookmark",
      name: "My Bids",
      href: "myBids"
    },
    {
      icon: "delete",
      name: "Trash"
    }
  ],
  profile: [
    {
      icon: "person",
      name: "Profile"
    },
    {
      icon: "inbox",
      name: "Inbox"
    },
    {
      icon: "help",
      name: "Help"
    }
  ]
};

const routes = [
  {
    path: "/",
    component: () => import("layouts/MyLayout.vue"),
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
    props: {
      menu: menu_list.dashboard
    },
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
    props: {
      menu: menu_list.profile
    },
    children: [
      {
        path: "/",
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
    props: {
      menu: menu_list.auctions
    },
    children: [
      {
        path: "/",
        component: () => import("pages/CreateAuction")
      }
    ]
  },
  {
    path: "/auctions",
    component: () => import("layouts/InnerLayout.vue"),
    props: {
      menu: menu_list.auctions
    },
    children: [
      {
        path: "/",
        component: () => import("pages/Auctions")
      }
    ]
  },
  {
    path: "/search",
    component: () => import("layouts/InnerLayout.vue"),
    props: {
      menu: menu_list.search
    },
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
