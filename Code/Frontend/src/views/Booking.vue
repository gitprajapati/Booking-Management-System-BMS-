<template>
  <navBar></navBar>
  <div class="container-fluid">
    <h2 class="text-warning display-1 text-center">Booking</h2>
    <div class="text-center text-warning">
      <h1>Show name : {{ shows_data.name }}</h1>
    </div>
    <section
      class="container my-5 w-50 p-5 text-black bg-secondary bg-gradient border border-primary-subtle rounded-3"
    >
      <form class="d-flex">
        <input
          type="date"
          class="form-control"
          :min="`${shows_data.start_date}`"
          :max="`${shows_data.out_date}`"
          v-model="inputDate"
          required
        />
        <button
          class="btn btn-danger"
          type="button"
          @click="showsByDate(shows_data.id)"
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
    <div v-if="success == true" class="text-center text-warning">
      <div class="row">
        <h1 class="col">Remaining seats : {{ booking_data.capacity }}</h1>

        <h1 class="col">Ticket cost : {{ booking_data.price }}</h1>
      </div>
      <div v-if="purchased == true">
        <button
          type="button"
          class="btn btn-success"
          @click="downloadPDF(this.booked_id)"
        >
          <h2>Click Here to download ticket</h2>
        </button>
      </div>
      <section
        v-if="booking_data.capacity > 0"
        class="container my-3 w-50 p-5 text-black bg-secondary bg-gradient border border-primary-subtle rounded-3"
      >
        <p>Select number of seats</p>
        <form class="d-flex form-check form-check-inline">
          <div class="form-check form-check-inline">
            <input
              class="form-check-input"
              type="radio"
              id="inlineRadio1"
              value="1"
              v-model="seat"
              @change="handleChange"
            />
            <label class="form-check-label" for="inlineRadio1">1</label>
          </div>
          <div class="form-check form-check-inline">
            <input
              class="form-check-input"
              type="radio"
              id="inlineRadio2"
              value="2"
              v-model="seat"
              @change="handleChange"
            />
            <label class="form-check-label" for="inlineRadio2">2</label>
          </div>
          <div class="form-check form-check-inline">
            <input
              class="form-check-input"
              type="radio"
              id="inlineRadio3"
              value="3"
              v-model="seat"
              @change="handleChange"
            />
            <label class="form-check-label" for="inlineRadio3">3 </label>
          </div>
          <div class="form-check form-check-inline">
            <input
              class="form-check-input"
              type="radio"
              id="inlineRadio4"
              value="4"
              v-model="seat"
              @change="handleChange"
            />
            <label class="form-check-label" for="inlineRadio3">4 </label>
          </div>
          <div class="form-check form-check-inline">
            <input
              class="form-check-input"
              type="radio"
              id="inlineRadio5"
              value="5"
              v-model="seat"
              @change="handleChange"
            />
            <label class="form-check-label" for="inlineRadio4">5 </label>
          </div>
          <div class="form-check form-check-inline">
            <input
              class="form-check-input"
              type="radio"
              id="inlineRadio6"
              value="6"
              v-model="seat"
              @change="handleChange"
            />
            <label class="form-check-label" for="inlineRadio6"> 6 </label>
            <div class="form-check form-check-inline">
              <input
                class="form-check-input"
                type="radio"
                id="inlineRadio7"
                value="7"
                v-model="seat"
                @change="handleChange"
              />
              <label class="form-check-label" for="inlineRadio7"> 7 </label>
            </div>
            <div class="form-check form-check-inline">
              <input
                class="form-check-input"
                type="radio"
                id="inlineRadio8"
                value="8"
                v-model="seat"
                @change="handleChange"
              />
              <label class="form-check-label" for="inlineRadio8">8 </label>
            </div>
            <div class="form-check form-check-inline">
              <input
                class="form-check-input"
                type="radio"
                id="inlineRadio9"
                value="9"
                v-model="seat"
                @change="handleChange"
              />
              <label class="form-check-label" for="inlineRadio9">9 </label>
            </div>
          </div>
          <button class="btn btn-danger" type="button" @click="cost()">
            Proceed
          </button>
        </form>
        <div>
          <div
            v-if="totalCost > 0 && booking_data.capacity >= seat"
            class="row mt-5"
          >
            <div class="col">
              <h3 class="mb-5">Total Cost : {{ this.totalCost }}</h3>
            </div>
            <div class="col">
              <button
                type="button"
                class="btn btn-success"
                @click="purchase(booking_data.id)"
              >
                BUY
              </button>
            </div>
          </div>
          <div v-else-if="booking_data.capacity < seat">
            <h3 class="text-danger">
              You can book upto {{ booking_data.capacity }} seats only.
            </h3>
          </div>
        </div>
      </section>
      <div v-else-if="booking_data.capacity == 0">
        <h1 class="text-danger">Houseful !!</h1>
        <h3 class="text-danger">You can book search for other dates.</h3>
      </div>
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
      shows_data: {},
      shows: "",
      success: "",
      inputDate: "",
      booking_data: {},
      seat: "",
      totalCost: "",
      purchased: "",
      booked_id: "",
    };
  },
  methods: {
    handleChange() {
      this.totalCost = "";
      this.purchased = "";
    },
    async purchase(bookingId) {
      const config = {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      };
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/purchase/" + bookingId,
          { seat: this.seat },
          config
        );

        if (response.data.success == true) {
          const numSeats = parseInt(this.seat, 10);
          const totalSeat = this.booking_data.capacity;
          this.booking_data.capacity = totalSeat - numSeats;
          this.totalCost = 0;
          this.seat = "";
          this.purchased = true;
          this.booked_id = response.data.id;
          toast.success("Booking Done Sucessfully !", {
            autoClose: 3000,
          });
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
    async showsByDate(showId) {
      const config = {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      };
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/showbooking/" + showId,
          {
            date: this.inputDate,
          },
          config
        );
        if (response.data.success == true) {
          this.success = true;

          this.booking_data = response.data.booking_data;
        } else {
          this.success = false;
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
    cost() {
      if (this.seat !== "" && this.seat <= this.booking_data.capacity) {
        const numSeats = parseInt(this.seat, 10);

        this.totalCost = numSeats * this.booking_data.price;
      } else if (this.seat !== "" && this.seat > this.booking_data.capacity) {
        toast.success("Choose seates within range.", {
          autoClose: 3000,
        });
      } else {
        toast.success("Please select the number of seats before proceeding.", {
          autoClose: 3000,
        });
      }
    },

    async getShows() {
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
    },
    async downloadPDF(id) {
      try {
        let access_token = localStorage.getItem("access_token");
        axios.defaults.headers.common["Authorization"] =
          "Bearer " + access_token;

        const response = await axios.post(
          "http://127.0.0.1:5000/api/mybooking/" + id,
          { responseType: "arraybuffer" }
        );

        const url = window.URL.createObjectURL(new Blob([response.data]));

        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "myBooking.pdf");
        document.body.appendChild(link);
        link.click();

        window.URL.revokeObjectURL(url);
      } catch (error) {
        if (error.response && error.response.status === 401) {
          alert("Oops time expired...");
          localStorage.removeItem("token");
          this.$router.push("/login");
        } else if (error.response && error.response.status === 422) {
          this.$router.push("/login");
        } else {
          console.error(error);
        }
      }
    },
  },
  mounted() {
    this.getShows();
    document.title = "Booking Page";
  },
  components: {
    navBar,
  },
};
</script>
