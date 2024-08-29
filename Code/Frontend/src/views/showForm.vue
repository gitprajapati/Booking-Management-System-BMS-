<template>
  <body>
    <main>
      <adminNav></adminNav>
      <h1 class="text-center text-warning">Create Show</h1>
      <div
        class="container col-lg-5 text-black bg-secondary bg-gradient border border-primary-subtle rounded-3"
      >
        <div class="row justify-content-center">
          <div class="">
            <form enctype="multipart/form-data">
              <div class="form-group">
                <label for="name">Name:</label>
                <input
                  type="text"
                  class="form-control"
                  id="name"
                  v-model="show.name"
                  required
                />
              </div>

              <div class="form-group">
                <label for="caption">Caption:</label>
                <textarea
                  type="text"
                  class="form-control"
                  id="caption"
                  v-model="show.caption"
                  required
                ></textarea>
              </div>
              <div class="form-group">
                <label for="capacity">Capacity:</label>
                <input
                  v-model="show.capacity"
                  type="number"
                  class="form-control"
                  id="capacity"
                  required
                />
              </div>
              <div class="form-group">
                <label for="price">Price:</label>
                <input
                  type="number"
                  class="form-control"
                  id="price"
                  v-model="show.price"
                  required
                />
              </div>
              <div class="form-group">
                <label for="startdate">Start Date:</label>
                <input
                  type="date"
                  class="form-control"
                  id="startdate"
                  required
                  pattern="\d{4}-\d{2}-\d{2}"
                  v-model="show.start_date"
                  :min="currentDate"
                />
              </div>
              <div class="form-group">
                <label for="outdate">Out Date:</label>
                <input
                  type="date"
                  class="form-control"
                  id="date"
                  required
                  pattern="\d{4}-\d{2}-\d{2}"
                  v-model="show.out_date"
                  :min="currentDate"
                />
              </div>
              <label for="radio">Genre:</label>
              <div class="form-group" id="radio">
                <div class="form-row">
                  <div class="col">
                    <input
                      type="radio"
                      id="Action"
                      value="Action"
                      v-model="show.tags"
                    /><label for="Action">Action</label>

                    <input
                      type="radio"
                      id="Horror"
                      value="Horror"
                      v-model="show.tags"
                    /><label for="Horror">Horror</label>

                    <input
                      type="radio"
                      id="Drama"
                      value="Drama"
                      v-model="show.tags"
                    /><label for="Drama">Drama</label>

                    <input
                      type="radio"
                      id="Romance"
                      value="Romance"
                      v-model="show.tags"
                    /><label for="Romance">Romance</label>
                  </div>
                </div>
              </div>

              <div class="form-group mt-2">
                <label for="formFile" class="form-label">Upload Image: </label>
                <input
                  type="file"
                  class="form-control"
                  v-on:change="onFileChange"
                  id="image"
                  accept=".jpg,.gif,.png,.jpeg"
                  ref="image"
                  
                />
              </div>
              <div class="form-group">
                <label for="duration">Duration:</label>
                <input
                  type="text"
                  class="form-control"
                  id="duration"
                  name="duration"
                  v-model="show.duration"
                  placeholder="HH:MM"
                  required
                />
              </div>

              <button
                type="button"
                class="btn btn-primary form-control mt-3 mb-3"
                v-on:click="createShow()"
                enctype="multipart/form-data"
              >
                Create Show
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
      currentDate: "",
      show: {
        name: "",
        duration: "",
        start_date: "",
        out_date: "",
        tags: "",
        price: "",
        caption: "",
        image: null,
      },
    };
  },

  methods: {
    onFileChange(event) {
      this.show.image = event.target.files[0];
    },

    async createShow() {
      let formData = new FormData();

      formData.append("data", JSON.stringify(this.show));

      if (this.show.image) {
        formData.append("image", this.show.image);
      }
      try {
        const venueId = this.$route.params.id;
        const d1 = Date.parse(this.show.start_date);

        const d2 = Date.parse(this.show.out_date);
        if (d1 > d2) {
          this.show.out_date = "";
          this.show.start_date = "";
          toast.error("Start date should be less than the out date");
        } else {
          const config = {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          };

          await axios.post(
            "http://127.0.0.1:5000/api/shows/" + venueId,

            formData,

            config
          );

          this.show.name = "";
          this.show.out_date = "";
          this.show.duration = "";
          this.show.start_date = "";
          this.show.tags = "";
          this.show.price = "";
          this.show.capacity = "";
          this.show.caption = "";
          toast.success("Show Added Sucessfully !", {
            autoClose: 3000,
          });
          await new Promise((resolve) => setTimeout(resolve, 3000));
          this.$router.push("/");
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
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");
    this.currentDate = year + "-" + month + "-" + day;
    document.title = "Show Form";
  },

  components: {
    adminNav,
  },
};
</script>
