<template>
  <adminNav></adminNav>
  <h1 class="text-center text-warning">-: Shows :-</h1>
  <div class="container" v-if="shows == true">
    <div class="row mb-2">
      <div class="col-md-6" v-for="show in shows_data">
        <div class="card flex-md-row mb-4 box-shadow h-md-250">
          <div class="card-body d-flex flex-column align-items-start">
            <div class="mb-1 text-muted">Date : {{ show.start_date }}</div>
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
            <RouterLink :to="`/show/${show.id}`">Continue reading</RouterLink>
          </div>
          <img
            alt="Show_image"
            style="width: 200px; height: 250px "
            :src="show.show_image_url"
          />
        </div>
        <div
          v-if="role === 'admin'"
          class="btn-group"
          role="group"
          aria-label="Basic mixed styles example"
        >
          <button
            type="button"
            class="btn btn-warning"
            data-bs-toggle="modal"
            :data-bs-target="'#staticBackdrop-' + show.id"
          >
            Edit
          </button>
          <!-- Modal -->
          <div
            class="modal fade"
            :id="'staticBackdrop-' + show.id"
            data-bs-backdrop="static"
            data-bs-keyboard="false"
            tabindex="-1"
            aria-labelledby="staticBackdropLabel"
            aria-hidden="true"
          >
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h1 class="modal-title fs-5" id="staticBackdropLabel">
                    Edit Show
                  </h1>
                  <button
                    type="button"
                    class="btn-close"
                    data-bs-dismiss="modal"
                    aria-label="Close"
                  ></button>
                </div>
                <div class="container">
                  <div class="row justify-content-center">
                    <div class="col-lg-12">
                      <div class="form-group">
                        <label for="name">Name:</label>
                        <input
                          :placeholder="show.name"
                          v-model="editedShowdata.name"
                          type="text"
                          class="form-control"
                          id="name"
                        />
                      </div>
                      <div class="form-group">
                        <label for="caption">Caption:</label>
                        <textarea
                          v-model="editedShowdata.caption"
                          :placeholder="show.caption"
                          type="text"
                          class="form-control"
                          id="caption"
                        ></textarea>
                      </div>
                      <div class="form-group">
                        <label for="capacity">Capacity:</label>
                        <input
                          v-model="editedShowdata.capacity"
                          :placeholder="show.capacity"
                          type="number"
                          class="form-control"
                          id="capacity"
                          required
                        />
                      </div>
                      <div class="form-group">
                        <label for="price">Price:</label>
                        <input
                          v-model="editedShowdata.price"
                          :placeholder="show.price"
                          type="number"
                          class="form-control"
                          id="price"
                        />
                      </div>
                      <div class="form-group">
                        <label for="radio">Genre:</label>
                        <div class="form-group" id="radio">
                          <div class="form-row">
                            <div class="col">
                              <input
                                type="radio"
                                id="Action"
                                value="Action"
                                v-model="editedShowdata.tag"
                                :placeholder="show.tag"
                              /><label for="Action">Action</label>

                              <input
                                type="radio"
                                id="Horror"
                                value="Horror"
                                v-model="editedShowdata.tag"
                                :placeholder="show.tag"
                              /><label for="Horror">Horror</label>

                              <input
                                type="radio"
                                id="Drama"
                                value="Drama"
                                v-model="editedShowdata.tag"
                                :placeholder="show.tag"
                              /><label for="Drama">Drama</label>

                              <input
                                type="radio"
                                id="Romance"
                                value="Romance"
                                v-model="editedShowdata.tag"
                                :placeholder="show.tag"
                              /><label for="Romance">Romance</label>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="form-group">
                        <label for="duration">Duration:</label>
                        <input
                          type="text"
                          class="form-control"
                          id="duration"
                          name="duration"
                          v-model="editedShowdata.duration"
                          :placeholder="show.duration"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <br />
                <div class="modal-footer">
                  <button
                    type="button"
                    class="btn btn-secondary"
                    data-bs-dismiss="modal"
                  >
                    Close
                  </button>
                  <button
                    type="button"
                    class="btn btn-primary"
                    @click="editShow(show.id)"
                    data-bs-dismiss="modal"
                  >
                    Edit Show
                  </button>
                </div>
              </div>
            </div>
          </div>
          <button
            type="button"
            class="btn btn-danger"
            data-bs-toggle="modal"
            :data-bs-target="'#staticBackdrop2-' + show.id"
          >
            Delete
          </button>
          <!-- Modal -->
          <div
            class="modal fade"
            :id="'staticBackdrop2-' + show.id"
            data-bs-backdrop="static"
            data-bs-keyboard="false"
            tabindex="-1"
            aria-labelledby="staticBackdropLabel"
            aria-hidden="true"
          >
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h1 class="modal-title fs-5" id="staticBackdropLabel">
                    Delete Show
                  </h1>
                  <button
                    type="button"
                    class="btn-close"
                    data-bs-dismiss="modal"
                    aria-label="Close"
                  ></button>
                </div>
                <div class="modal-body">Are you sure to delete.</div>
                <div class="modal-footer">
                  <button
                    type="button"
                    class="btn btn-secondary"
                    data-bs-dismiss="modal"
                  >
                    Close
                  </button>
                  <button
                    type="button"
                    class="btn btn-danger"
                    @click="deleteShow(show.id)"
                    data-bs-dismiss="modal"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <h1 class="text-center text-warning">No Shows</h1>
  </div>
