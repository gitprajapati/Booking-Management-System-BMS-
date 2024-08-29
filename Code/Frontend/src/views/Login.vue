<template>
  <body>
    <main>
      <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
          <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarTogglerDemo01"
            aria-controls="navbarTogglerDemo01"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <img
                src="@/assets/images/bmswhite.gif"
                class="navbar-brand"
                width="150"
                height="80"
              />
            </ul>

            <RouterLink class="btn btn-primary" to="/register"
              >Register</RouterLink
            >
          </div>
        </div>
      </nav>
      <div class="container-fluid">
        <header class="text-center">
          <h2 class="text-warning display-1">Welcome To BMS</h2>
          <hr class="text-warning" />
          <h1 class="text-warning">Login Here</h1>
        </header>
      </div>
      <section
        class="container my-5 w-50 p-5 text-black bg-secondary bg-gradient border border-primary-subtle rounded-3"
      >
        <div>
          <form>
            <div class="form-group">
              <label for="email">Email:</label>
              <input
                type="text"
                class="form-control"
                id="email"
                v-model="email"
                :class="{ 'is-invalid': validationErrors.email }"
              />
              <div v-if="validationErrors.email" class="invalid-feedback">
                {{ validationErrors.email }}
              </div>
            </div>
            <div class="form-group">
              <label for="password">Password:</label>
              <input
                type="password"
                class="form-control"
                id="password"
                v-model="password"
                :class="{ 'is-invalid': validationErrors.password }"
              />
              <div v-if="validationErrors.password" class="invalid-feedback">
                {{ validationErrors.password }}
              </div>
            </div>
            <br />
            <button
              type="button"
              class="btn btn-primary form-control"
              v-on:click="loginUser()"
            >
              Login
            </button>
            <div v-if="fetchApiError" class="alert alert-danger mt-4">
              {{ fetchApiError }}
            </div>
            <div v-if="apiSuccess" class="alert alert-success mt-4">
              {{ apiSuccess }}
            </div>
          </form>
        </div>
      </section>
    </main>
  </body>
</template>

<script>
import axios from "axios";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
export default {
  data() {
    return {
      email: "",
      password: "",

      validationErrors: {},
      fetchApiError: "",
      apiSuccess: "",
    };
  },
  methods: {
    async loginUser() {
      this.validationErrors = {};
      this.fetchApiError = "";
      this.apiSuccess = "";

      if (!this.email.trim()) {
        this.validationErrors.email = "email is required.";
      } else if (!this.isValidEmail(this.email)) {
        this.validationErrors.email = "Email is not valid.";
      }

      if (!this.password.trim()) {
        this.validationErrors.password = "Password is required.";
      }

      try {
        const response = await axios.post("http://127.0.0.1:5000/api/login", {
          email: this.email,
          password: this.password,
        });

        if (response.data.status == true) {
          const token = response.data.access_token;
          localStorage.setItem("token", token);
          toast.success("Login Sucessfull !", {
            autoClose: 3000,
          });
          this.apiSuccess = "Login Sucessfull";
          await new Promise((resolve) => setTimeout(resolve, 3000));
          this.$router.push("/");

          return;
        }
      } catch (error) {
        // if (response.data.data == 2) {
        //   this.fetchApiError = "Incorrect password, please try again.";
        //   toast.error("Incorrect password!!", {
        //     autoClose: 3000,
        //   });
        //   return;
        // }
        console.error(error.response.data.error);
        if (error.response && error.response.data) {
          this.fetchApiError = error.response.data.error;
          toast.error(error.response.data.error, {
            autoClose: 3000,
          });
        }
        // if (response.data.data == 3) {
        //   toast.error("Email does not exist!!", {
        //     autoClose: 3000,
        //   });
        //   this.fetchApiError = "Email does not exist.";
        //   return;
        else {
          toast.error("An error occurred. Please try again later.", {
            autoClose: 3000,
          });
          this.fetchApiError = "An error occurred. Please try again later.";
        }
      }
    },

    isValidEmail(email) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    },
  },
  mounted() {
    document.title = "Login";
  },
};
</script>
