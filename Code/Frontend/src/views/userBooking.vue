<template>
  <navBar></navBar>

  <div class="container">
    <div v-if="booked_details.length > 0">
      <h2 class="text-warning display-1 text-center">My Booking</h2>
      <table
        class="table table-hover table-dark text-center border text-warning"
      >
        <thead>
          <tr>
            <th scope="col">S.No.</th>
            <th scope="col">Show Name</th>
            <th scope="col">Date</th>
            <th scope="col">Seats</th>
            <th scope="col">Fare</th>
            <th scope="col">View Details</th>
            <th scope="col">Rate</th>
          </tr>
        </thead>
        <tbody v-for="(booking, index) in booked_details" :key="booking.id">
          <tr>
            <th scope="row" class="text-warning">{{ index + 1 }}</th>
            <td scope="col" class="text-warning">{{ booking.show_name }}</td>
            <td scope="col" class="text-warning">{{ booking.show_date }}</td>
            <td scope="col" class="text-warning">{{ booking.seats }}</td>
            <td scope="col" class="text-warning">{{ booking.price }}</td>
            <td scope="col">
              <button class="btn btn-primary" @click="downloadPDF(booking.id)">
                Download Ticket
              </button>
            </td>
            <td scope="col" class="text-black">
              <!-- Button trigger modal -->
              <button
                type="button"
                class="btn btn-primary"
                data-bs-toggle="modal"
                :data-bs-target="'#' + booking.id"
              >
                Rate</button
              ><!-- Modal -->
              <div
                class="modal fade"
                :id="booking.id"
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
                        Rate
                      </h1>
                      <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                      ></button>
                    </div>
                    <div class="modal-body">
                      <!-- -------------------------------- -->
                      <div class="form-check form-check-inline">
                        Show Rating :
                      </div>
                      <div class="form-check form-check-inline">
                        <input
                          class="form-check-input"
                          type="radio"
                          id="inlineRadio1"
                          value="1"
                          v-model="showrate"
                        />
                        <label class="form-check-label" for="inlineRadio1"
                          >1</label
                        >
                      </div>
                      <div class="form-check form-check-inline">
                        <input
                          class="form-check-input"
                          type="radio"
                          id="inlineRadio2"
                          value="2"
                          v-model="showrate"
                        />
                        <label class="form-check-label" for="inlineRadio2"
                          >2</label
                        >
                      </div>
                      <div class="form-check form-check-inline">
                        <input
                          class="form-check-input"
                          type="radio"
                          id="inlineRadio3"
                          value="3"
                          v-model="showrate"
                        />
                        <label class="form-check-label" for="inlineRadio3"
                          >3
                        </label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input
                          class="form-check-input"
                          type="radio"
                          id="inlineRadio4"
                          value="4"
                          v-model="showrate"
                        />
                        <label class="form-check-label" for="inlineRadio3"
                          >4
                        </label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input
                          class="form-check-input"
                          type="radio"
                          id="inlineRadio5"
                          value="5"
                          v-model="showrate"
                        />
                        <label class="form-check-label" for="inlineRadio4"
                          >5
                        </label>
                      </div>
                      <div class="form-check form-check-inline">
                        Venue Rating :
                      </div>
                      <div class="form-check form-check-inline">
                        <input
                          class="form-check-input"
                          type="radio"
                          id="inlineRadio1"
                          value="1"
                          v-model="venuerate"
                        />
                        <label class="form-check-label" for="inlineRadio1"
                          >1</label
                        >
                      </div>
                      <div class="form-check form-check-inline">
                        <input
                          class="form-check-input"
                          type="radio"
                          id="inlineRadio2"
                          value="2"
                          v-model="venuerate"
                        />
                        <label class="form-check-label" for="inlineRadio2"
                          >2</label
                        >
                      </div>
                      <div class="form-check form-check-inline">
                        <input
                          class="form-check-input"
                          type="radio"
                          id="inlineRadio3"
                          value="3"
                          v-model="venuerate"
                        />
                        <label class="form-check-label" for="inlineRadio3"
                          >3
                        </label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input
                          class="form-check-input"
                          type="radio"
                          id="inlineRadio4"
                          value="4"
                          v-model="venuerate"
                        />
                        <label class="form-check-label" for="inlineRadio3"
                          >4
                        </label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input
                          class="form-check-input"
                          type="radio"
                          id="inlineRadio5"
                          value="5"
                          v-model="venuerate"
                        />
                        <label class="form-check-label" for="inlineRadio4"
                          >5
                        </label>
                      </div>

                      <!-- ----------------------------------------- -->
                    </div>
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
                        data-bs-dismiss="modal"
                        @click="rating(booking.show_id, booking.venue_id)"
                      >
                        Done
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <h2 class="text-warning display-1 text-center">No Booking</h2>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import navBar from "../components/navBar.vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
export default {
  data() {
    return {
      booked_details: {},
      has_booking_details: "",
      venuerate: "",
      showrate: "",
    };
  },
  methods: {
    async rating(sid, vid) {
      try {
        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        };

        const response = await axios.post(
          "http://127.0.0.1:5000/api/rating/" + sid + "/" + vid,
          { showrate: this.showrate, venuerate: this.venuerate },
          config
        );
        this.showrate = "";
        this.venuerate = "";
        toast.success("Rating Done Sucessfully !", {
          autoClose: 2000,
        });
      } catch (error) {
        return console.error(error);
      }
    },

    async fetch_booking_details() {
      try {
        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        };

        const response = await axios.get(
          "http://127.0.0.1:5000/api/mybooking",
          config
        );
        if (response.data.success == true) {
          this.has_booking_details = response.data.success;
          this.booked_details = response.data.booked_details;
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
    async downloadPDF(id) {
      try {
       

        const response = await axios.post(
          "http://127.0.0.1:5000/api/mybooking/" + id,
      
          { responseType: "arraybuffer" }
        );

        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;

        link.click();

        window.URL.revokeObjectURL(url);
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
    this.fetch_booking_details();
    document.title = "My Bookings";
  },
  components: {
    navBar,
  },
};
</script>
