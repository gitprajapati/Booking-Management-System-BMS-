<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-dark">
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
          <RouterLink class="nav-link" to="/"
            ><img
              src="@/assets/images/bmsblack.gif"
              class="navbar-brand"
              width="150"
              height="80"
          /></RouterLink>
        </li>
      </ul>

      <button class="btn btn-primary mr-2" id="logout-button" @click="logout">
        Logout
      </button>
    </div>
  </nav>
</template>

<style scoped>
#logout-button {
  margin-left: auto;
  margin-right: 10px;
}
</style>

<script>
import myMethods from "../mixins/myMethods";

export default {
  mixins: [myMethods],
};
</script>

