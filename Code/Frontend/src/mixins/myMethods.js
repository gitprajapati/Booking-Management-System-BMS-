// mixins/myMethods.js
import axios from "axios";
export default {
  methods: {
    async logout() {
      try {
        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        };
        await axios.delete("http://127.0.0.1:5000/api/logout", config),
          localStorage.removeItem("token"),
          this.$router.push("/login");
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
    async check_role() {
      try {
        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        };
        const response = await axios.get(
          "http://127.0.0.1:5000/api/check-role",
          config
        );

        this.role = response.data.role;
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
    async check_venue() {
      try {
        const config = {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        };
        const response = await axios.get(
          "http://127.0.0.1:5000/api/venues",
          config
        );
        if (response.data.venues == true) {
          this.venues = true;
          this.venue_data = response.data.venue_data;
        } else {
          this.venues = false;
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
};