</template>

<script>
import adminNav from "../components/adminNav.vue";
import myMethods from "@/mixins/myMethods";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import axios from "axios";
export default {
  data() {
    return {
      shows_data: {},
      shows: "",
      role: "",

      editedShowdata: {
        name: "",
        tag: "",
        duration: "",
        price: "",
        caption: "",
        capacity: "",
      },
      editedShowId: null,
    };
  },
  methods: {
    async editShow(showId) {
      let formData = new FormData();
      formData.append("data", JSON.stringify(this.editedShowdata));
      try {
        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        };

        await axios.put(
          "http://127.0.0.1:5000/api/shows/" + showId,

          formData,

          config
        );

        const editedShow = this.shows_data.find((show) => show.id === showId);
        if (editedShow) {
          if (this.editedShowdata.name) {
            editedShow.name = this.editedShowdata.name;
          }
          if (this.editedShowdata.duration) {
            editedShow.duration = this.editedShowdata.duration;
          }
          if (this.editedShowdata.tag) {
            editedShow.tag = this.editedShowdata.tag;
          }
          if (this.editedShowdata.caption) {
            editedShow.caption = this.editedShowdata.caption;
          }
          if (this.editedShowdata.price) {
            editedShow.price = this.editedShowdata.price;
          }
          if (this.editedShowdata.capacity) {
            editedShow.capacity = this.editedShowdata.capacity;
          }
        }

        this.editedShowdata = {
          name: "",
          tag: "",
          price: "",
          duration: "",
          caption: "",
          capacity: "",
        };
        this.editedShowId = null;
        toast.success("Show Edited Sucessfully !", {
          autoClose: 3000,
        });
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
    async deleteShow(showId) {
      try {
        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        };

        const response = await axios.delete(
          "http://127.0.0.1:5000/api/shows/" + showId,
          config
        );

        this.shows_data = this.shows_data.filter((show) => show.id !== showId);
        toast.success("Show Deleted Sucessfully !", {
          autoClose: 3000,
        });
        if (this.shows_data.length === 0) {
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
          console.error("Failed to delete shows:", error);
        }
      }
    },
    async fetch_shows() {
      try {
        const venueId = this.$route.params.id;
        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        };

        const response = await axios.get(
          "http://127.0.0.1:5000/api/shows/" + venueId,
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
    },
  },
  mounted() {
    this.fetch_shows();
    document.title = "Admin Show Page";
    this.check_role();
  },

  components: {
    adminNav,
  },
  mixins: [myMethods],
};
</script>
