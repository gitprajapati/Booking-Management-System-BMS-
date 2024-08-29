import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import venueForm from "../views/venueForm.vue";
import showForm from "../views/showForm.vue";
import adminShows from "../views/adminShows.vue";
import search from "../views/search.vue";
import Booking from "../views/Booking.vue";
import userBooking from "../views/userBooking.vue";
import showDetails from "../views/showDetails.vue";
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/login",
      name: "login",
      component: Login,
    },
    {
      path: "/register",
      name: "register",
      component: Register,
    },
    {
      path: "/createvenue",
      name: "createvenue",
      component: venueForm,
    },
    {
      path: "/createshow/:id",
      name: "createshow",
      component: showForm,
    },
    {
      path: "/viewshows/:id",
      name: "viewshows",
      component: adminShows,
    },
    {
      path: "/search",
      name: "search",
      component: search,
    },
    {
      path: "/booking/:id",
      name: "booking",
      component: Booking,
    },
    {
      path: "/mybooking",
      name: "userBooking",
      component: userBooking,
    },
    {
      path: "/show/:id",
      name: "showDetails",
      component: showDetails,
    },
  ],
});

export default router;
