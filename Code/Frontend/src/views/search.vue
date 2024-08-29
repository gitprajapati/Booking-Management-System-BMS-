<template>
  <header>
    <navBar></navBar>
  </header>
  <main>
    <body>
      <h1 class="text-center text-warning">Search</h1>
      <div class="text-center text-warning">
        <div class="search-venue-show">
          <div class="form-check form-check-inline">
            <input
              class="form-check-input"
              type="radio"
              id="inlineRadio122"
              value="Venue"
              v-model="venue.venue_show_selection"
              @change="handleSearchSelection"
            />
            <label class="form-check-label" for="inlineRadio122">
              Search Venue
            </label>
          </div>
          <div class="form-check form-check-inline">
            <input
              class="form-check-input"
              type="radio"
              id="inlineRadio133"
              value="Show"
              v-model="venue.venue_show_selection"
              @change="handleSearchSelection"
            />
            <label class="form-check-label" for="inlineRadio133"
              >Search Show
            </label>
          </div>
        </div>
        <div v-if="venue.venue_show_selection === 'Venue'" class="venue">
          <div class="search-all-venue">
            <section
              class="container my-5 w-50 p-5 text-black bg-secondary bg-gradient border border-primary-subtle rounded-3"
            >
              <form class="d-flex">
                <input
                  class="form-control me-2"
                  id="venuesearch"
                  type="search"
                  placeholder="Search by venue name"
                  aria-label="Search"
                  @input="venueInput"
                  v-model="venue.input_venue_name"
                />

                <button
                  class="btn btn-danger ms-5"
                  type="button"
                  @click="searchVenue()"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    fill="currentColor"
                    class="bi bi-search"
                    viewBox="0 0 16 16"
                  >
                    <path
                      d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"
                    ></path>
                  </svg>
                  Search
                </button>
              </form>
            </section>
            <section
              v-if="
                venue.input_venue_name.length > 0 &&
                venue.searchResults.length > 0
              "
              class="container text-black bg-secondary bg-gradient border border-primary-subtle rounded-3"
            >
              <div>
                <h4 class="text-warning text-center">
                  Here are some results for keyword "{{
                    this.venue.input_venue_name
                  }}"
                </h4>

                <div class="table-responsive">
                  <table class="table table-hover text-center">
                    <thead>
                      <tr>
                        <th>Venue Name</th>
                        <th>Venue City</th>
                        <th>Rating</th>
                        <th>View Shows</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="venue in venue.searchResults" :key="venue.id">
                        <td>{{ venue.name }}</td>
                        <td>{{ venue.city }}</td>
                        <td>{{ venue.avg_venuerate }}</td>
                        <td>
                          <RouterLink :to="`/viewshows/${venue.id}`"
                            >Click Here</RouterLink
                          >
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </section>
            <section
              v-if="venue.success === false"
              class="container my-5 w-50 p-5 text-black bg-secondary bg-gradient border border-primary-subtle rounded-3"
            >
              <div>
                <h4 class="text-danger text-center">No Result Found !!</h4>
              </div>
            </section>
          </div>
        </div>

        <div v-if="venue.venue_show_selection === 'Show'" class="search">
          <div class="search-all-show">
            <div class="form-check form-check-inline">
              <input
                class="form-check-input"
                type="radio"
                id="inlineRadio4"
                value="showname_selected"
                v-model="show.show_search_selected"
                @change="handleSearchChange"
              />
              <label class="form-check-label" for="inlineRadio3"
                >Show name
              </label>
            </div>
            <div class="form-check form-check-inline">
              <input
                class="form-check-input"
                type="radio"
                id="inlineRadio5"
                value="tag_selected"
                v-model="show.show_search_selected"
                @change="handleSearchChange"
              />
              <label class="form-check-label" for="inlineRadio4">Tag </label>
            </div>
          </div>
          <section
            v-if="show.show_search_selected === 'showname_selected'"
            class="container my-5 w-50 p-5 text-black bg-secondary bg-gradient border border-primary-subtle rounded-3"
          >
            <form class="d-flex">
              <input
                class="form-control me-2"
                id="search"
                type="search"
                placeholder="Search by show name"
                aria-label="Search"
                @input="handle_text_Search_Change"
                v-model="show.input_show_name"
              />

              <button
                class="btn btn-danger ms-5"
                type="button"
                @click="searchShows()"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  fill="currentColor"
                  class="bi bi-search"
                  viewBox="0 0 16 16"
                >
                  <path
                    d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"
                  ></path>
                </svg>
                Search
              </button>
            </form>
          </section>
          <section
            v-if="show.show_search_selected === 'tag_selected'"
            class="container my-5 w-50 p-5 text-black bg-secondary bg-gradient border border-primary-subtle rounded-3"
          >
            <form class="d-flex">
              <div class="form-check form-check-inline">
                <input
                  class="form-check-input"
                  type="radio"
                  id="inlineRadio1"
                  value="Action"
                  v-model="show.input_tag"
                  @change="handleTagChange"
                />
                <label class="form-check-label" for="inlineRadio1"
                  >Action
                </label>
              </div>
              <div class="form-check form-check-inline">
                <input
                  class="form-check-input"
                  type="radio"
                  id="inlineRadio4"
                  value="Romance"
                  v-model="show.input_tag"
                  @change="handleTagChange"
                />
                <label class="form-check-label" for="inlineRadio4"
                  >Romance
                </label>
              </div>
              <div class="form-check form-check-inline">
                <input
                  class="form-check-input"
                  type="radio"
                  id="inlineRadio3"
                  value="Drama"
                  v-model="show.input_tag"
                  @change="handleTagChange"
                />
                <label class="form-check-label" for="inlineRadio3"
                  >Drama
                </label>
              </div>
              <div class="form-check form-check-inline">
                <input
                  class="form-check-input"
                  type="radio"
                  id="inlineRadio2"
                  value="Horror"
                  v-model="show.input_tag"
                  @change="handleTagChange"
                />
                <label class="form-check-label" for="inlineRadio2"
                  >Horror
                </label>
              </div>

              <button
                class="btn btn-danger ms-5"
                type="button"
                @click="searchShows()"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  fill="currentColor"
                  class="bi bi-search"
                  viewBox="0 0 16 16"
                >
                  <path
                    d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"
                  ></path>
                </svg>
                Search
              </button>
            </form>
          </section>
          <section
            v-if="
              show.input_show_name.length > 0 && show.searchResults.length > 0
            "
            class="container text-black bg-secondary bg-gradient border border-primary-subtle rounded-3"
          >
            <div>
              <h4 class="text-danger text-center">
                Here are some results for keyword "{{
                  this.show.input_show_name
                }}"
              </h4>

              <div class="table-responsive">
                <table class="table table-hover text-center">
                  <thead>
                    <tr>
                      <th>Show Name</th>
                      <th>Booking Date</th>
                      <th>Tag</th>
                      <th>Rating</th>
                      <th>View Details</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="show in show.searchResults" :key="show.id">
                      <!-- Add ':key="show.id"' to optimize rendering -->
                      <td>{{ show.name }}</td>
                      <td>{{ show.start_date }}-{{ show.out_date }}</td>
                      <td>{{ show.tag }}</td>
                      <td>{{ show.avg_showrate }}</td>
                      <td>
                        <RouterLink :to="`/show/${show.id}`"
                          >View Details</RouterLink
                        >
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </section>
          <section
            v-if="show.input_tag.length > 0 && show.searchResults.length > 0"
            class="container text-black bg-secondary bg-gradient border border-primary-subtle rounded-3"
          >
            <div>
              <h4 class="text-danger text-center">
                Here are some results for tag "{{ this.show.input_tag }}"
              </h4>

              <div class="table-responsive">
                <table class="table table-hover text-center">
                  <thead>
                    <tr>
                      <th>Show Name</th>
                      <th>Booking Date</th>
                      <th>Tag</th>
                      <th>Rating</th>
                      <th>View Details</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="show in show.searchResults" :key="show.id">
                      <td>{{ show.name }}</td>
                      <td>{{ show.start_date }}-{{ show.out_date }}</td>
                      <td>{{ show.tag }}</td>
                      <td>{{ show.avg_showrate }}</td>
                      <td>
                        <RouterLink :to="`/show/${show.id}`"
                          >View Details</RouterLink
                        >
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </section>
          <section
            v-if="show.success === false"
            class="container my-5 w-50 p-5 text-black bg-secondary bg-gradient border border-primary-subtle rounded-3"
          >
            <div>
              <h4 class="text-danger text-center">No Result Found !!</h4>
            </div>
          </section>
        </div>
      </div>
    </body>
  </main>
