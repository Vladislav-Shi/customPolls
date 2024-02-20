<template>
  <div v-if="loading">Loading...</div>
  <div class="row" v-else>
    <div class="col-3"></div>
    <div class="col" v-if="error == null">
      <h2>{{ pollName }}</h2>
      <div action="" id="FormPoll" class="form">
        <QuectionComponent
        @ValidateError="validate[item.id] = false"
        @validateSuccses="validate[item.id] = true"
          :ref="`field_${item.id}`"
          v-for="(item) in currentQuestions"
          :key="item"
          :question="item"
        />
        <div class="row">
          <div v-if="currentSection > 0" class="col-6">
            <button
              id="form-submit"
              class="btn btn-primary btn-block"
              @click="changeSectionDown"
            >
              &#8592; назад
            </button>
          </div>

          <div v-if="currentSection == sections - 1" class="col">
            <button
              id="form-submit"
              class="btn btn-primary btn-block"
              @click="submitForm"
              :disabled="disbledButton"
            >
              Подтвердить
            </button>
          </div>
          <div v-else class="col">
            <button
              id="form-submit"
              class="btn btn-primary btn-block"
              @click="changeSectionUp"
              :disabled="disbledButton"
            >
              {{ currentSection + 1 }} из {{ sections }} Секций
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <h3 class="text-warning">{{ error }}</h3>
    </div>
    <div class="col-3"></div>
  </div>
</template>

<script>
import { authAxios } from "@/utils/auth";
import QuectionComponent from "@/components/QuectionComponent.vue";
// @ is an alias to /src

export default {
  name: "PollView",
  data() {
    return {
      loading: true,
      questions: [],
      currentSection: 0,
      ansvers: [],
      pollName: "Имя не задано",
      error: null,
      polls: {},
      sections: 0,
      validate: {}
    };
  },
  computed: {
    currentQuestions() {
      return this.polls.sections[this.currentSection].questions;
    },
    disbledButton(){
        console.log('disbledButton', this.validate)
        return Object.values(this.validate).includes(false)
    },
  },
  components: {
    QuectionComponent,
  },

  methods: {
    changeSectionUp() {
      this.currentSection += 1;
      console.log("questionUp", this.currentQuestions);
    },
    changeSectionDown() {
      this.currentSection -= 1;
      console.log("questionDown", this.currentQuestions);

    },
    saveChangeField () {},

    async submitForm() {
        let data = this.$store.state.ansvers
        console.log('data', data)
        await authAxios.post(`api/poll/${this.$route.params.id}`, data)
        console.log('`base/${this.$route.params.id}/`', `api/poll/${this.$route.params.id}`)
    },

    async getQuestions() {
      let response = await authAxios
        .get(`api/poll/${this.$route.params.id}`)
        .catch(() => {
          this.$data.error =
            "Страница не найдена или вы не можете пройти данный опрос";
        });
      if (response.status == 404) {
        this.$data.error =
          "Страница не найдена или вы не можете пройти данный опрос";
        return;
      }
      this.polls = response.data;
      this.sections = this.polls.sections.length;
      console.log("response", response.data);
    },
    async addOpenPolls() {
      let response = await authAxios.get("api/polls/");
      if (response.status == 403) {
        this.$router.push("/signin");
        return;
      }
      if (response.status == 200) {
        this.polls = response.data;
      }
    },
  },
  created() {
    this.$store.commit('clear_question')
    this.getQuestions().finally(() => (this.loading = false));
  },
};
</script>
