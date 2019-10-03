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
    path: "/",
    component: () => import("layouts/InnerLayout.vue"),
    children: [
      {
        path: "/dashboard",
        component: () => import("pages/DashBoard")
      },
      {
        path: "/profile",
        component: () => import("pages/Profile")
      },
      {
        path: "/create",
        component: () => import("pages/CreateAuction")
      },
      {
        path: "/auctions",
        component: () => import("pages/Auctions")
      },
      {
        path: "/search",
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
