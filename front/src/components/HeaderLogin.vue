<template>
    <ul class="navbar-nav" v-if="is_active">
        <li class="nav-item">
            <a class="nav-link"> {{ username }} </a>
        </li>
        <li class="nav-item">
            <a href="#" class="nav-link" @click="signout">signout</a>
        </li>
    </ul>
    <ul class="navbar-nav" v-else>
        <li class="nav-item">
            <router-link to="/signin/" class="nav-link">signin</router-link>
        </li>
    </ul>
</template>

<script>
import store from '@/store'

export default {
    name: 'HeaderLogin',
    data() {
        return {
        }
    },
    computed: {
        username() { return store.state.auth.username },
        is_active() { return store.state.auth.username != null }
    },
    components: {
    },
    methods: {
        signout() {
            this.$store.dispatch('logout')
            this.$router.push({ path: 'signin/', query: { msg: 'logout' } })
        }
    }
}
</script>