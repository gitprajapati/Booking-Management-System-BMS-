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

            <RouterLink class="btn btn-primary" to="/login">Login</RouterLink>
          </div>
        </div>
      </nav>
      <div class="container-fluid">
        <header class="text-center">
          <h2 class="text-warning display-1">Welcome To BMS</h2>
          <hr class="text-warning" />
          <h1 class="text-warning">Register Here</h1>
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
            <div class="row">
              <div class="col">
                <label for="first_name">First Name:</label>
                <input
                  type="text"
                  class="form-control"
                  id="first_name"
                  v-model="first_name"
                  :class="{ 'is-invalid': validationErrors.first_name }"
                />
                <div
                  v-if="validationErrors.first_name"
                  class="invalid-feedback"
                >
                  {{ validationErrors.first_name }}
                </div>
              </div>
              <div class="col">
                <label for="lastname">Last Name:</label>
                <input type="text" class="form-control" v-model="last_name" />
              </div>
            </div>

            <div class="mt-3">
              <label for="username">Username:</label>
              <input
                type="text"
                class="form-control"
                id="username"
                v-model="username"
                :class="{ 'is-invalid': validationErrors.username }"
              />
              <div v-if="validationErrors.username" class="invalid-feedback">
                {{ validationErrors.username }}
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
            <div class="form-group">
              <label for="c_password">Confirm Password:</label>
              <input
                type="text"
                class="form-control"
                id="c_password"
                v-model="c_password"
                :class="{ 'is-invalid': validationErrors.c_password }"
              />
              <div v-if="validationErrors.c_password" class="invalid-feedback">
                {{ validationErrors.c_password }}
              </div>
            </div>

            <div class="form-group">
              <label for="userType">Role:</label>
              <select
                class="form-control"
                id="userType"
                name="userType"
                v-model="userType"
              >
                <option value="2">User</option>
                <option v-if="this.admin_exists == false" value="1">
                  Admin
                </option>
              </select>
              
            </div>
            <br />

            <button
              type="button"
              class="btn btn-primary form-control"
              v-on:click="registerUser()"
            >
              Submit
            </button>
            <div v-if="apiError" class="alert alert-danger mt-3">
              {{ apiError }}
            </div>
            <div v-if="apiSuccess" class="alert alert-success mt-3">
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

export default {
  data() {
    return {
      post_image_url: "",
      email: "",
      first_name: "",
      last_name: "",
      username: "",
      password: "",
      c_password: "",
      userType: "",
      validationErrors: {},
      apiError: "",
      apiSuccess: "",
      admin_exists: "",
    };
  },
  methods: {
    async check_admin() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/register");

        this.admin_exists = response.data.admin_exists;
        this.post_image_url = response.data.url;
      } catch (error) {
        console.error(error);
      }
    },
    async registerUser() {
      this.validationErrors = {};
      this.apiError = "";
      this.apiSuccess = "";

      if (!this.username.trim()) {
        this.validationErrors.username = "Username is required.";
      }
      if (!this.email.trim()) {
        this.validationErrors.email = "email is required.";
      } else if (!this.isValidEmail(this.email)) {
        this.validationErrors.email = "Email is not valid.";
      }
      
      if (!this.email.trim()) {
        this.validationErrors.email = "Email is required.";
      }
      if (!this.password.trim()) {
        this.validationErrors.password = "Password is required.";
      }
      if (!this.first_name.trim()) {
        this.validationErrors.first_name = "First name is required.";
      }
     
      if (this.password !== this.c_password) {
        this.validationErrors.c_password = "Password not match.";
      }
      if (Object.keys(this.validationErrors).length > 0) {
        return;
      }

      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/register",
          {
            username: this.username,
            email: this.email,
            password: this.password,
            first_name: this.first_name,
            last_name: this.last_name,
            userType: this.userType,
          }
        );
        this.$router.push("/login");
        this.apiSuccess = "Registration successful.";
        this.username = "";
        this.email = "";
        this.password = "";
        this.c_password = "";
        this.first_name = "";
        this.last_name = "";
        this.userType = "";
      } catch (error) {
        console.error(error.response.data.error);
        if (error.response && error.response.data) {
          this.apiError = error.response.data.error;
        } else {
          this.apiError = "An error occurred.";
        }
      }
    },
    isValidEmail(email) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    },
  },

  mounted() {
    document.title = "Register";
    this.check_admin();
  },
};
</script>
