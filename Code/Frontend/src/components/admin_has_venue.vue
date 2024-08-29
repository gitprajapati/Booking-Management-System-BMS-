<template>
  <div class="text-center" v-if="venues == true">
    <h1 class="text-warning">-:Venue:-</h1>

    <br />

    <RouterLink class="btn btn-primary" to="/createvenue">Add venue</RouterLink>

    <br />
    <br />
    <table class="table table-striped">
      <thead>
        <tr class="text-warning">
          <th scope="col">S.No.</th>
          <th scope="col">Venue Name</th>
          <th scope="col">Venue Location</th>

          <th scope="col">Actions</th>
          <th scope="col">Add Show</th>
          <th scope="col">View Show</th>
          <th scope="col">Export Details</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(venue, index) in venue_data" :key="venue.id">
          <th scope="row" class="text-warning">{{ index + 1 }}</th>
          <td class="text-warning">{{ venue.name }}</td>
          <td class="text-warning">{{ venue.city }}</td>

          <td>
            <!-- Button trigger modal -->
            <button
              type="button"
              class="btn btn-warning rounded-pill"
              data-bs-toggle="modal"
              :data-bs-target="'#staticBackdrop-' + venue.id"
            >
              Edit
            </button>

            <!-- Modal -->
            <div
              class="modal fade"
              :id="'staticBackdrop-' + venue.id"
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
                      Edit Venue
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
                            :placeholder="venue.name"
                            v-model="editedVenuedata.name"
                            type="text"
                            class="form-control"
                            id="name"
                            required
                          />
                        </div>
                        <div class="form-group">
                          <label for="address">Address:</label>
                          <input
                            v-model="editedVenuedata.address"
                            :placeholder="venue.address"
                            type="text"
                            class="form-control"
                            id="address"
                            required
                          />
                        </div>
                        <div class="form-group">
                          <label for="city">City:</label>
                          <input
                            v-model="editedVenuedata.city"
                            :placeholder="venue.city"
                            type="text"
                            class="form-control"
                            id="city"
                            required
                          />
                        </div>
                        <div class="form-group">
                          <label for="state">State:</label>
                          <input
                            v-model="editedVenuedata.state"
                            :placeholder="venue.state"
                            type="text"
                            class="form-control"
                            id="state"
                            required
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
                      @click="editVenue(venue.id)"
                      data-bs-dismiss="modal"
                    >
                      Edit Venue
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <!-- Button trigger modal -->
            <button
              type="button"
              class="btn btn-danger rounded-pill"
              data-bs-toggle="modal"
              :data-bs-target="'#staticBackdrop2-' + venue.id"
            >
              Delete
            </button>
            <!-- Modal -->
            <div
              class="modal fade"
              :id="'staticBackdrop2-' + venue.id"
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
                      Delete Venue
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
                      @click="deleteVenue(venue.id)"
                      data-bs-dismiss="modal"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </td>
          <td>
            <RouterLink
              class="btn btn-primary rounded-pill"
              :to="`/createshow/${venue.id}`"
            >
              Add Show
            </RouterLink>
          </td>

          <td>
            <RouterLink
              class="btn btn-success rounded-pill position-relative"
              :to="`/viewshows/${venue.id}`"
            >
              View Shows
              <span
                class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
              >
                {{ venue.shows.length }}
                <span class="visually-hidden">unread messages</span>
              </span>
            </RouterLink>
          </td>
          <td>
            <button
              type="button"
              class="btn btn-warning rounded-pill"
              v-on:click="exportCSV(venue.id)"
            >
              Export CSV
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <admin_no_venue v-if="venues == false"></admin_no_venue>
</template>

<script>
import myMethods from "@/mixins/myMethods";
import axios from "axios";
import admin_no_venue from "../components/admin_no_venue.vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
export default {
  data() {
    return {
      venues: null,
      venue_data: {},
      editedVenuedata: {
        name: "",
        address: "",
        city: "",
        state: "",

        owner_id: "",
      },
      editedVenueId: null,
    };
  },
  methods: {
    async exportCSV(id) {
      try {
        let access_token = localStorage.getItem("access_token");
        toast.warning("Please wait for download.", {
          autoClose: 2000,
        });
        axios.defaults.headers.common["Authorization"] =
          "Bearer " + access_token;

        const response = await axios.get(
          "http://127.0.0.1:5000/api/exportcsv/" + id,
          { responseType: "blob" } // Use 'blob' as the responseType
        );

        // Create a Blob from the response data
        const blob = new Blob([response.data], { type: "application/csv" });

        // Create a URL for the Blob
        const url = window.URL.createObjectURL(blob);

        // Create an anchor element to trigger the download
        const link = document.createElement("a");
        link.href = url;
        link.download = "csvfile" + id + ".csv"; // Set the filename for the downloaded CSV file
        link.click();
        toast.success("File downloaded Sucessfully.", {
          autoClose: 3000,
        });
        // Cleanup the URL and the link
        window.URL.revokeObjectURL(url);
      } catch (error) {
        if (error.response && error.response.status === 401) {
          alert("Opps time expired...");
          localStorage.removeItem("token"), this.$router.push("/login");
        } else {
          console.error(error);
          // Handle other errors appropriately
        }
      }
    },

    async deleteVenue(venueId) {
      try {
        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        };

        const response = await axios.delete(
          "http://127.0.0.1:5000/api/venues/" + venueId,
          config
        );

        console.log("Venue deleted successfully");
        this.venue_data = this.venue_data.filter(
          (venue) => venue.id !== venueId
        );
        console.log(this.venue_data);
        toast.success("Venue Deleted Sucessfully !", {
          autoClose: 3000,
        });
        if (this.venue_data.length === 0) {
          // If all venues are deleted, set 'venues' to false
          this.venues = false;
        }
      } catch (error) {
        console.error(error.response.data.error);
        if (error.response && error.response.status === 404) {
          toast.error(error.response.data.error, {
            autoClose: 3000,
          });
        }
        if (error.response && error.response.status === 401) {
          alert("Opps time expired...");
          localStorage.removeItem("token"), this.$router.push("/login");
        }
        if (error.response && error.response.status === 422) {
          this.$router.push("/login");
        } else {
          console.error("Failed to delete venue:", error);
          // Handle other errors appropriately
        }
      }
    },
    async editVenue(venueId) {
      try {
        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        };

        await axios.put(
          "http://127.0.0.1:5000/api/venues/" + venueId,
          {
            name: this.editedVenuedata.name,
            address: this.editedVenuedata.address,
            city: this.editedVenuedata.city,
            state: this.editedVenuedata.state,
          },
          config
        );

        const editedVenue = this.venue_data.find(
          (venue) => venue.id === venueId
        );
        if (editedVenue) {
          if (this.editedVenuedata.name) {
            editedVenue.name = this.editedVenuedata.name;
          }
          if (this.editedVenuedata.address) {
            editedVenue.address = this.editedVenuedata.address;
          }
          if (this.editedVenuedata.city) {
            editedVenue.city = this.editedVenuedata.city;
          }
        }

        this.editedVenuedata = {
          name: "",
          address: "",
          city: "",
          state: "",

          owner_id: "",
        };
        this.editedVenueId = null;
        toast.success("Venue Edited Sucessfully !", {
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
  },
  mixins: [myMethods],
  mounted() {
    this.check_venue();
  },
  components: {
    admin_no_venue,
  },
};
</script>
