<template>
  <body>
    <header v-if="role === 'admin'"><adminNav></adminNav></header>

    <main v-if="role === 'admin'">
      <admin_has_venue v-if="venues == true"></admin_has_venue>
      <admin_no_venue v-else></admin_no_venue>
    </main>
    <header v-if="role === 'user'"><navBar></navBar></header>
    <main v-if="role === 'user'" class="mb-5">
      <div class="home container">
        <h1 class="my-4 text-center text-warning">Welcome to BMS</h1>
        <div v-if="shows_data.length > 0" class="row">
          <div class="col-md-6" v-for="show in shows_data">
            <div class="card flex-md-row mb-4 box-shadow h-md-250">
              <div class="card-body d-flex flex-column align-items-start">
                <h5 class="text-center">Venue: {{ show.venue_name }}</h5>
                <div class="mb-1 text-muted">
                  Date : {{ show.start_date }} to
                  {{ show.out_date.substring(2, 16) }}
                </div>
                <strong class="d-inline-block mb-2 text-primary">{{
                  show.name
                }}</strong>
                <small> Tag: {{ show.tag }}</small>

                <label for="caption">Caption:</label>
                <p
                  v-if="show.caption.length < 100"
                  class="card-text mb-auto"
                  id="caption"
                >
                  {{ show.caption }}
                </p>
                <p v-else class="card-text mb-auto" id="caption">
                  {{ show.caption.substring(0, 100) + "..." }}
                </p>
                <RouterLink :to="`/show/${show.id}`"
                  >Continue reading</RouterLink
                >
              </div>
              <img
                class="card-img-right flex-auto d-none d-md-block"
                data-src="holder.js/200x250?theme=thumb"
                alt="Thumbnail [200x250]"
                style="width: 200px; height: 250px"
                :src="show.show_image_url"
                data-holder-rendered="true"
              />
            </div>
            <RouterLink
              type="button"
              class="btn btn-primary"
              :to="`/booking/${show.id}`"
            >
              Book Now
            </RouterLink>
          </div>
        </div>
        <div v-else class="alert alert-info">
          No shows available at the moment.
        </div>
      </div>
    </main>
  </body>
</template>

<script>
import admin_no_venue from "../components/admin_no_venue.vue";
import admin_has_venue from "../components/admin_has_venue.vue";
import adminNav from "../components/adminNav.vue";
import myMethods from "@/mixins/myMethods";
import navBar from "../components/navBar.vue";

import axios from "axios";
export default {
  data() {
    return {
      shows_data: "",
      shows: "",
      venues: null,
      venue_data: {},
      role: "",
    };
  },
  methods: {
    async get_all_shows() {
      try {
        const venueId = this.$route.params.id;
        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        };

        const response = await axios.get(
          "http://127.0.0.1:5000/api/allshows",
          config
        );
        if (response.data.shows == true) {
          this.shows = true;

          this.shows_data = response.data.shows_data;
        } else {
          this.shows = false;
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          localStorage.removeItem("token"), this.$router.push("/login");
        }
        if (error.response && error.response.status === 422) {
          this.$router.push("/login");
        } else {
          console.error(error);
        }
      }
    },
  },
  components: {
    adminNav,
    admin_no_venue,
    admin_has_venue,
    navBar,
  },
  mixins: [myMethods],
  mounted() {
    this.check_venue();
    this.check_role();
    this.get_all_shows();
    document.title = "Home Page";
  },
};
</script>
