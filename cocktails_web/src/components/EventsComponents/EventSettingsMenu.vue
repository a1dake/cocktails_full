<template>
  <v-menu v-model="isOpened" :close-on-content-click="false" location="bottom">
    <template v-slot:activator="{ props }">
      <v-btn class="btn-primary" v-bind="props"><v-icon>mdi-cog</v-icon></v-btn>
    </template>

    <v-card min-width="300" class="kek">
      <v-card-text>
        <div class="text-center mt-2 fs-5 fw-bold">Настройки календаря</div>

        <v-divider></v-divider>

        <v-select
          label="Отображать при открытии"
          :items="items"
          v-model="selectedView"
          item-title="name"
          item-value="model"
          density="compact"
          variant="outlined"
        ></v-select>
      </v-card-text>
    </v-card>
  </v-menu>
</template>

<script>
import { mapGetters } from "vuex";
import store from "@/store";

export default {
  name: "EventSettingsMenu",
  props: ["opened"],
  emits: ["update:opened"],
  data() {
    return {
      items: [
        { name: "Год", model: "multiMonthYear" },
        { name: "Месяц", model: "dayGridMonth" },
        { name: "Неделя", model: "dayGridWeek" },
        { name: "День", model: "dayGridDay" },
      ],
      defaultView: this.profile?.defaultCalendarView ?? "dayGridWeek",
    };
  },
  computed: {
    ...mapGetters(["profile", "userInfo"]),
    selectedView: {
      get() {
        return this.profile?.defaultCalendarView ?? "dayGridWeek";
      },
      async set(value) {
        await this.save(value, this.profile, this.userInfo?.url);
      },
    },
    isOpened: {
      get() {
        return this.opened;
      },
      set(value) {
        this.$emit("update:opened", value);
      },
    },
  },
  methods: {
    async save(value, profile, url) {
      try {
        this.profile["defaultCalendarView"] = value;
        await store.dispatch("setProfile", { profile, url });
      } catch (error) {
        this.profile["defaultCalendarView"] = this.defaultView;
      }
    },
  },
};
</script>

<style scoped lang="scss">
.btn-primary {
  border: 1px solid #0d6efd;
  border-radius: 0.4em;
  background-color: #0d6efd;
  padding: 0.25rem 0.5rem;
  color: #ffffff;
  font-weight: bold;

  &:hover {
    background-color: #0a58ca;
  }
}
.kek {
  border: none;
  border-radius: 0.8rem !important;
}
</style>
