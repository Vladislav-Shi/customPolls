<template>
  <div class="home">
    <h2>Список опросов</h2>
    <button type="button" @click="addOpenPolls" class="btn btn-secondary">Обновить</button>
    <table class="table table-sm table-hover">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Название</th>
          <th scope="col">Описание</th>
          <th scope="col">Пройти</th>
        </tr>
      </thead>
      <tbody >
        <tr v-for="(poll, index) in polls" :key="index">
          <th scope="row">{{ index }}</th>
          <td>{{ poll.name }}</td>
          <td>{{ poll.description }}</td>
          <td><router-link :to="`/poll/${poll.id}`" class="text-danger">пройти</router-link></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { authAxios } from '@/utils/auth'
// @ is an alias to /src

export default {
  name: 'HomeView',
  data() {
    return {
      polls: [],
    }
  },
  methods: {
    async addOpenPolls() {
      let response = await authAxios.get('api/polls/')
      if (response.status == 403) {
        this.$router.push("/signin")
        return
      }
      if (response.status == 200) {
        this.polls = response.data
      }
    }
  }

}
</script>
