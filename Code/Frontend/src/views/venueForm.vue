<template>
  <body>
    <main>
      <adminNav></adminNav>
      <h1 class="text-center text-warning">Create venue</h1>
      <div
        class="container col-lg-5 bg-secondary bg-gradient border border-primary-subtle rounded-3"
      >
        <div class="row justify-content-center">
          <div class="">
            <form class="text-black">
              <div class="form-group">
                <label for="name">Name:</label>
                <input
                  v-model="venue.name"
                  type="text"
                  class="form-control"
                  id="name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="address">Address:</label>
                <input
                  v-model="venue.address"
                  type="text"
                  class="form-control"
                  id="address"
                  required
                />
              </div>
              <div class="form-group">
                <label for="city">City:</label>
                <input
                  v-model="venue.city"
                  type="text"
                  class="form-control"
                  id="city"
                  required
                />
              </div>
              <div class="form-group">
                <label for="state">State:</label>
                <input
                  v-model="venue.state"
                  type="text"
                  class="form-control"
                  id="state"
                  required
                />
              </div>

              <button
                type="button"
                class="btn btn-primary form-control mt-5 mb-3"
                v-on:click="createVenue()"
              >
                Create Venue
              </button>
            </form>
          </div>
        </div>
      </div>
    </main>
  </body>
</template>

<script>
import adminNav from "../components/adminNav.vue";
import axios from "axios";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
export default {
  data() {
    return {
      venue: {
        name: "",
        address: "",
        city: "",
        state: "",
        owner_id: "",
      },
    };
  },
  methods: {
    async createVenue() {
      try {
        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        };
        await axios.post(
          "http://127.0.0.1:5000/api/venues",
          {
            name: this.venue.name,
            address: this.venue.address,
            city: this.venue.city,
            state: this.venue.state,
          },
          config
        );
        this.venue.name = "";
        this.venue.address = "";
        this.venue.city = "";
        this.venue.state = "";
        toast.success("Venue Added Sucessfully !", {
          autoClose: 1000,
        });
        await new Promise((resolve) => setTimeout(resolve, 3000));
        this.$router.push("/");
      } catch (error) {
        if (error.response && error.response.status === 401) {
          alert("Opps time expired...");
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
  mounted() {
    document.title = "Venue Form";
  },
  components: {
    adminNav,
  },
};
</script>
