<template>
  <div class="profile">
    <CollapsingCard
      showTitle="Персонификация"
      hiddenTitle="Персонификация"
      class="mb-3"
      visible
    >
      <div class="p-3">
        <span>Размер шрифта:</span>
        <input
          type="number"
          :min="MIN_FONT_SIZE"
          :max="MAX_FONT_SIZE"
          v-model="font"
        />
      </div>
    </CollapsingCard>
    <CollapsingCard
      showTitle="Информация о пользователе"
      hiddenTitle="Информация о пользователе"
      visible
    >
      <div class="p-3">
        <div v-if="userName"><span>Пользователь:</span>{{ userName }}</div>
        <div v-if="$store.state.userInfo?.username">
          <span>Логин:</span>{{ $store.state.userInfo.username }}
        </div>
        <div v-if="$store.state.userInfo?.email">
          <span>Email:</span>{{ $store.state.userInfo.email }}
        </div>
        <div v-if="$store.state.userInfo?.employeeID">
          <span>Идентификатор:</span>{{ $store.state.userInfo.employeeID }}
        </div>
        <div v-if="$store.state.userInfo?.title">
          <span>Должность:</span>{{ $store.state.userInfo.title }}
        </div>
        <div v-if="userUnits?.length">
          <span>Структурное подразделение:</span>
          <p v-for="(unit, index) in userUnits" :key="index">- {{ unit }}</p>
        </div>
        <div>
          <span>Токен:</span>
          {{ $store.state.userInfo?.token ?? "Отсутствует" }}
          <button
            style="padding: 0.1rem 0.4rem; margin-left: 0.2rem"
            type="button"
            class="btn btn-primary"
            @click="updateToken"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-arrow-clockwise"
              viewBox="0 0 16 16"
            >
              <path
                fill-rule="evenodd"
                d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2z"
              ></path>
              <path
                d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466"
              ></path>
            </svg>
          </button>
        </div>
        <div v-if="$store.state.userInfo?.groups?.length">
          <span>Группы пользователя:</span>
          <p
            v-for="(group, index) in $store.state.userInfo.groups"
            :key="index"
          >
            - {{ group }}
          </p>
        </div>
        <div v-else><span>Группы пользователя:</span> Отсутствуют</div>
      </div>
    </CollapsingCard>
  </div>
</template>

<script>
import { request } from "@/http";
import { mapGetters, mapMutations } from "vuex";
import CollapsingCard from "@/shared/components/CollapsingCard.vue";
export default {
  name: "ProfileView",
  components: { CollapsingCard },
  setup() {
    const MIN_FONT_SIZE = 10;
    const MAX_FONT_SIZE = 22;
    return { MIN_FONT_SIZE, MAX_FONT_SIZE };
  },
  computed: {
    ...mapGetters(["userName", "userUnits", "profile"]),
    font: {
      get() {
        return (this.profile?.fontSize ?? "16px").replace("px", "") - 0;
      },
      set(value) {
        value =
          (value < this.MIN_FONT_SIZE
            ? this.MIN_FONT_SIZE
            : value > this.MAX_FONT_SIZE
            ? this.MAX_FONT_SIZE
            : value) + "px";
        this.setFontSize(value);
      },
    },
  },
  methods: {
    ...mapMutations(["setFontSize"]),
    async updateToken() {
      await request(
        this.$store.state.userInfo?.url + "token/",
        "POST",
        "",
        true
      ).then((resp) => {
        if (resp.isOk)
          this.$store.commit("updateUserInfo", {
            ...this.$store.state.userInfo,
            ...resp.data,
          });
      });
    },
  },
};
</script>

<style lang="scss">
.profile {
  padding: var(--body-padding-top) var(--body-padding-side) 0
    var(--body-padding-side);
  .card-body {
    div {
      padding: 0.2rem;
      span {
        font-weight: 600;
        margin-right: 0.2rem;
      }
      p {
        margin: 0;
        margin-left: 2rem;
      }
    }
  }
}
</style>
