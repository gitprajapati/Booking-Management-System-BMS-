<template>
  <header v-if="role === 'user'"><navBar></navBar></header>
  <header v-if="role === 'admin'"><adminNav></adminNav></header>
  <div
    class="container marketing my-5 rounded-3"
    style="background-color: rgba(226, 217, 130, 0.986)"
  >
    <div class="row featurette">
      <div class="col-md-7">
        <h3 style="text-transform: uppercase" class="text-danger text-center">
          Show Name: {{ shows_data.name }}
        </h3>
        <p>
          Show Date: {{ shows_data.start_date }} to {{ shows_data.out_date }}
        </p>
        <div class="row">
          <div class="col-md-4">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-tag-fill"
              viewBox="0 0 16 16"
            >
              <path
                d="M2 1a1 1 0 0 0-1 1v4.586a1 1 0 0 0 .293.707l7 7a1 1 0 0 0 1.414 0l4.586-4.586a1 1 0 0 0 0-1.414l-7-7A1 1 0 0 0 6.586 1H2zm4 3.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"
              />
            </svg>
            Tag: {{ shows_data.tag }}
          </div>

          <div class="col-4">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-clock-history"
              viewBox="0 0 16 16"
            >
              <path
                d="M8.515 1.019A7 7 0 0 0 8 1V0a8 8 0 0 1 .589.022l-.074.997zm2.004.45a7.003 7.003 0 0 0-.985-.299l.219-.976c.383.086.76.2 1.126.342l-.36.933zm1.37.71a7.01 7.01 0 0 0-.439-.27l.493-.87a8.025 8.025 0 0 1 .979.654l-.615.789a6.996 6.996 0 0 0-.418-.302zm1.834 1.79a6.99 6.99 0 0 0-.653-.796l.724-.69c.27.285.52.59.747.91l-.818.576zm.744 1.352a7.08 7.08 0 0 0-.214-.468l.893-.45a7.976 7.976 0 0 1 .45 1.088l-.95.313a7.023 7.023 0 0 0-.179-.483zm.53 2.507a6.991 6.991 0 0 0-.1-1.025l.985-.17c.067.386.106.778.116 1.17l-1 .025zm-.131 1.538c.033-.17.06-.339.081-.51l.993.123a7.957 7.957 0 0 1-.23 1.155l-.964-.267c.046-.165.086-.332.12-.501zm-.952 2.379c.184-.29.346-.594.486-.908l.914.405c-.16.36-.345.706-.555 1.038l-.845-.535zm-.964 1.205c.122-.122.239-.248.35-.378l.758.653a8.073 8.073 0 0 1-.401.432l-.707-.707z"
              />
              <path
                d="M8 1a7 7 0 1 0 4.95 11.95l.707.707A8.001 8.001 0 1 1 8 0v1z"
              />
              <path
                d="M7.5 3a.5.5 0 0 1 .5.5v5.21l3.248 1.856a.5.5 0 0 1-.496.868l-3.5-2A.5.5 0 0 1 7 9V3.5a.5.5 0 0 1 .5-.5z"
              />
            </svg>
            Runtime: {{ shows_data.duration }}(HH:MM)
          </div>
        </div>
        <div v-if="shows_data.avg_showrate" class="mt-1">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-star"
            viewBox="0 0 16 16"
          >
            <path
              d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"
            />
          </svg>
          Rating: {{ shows_data.avg_showrate }}
        </div>
        <p>Caption: {{ shows_data.caption }}</p>
        <h2 class="text-center">Venue Details</h2>
        <p>Venue name: {{ venue_data.name }}</p>
        <p v-if="venue_data.avg_venuerate">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-star"
            viewBox="0 0 16 16"
          >
            <path
              d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"
            />
          </svg>
          Rating: {{ venue_data.avg_venuerate }}
        </p>
        <p>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-geo-alt-fill"
            viewBox="0 0 16 16"
          >
            <path
              d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10zm0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6z"
            />
          </svg>
          Venue Address: {{ venue_data.address }}
        </p>
        <p>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-geo-alt-fill"
            viewBox="0 0 16 16"
          >
            <path
              d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10zm0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6z"
            />
          </svg>
          Venue City: {{ venue_data.city }}
        </p>
      </div>
      <div class="col-md-5 my-3">
        <img
          :src="shows_data.image_url"
          class="img-fluid"
          alt="show_image"
          style="object-fit: contain; width: auto; height: 500px"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import navBar from "../components/navBar.vue";
import adminNav from "../components/adminNav.vue";
import myMethods from "@/mixins/myMethods";
export default {
  data() {
    return {
      shows_data: {},
      venue_data: {},
      venue: "",
      shows: "",
      role: "",
    };
  },
  methods: {
    async getShow() {
      try {
        const showId = this.$route.params.id;

        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        };

        const response = await axios.get(
          "http://127.0.0.1:5000/api/showbooking/" + showId,
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
          alert("Opps time expired...");
          localStorage.removeItem("token"), this.$router.push("/login");
        }
        if (error.response && error.response.status === 422) {
          this.$router.push("/login");
        } else {
          console.error(error);
        }
      }
      try {
        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        };
        const id = this.shows_data.venue_id;
        const response = await axios.get(
          "http://127.0.0.1:5000/api/venue/" + id,
          config
        );
        if (response.data.success == true) {
          this.venue = true;

          this.venue_data = response.data.venue_data;
        } else {
          this.venue = false;
        }
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
    this.getShow();
    this.check_role();
    document.title = "Show Details";
  },
  mixins: [myMethods],
  components: {
    navBar,
    adminNav,
  },
};
</script>
