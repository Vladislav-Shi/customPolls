<template>
    <div class="row content">
        <div v-if="!!alert && !!messages[alert]">
            <p :class="messages[alert]['type']">{{ messages[alert]['text'] }}</p>
        </div>
        <div class="title">
            <h1>Авторизация</h1>
        </div>
        <div class="col-2"></div>
        <div class="col">
            <!-- Pills navs -->
            <div class="btn-group btns">
                <a to="/signin/" class="btn btn-secondary btn-lg active">Login</a>
            </div>

            <!-- Pills content -->
            <div class="">
                <div>
                    <form>
                        <!-- Email input -->
                        <div class="form-outline mb-4">
                            <input type="text" v-model="username" id="loginName" class="form-control" />
                            <label class="form-label" for="loginName">username</label>
                        </div>

                        <!-- Password input -->
                        <div class="form-outline mb-4">
                            <input type="password" v-model="password" id="loginPassword" class="form-control" />
                            <label class="form-label" for="loginPassword">Password</label>
                        </div>

                        <!-- 2 column grid layout -->
                        <div class="row mb-4">
                            <div class="col-md-6 d-flex justify-content-center">
                                <!-- Checkbox -->
                                <div class="form-check mb-3 mb-md-0">
                                    <input class="form-check-input" type="checkbox" value="" id="loginCheck" checked />
                                    <label class="form-check-label" for="loginCheck"> Remember me </label>
                                </div>
                            </div>

                            <div class="col-md-6 d-flex justify-content-center">
                                <!-- Simple link -->
                                <a href="#!">Forgot password?</a>
                            </div>
                        </div>
                    </form>
                    <!-- Submit button -->
                    <button :disabled="submit" @click="login" class="btn btn-secondary btn-block mb-4 btn-lg">Sign in</button>

                </div>
            </div>
        </div>
        <div class="col-2"></div>

    </div>
</template>

<style>
.content {
    margin-top: 30px;
}
</style>

<script>
import messagesArray from '../utils/messages'

export default {
    name: 'LoginPage',
    data() {
        return {
            username: '',
            password: '',
            alert: this.$route.query.msg,
            messages: messagesArray
        }
    },
    computed: {
        submit() { return !(this.username.length && this.password.length) }
    },
    methods: {
        login() {
            let username = this.username
            let password = this.password
            this.$store.dispatch('login', { username, password })
                .then(() => {
                    if (this.$store.state.auth.status == 'error')
                    {
                        throw 'Ошибка авторизации'
                    }
                    this.$router.push({ path: '/', query: { msg: 'auth' } })
                }
                )
                .catch(err => {
                    console.log('auth-error')
                    console.log(err)
                })
        },
    },
}
</script>

<style>
.title {
    text-align: center;
}

.btns {
    width: 100%;
    margin-bottom: 20px;
}
</style>