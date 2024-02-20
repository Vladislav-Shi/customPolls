<template>
  <div
    v-if="getQuestion.question_type == 'text'"
    data-mdb-input-init
    :class="{ 'form-outline mb-4': true, 'was-validated': validate_error }"
  >
    <label class="form-label" for="form1Example2">{{ getQuestion.text }}</label>

    <input
      :required="getQuestion.required"
      type="text"
      id="form1Example2"
      v-model="selectedOption"
      :name="`field__${getQuestion.id}`"
      class="form-control"
      @change="saveData"
    />
    <small class="text-muted" v-if="getQuestion.required"
      >обязательное поле</small
    >
  </div>

  <div v-if="question_data.question_type == 'single_choice'">
    <!-- Виджет поля radio select -->
    <div data-mdb-input-init class="form-outline mb-4">
      <label class="form-label" for="form1Example2">{{
        getQuestion.text
      }}</label>
      <fieldset>
        <small class="text-muted" v-if="getQuestion.required"
          >обязательное поле</small
        >

        <div
          v-for="(choice, index) in getQuestion.choices"
          :key="index"
          class="form-check"
        >
          <input
            class="form-check-input"
            type="radio"
            :name="`field__${getQuestion.id}`"
            id="flexRadioDefault1"
            :value="`$${choice.id}`"
            v-model="selectedOption"
            :required="getQuestion.required"
            @change="saveData"
            :checked="getValueStore == `$${choice.id}`"
          />
          <label class="form-check-label">
            {{ choice.text }}
          </label>
        </div>
        <div v-if="getQuestion.other_field" class="form-check">
          <input
            :required="getQuestion.required"
            class="form-check-input mt-2"
            type="radio"
            :name="`field__${getQuestion.id}`"
            value="$other"
            v-model="selectedOption"
            @change="saveData"
          />
          <label class="form-check-label">
            <input
              type="text"
              :name="`field__${getQuestion.id}__other`"
              id="field__{{getQuestion.id}}__other"
              class="form-control"
              placeholder="Другое"
              aria-label="Text input with checkbox"
              @change="saveData"
              v-model="valueOther"
            />
          </label>
        </div>
      </fieldset>
    </div>
  </div>

  <div v-if="question_data.question_type == 'multiple_choice'">
    <!-- Виджет поля multy select -->
    <div data-mdb-input-init class="form-outline mb-4">
      <label class="form-label" for="form1Example2">{{
        getQuestion.text
      }}</label>
      <fieldset>
        <small class="text-muted" v-if="getQuestion.required"
          >обязательное поле</small
        >

        <div
          v-for="(choice, index) in getQuestion.choices"
          :key="index"
          class="form-check"
        >
          <input
            :required="getQuestion.required"
            class="form-check-input"
            type="checkbox"
            :name="`field__${getQuestion.id}`"
            :value="`$${choice.id}`"
            v-model="selectedOption"
            @change="saveData"
          />
          <label class="form-check-label">
            {{ choice.text }}
          </label>
        </div>
        <div v-if="getQuestion.other_field" class="form-check">
          <input
            :required="getQuestion.required"
            class="form-check-input mt-2"
            type="checkbox"
            :name="`field__${getQuestion.id}`"
            value="$other"
            @change="saveData"
          />
          <label class="form-check-label">
            <input
              type="text"
              :name="`field__${getQuestion.id}__other`"
              id="field__{{getQuestion.id}}__other"
              class="form-control"
              placeholder="Другое"
              v-model="valueOther"
              @change="saveData"
            />
          </label>
        </div>
      </fieldset>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "QuectionComponent",
  data() {
    return {
      question_data: this.question,
      selectedOption: null,
      valueOther: null,
      value: null,
      validate_error: null,
    };
  },
  computed: {
    getQuestion() {
      return this.question;
    },
    getValueStore() {
      return this.$store.state.ansvers[`field__${this.getQuestion.id}`];
    },
  },
  emits: ["ValidateError", "ValidateSuccses"],
  props: {
    question: Object,
  },
  methods: {
    validateField() {
      if (this.getQuestion.required && !this.selectedOption) {
        this.validate_error = true;
        this.$emit("ValidateError", this.getQuestion.id);
      } else {
        this.$emit("ValidateSuccses", this.getQuestion.id);
        this.validate_error = false;
      }
    },

    saveData() {
      console.log("Save Data");
      this.validateField();

      if (this.selectedOption == "$other") {
        this.value = this.valueOther;
      } else {
        this.value = this.selectedOption;
      }
      this.$store.commit("add_question", {
        question: `field__${this.getQuestion.id}`,
        data: this.value,
      });
      console.log(this.selectedOption, this.value);
    },
  },

  created() {
    if (this.question.required && !this.selectedOption) {
      this.$emit("ValidateError", this.getQuestion.id);
    } else {
      this.$emit("ValidateSuccses", this.getQuestion.id);
    }
    if (this.question.question_type == "multiple_choice") {
      this.selectedOption = [];
    }
    if (this.getValueStore) {
      this.selectedOption = this.getValueStore;
    }
  },
};
</script>
