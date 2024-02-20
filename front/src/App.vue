<template>
  <div class="container">
    <!-- Nawbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand">Navbar</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false"
          aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Базовый опрос</a>
            </li>
          </ul>
          <div class="d-flex">
            <header-login></header-login>
          </div>
        </div>
      </div>
    </nav>
    <!-- End Nawbar -->

    <router-view></router-view>

  </div>
</template>

<script>
import HeaderLogin from '@/components/HeaderLogin.vue'
import store from './store';

export default {
  name: 'App',
  store: store,
  data() {
    return {
    }
  },
  computed: {
  },
  components: {
    HeaderLogin
  },
  methods: {

  }
}
</script>

<style>

</style>