</template>

<script>
import navBar from "../components/navBar.vue";
import axios from "axios";
export default {
  data() {
    return {
      show: {
        show_search_selected: "",
        input_tag: "",
        input_show_name: "",
        searchResults: {},
        success: "",
      },
      venue: {
        venue_show_selection: "",
        input_venue_name: "",
        searchResults: {},
      },
    };
  },
  methods: {
    venueInput() {
      this.venue.searchResults = {};
    },
    handleSearchSelection() {
      this.show.show_search_selected = "";
      this.show.input_show_name = "";
      this.show.input_tag = "";
      this.show.searchResults = {};
      this.venue.input_venue_name = "";
      this.venue.input_venue_name = "";
      this.venue.searchResults = {};
    },
    handle_text_Search_Change() {
      this.show.searchResults = "";
      this.show.success = "";
    },
    handleSearchChange() {
      if (this.show.show_search_selected === "tag_selected") {
        this.show.input_show_name = ""; 
        this.show.searchResults = "";
      } else if (this.show.show_search_selected === "showname_selected") {
        this.show.input_tag = ""; 
        this.show.searchResults = "";
      }
    },
    handleTagChange() {
      this.show.searchResults = "";
      this.show.success = "";
    },
    async searchVenue() {
      try {
        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        };
        const response = await axios.post(
          "http://127.0.0.1:5000/api/searchvenue",
          {
            venue_name: this.venue.input_venue_name,
          },
          config
        );

        if (response.data.success == true) {
          this.venue.searchResults = response.data.venues_data;

          this.venue.success = response.data.success;
        } 
      } catch (error) {
        this.venue.success = error.response.data.success
        if (error.response && error.response.status === 401) {
          alert("Opps time expired...");
          localStorage.removeItem("token"), this.$router.push("/login");
        }
        if (error.response && error.response.status === 422) {
          this.$router.push("/login");
        } else {
          console.error(error);
          this.show.searchResults = [];
        }
      }
    },

    async searchShows() {
      try {
        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        };
        const response = await axios.post(
          "http://127.0.0.1:5000/api/searchshow",
          {
            show_name: this.show.input_show_name,
            tag: this.show.input_tag,
          },
          config
        );

        if (response.data.success == true) {
          this.show.searchResults = response.data.shows_data;

          this.show.success = response.data.success;
        } 
      } catch (error) {
        this.show.success = error.response.data.success
        if (error.response && error.response.status === 401) {
          alert("Opps time expired...");
          localStorage.removeItem("token"), this.$router.push("/login");
        }
        if (error.response && error.response.status === 422) {
          this.$router.push("/login");
        } else {
          console.error(error);
          this.show.searchResults = [];
        }
      }
    },
  },

  components: {
    navBar,
  },
  mounted() {
    document.title = "Search";
  },
};
</script>
