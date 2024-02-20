<template>
    <div class="page-content page-container">
        <div v-if="!!alert && !!messages[alert]">
            <p :class="messages[alert]['type']">{{ messages[alert]['text'] }}</p>
        </div>

        <h3>Выбор чатов</h3>
        <button class="btn btn-outline-secondary" @click="getChatList">Обновить</button>
        <div>
            <table class="table table-hover table-borderless">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">chat name</th>
                        <th scope="col">new messages</th>
                        <th scope="col">link</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="chat in chats" :key="chat">
                        <th scope="row">{{ chat['id'] }}</th>
                        <td>{{ chat['chatName'] }}</td>
                        <td>{{ chat['newMessages'] }}</td>
                        <td>
                            <router-link :to="chat['link']" type="button" class="btn btn-outline-secondary">открыть</router-link>
                        </td>
                    </tr>

                </tbody>
            </table>
        </div>

        <div class="mt-2">
            <router-link to="/create/" type="button" class="btn btn-outline-secondary">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-lg" viewBox="-1 1 16 17">
                    <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z" />
                </svg>
                Создать чат
            </router-link>
        </div>

    </div>
</template>

<script>
import { authAxios } from '../utils/auth'
import messagesArray from '../utils/messages'

export default {
    name: 'HomePage',
    data() {
        return {
            chats: [],
            alert: this.$route.query.msg,
            messages: messagesArray
        }
    },

    methods: {

        chatListToData(data) {
            let chats = []
            data.forEach(element => {
                chats.push({ id: element.id, chatName: element.name, newMessages: 0, link: `/chat/${element.id}` })
            });
            return chats
        },

        async getChatList() {
            let response = await authAxios.get('api/list/')
            console.log('response', response)
            if (response.status == 403) {
                this.$router.push("/signin")
                return
            }
            this.$data.chats = this.chatListToData(response.data)
        }
    },
    created() {
        this.getChatList()
    }
}
</script>

<style></style>