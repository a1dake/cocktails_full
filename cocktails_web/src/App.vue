<template>
  <div>
    <div v-if="needAuth" class="app-root">
      <AuthPage
        style="grid-area: sidebar; width: 100vw"
        class="main-content-container"
      />
    </div>
    <div v-else class="app-root">
      <MainSidebar style="grid-area: sidebar" :sidebarItems="sidebarItems" />
      <MainHeader style="grid-area: header" />
      <div style="grid-area: body" class="main-content-container">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import MainHeader from "@/shared/components/MainHeader.vue";
import MainSidebar from "@/shared/components/MainSidebar.vue";
import { mapGetters } from "vuex";

import AuthPage from "@/views/AuthPage.vue";

import ads from "@/assets/icons/mainSidebar/ads.svg";
import points from "@/assets/icons/mainSidebar/points.svg";
import profile from "@/assets/icons/mainSidebar/profile.svg";
import recipes from "@/assets/icons/mainSidebar/recipes.svg";
import shop from "@/assets/icons/mainSidebar/shop.svg";
import statistic from "@/assets/icons/mainSidebar/statistic.svg";
import support from "@/assets/icons/mainSidebar/support.svg";
import tools from "@/assets/icons/mainSidebar/tools.svg";
import users from "@/assets/icons/mainSidebar/users.svg";

import exitImage from "@/assets/icons/sidebar/exit.svg";
import store from "@/store";

export default {
  name: "App",
  components: {
    MainHeader,
    MainSidebar,
    AuthPage,
  },
  data() {
    return {};
  },
  async beforeMount() {
    await store.dispatch("getUserInfo");
  },
  computed: {
    ...mapGetters(["isAuthenticated", "isAdmin", "isEditor"]),
    needAuth() {
      return !this.isAuthenticated;
    },
    sidebarItems() {
      const items = {
        top: [
          {
            href: "/",
            label: "Пользователи",
            image: users,
          },
          {
            href: "/recipes",
            label: "Каталог рецептов",
            image: recipes,
          },
          {
            href: "/tools",
            label: "Инструменты",
            image: tools,
          },
          {
            href: "/shop",
            label: "Магазин",
            image: shop,
          },
          {
            href: "/support",
            label: "Тех. поддержка",
            image: support,
          },
          {
            href: "/statistic",
            label: "Статистика",
            image: statistic,
          },
          {
            href: "/points",
            label: "Баллы",
            image: points,
          },
          {
            href: "/ads",
            label: "Реклама",
            image: ads,
          },
          {
            href: "/profile",
            label: "Личный кабинет",
            image: profile,
          },
        ],
      };
      if (this.isAuthenticated) {
        items.top.push({
          href: this.logoutUrl,
          label: "Выйти",
          image: exitImage,
        });
      }
      return items;
    },
    portalUrl() {
      return window.location.origin.replace(
        `${window.location.hostname.split(".")[0]}.`,
        ""
      );
    },
    adminUrl() {
      return `${window.location.origin}/admin/`;
    },
    loginUrl() {
      return `${window.location.origin}/admin/login/?next=${window.location.href}`;
    },
    logoutUrl() {
      console.log("isAdmin", this.isAdmin);
      console.log("isEditor", this.isEditor);
      return `${window.location.origin}/admin/logout/?next=${window.location.href}`;
    },
  },
  methods: {
    getRoute: function (name) {
      return this.$router.resolve({
        name: name,
      });
    },
  },
};
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap");

html,
body,
#app,
.app-root {
  width: 100%;
  height: 100%;
  font-family: "Inter", sans-serif !important;
  font-size: 14px !important;
  font-weight: 400 !important;
}
html {
  overflow: hidden;
  overflow-y: hidden !important;
  --sidebar-close-width: 3rem;
  --sidebar-open-width: 14rem;
  --sidebar-padding: 0.25rem;
  --table-header-background: #3176dd;
  --table-header-color: white;
  --body-padding: 1rem 2rem 0 2rem;
  --body-padding-top: 1rem;
  --body-padding-side: 2rem;
}
.app-root {
  --sidebar-width: 250px;
  --header-height: 60px;
  --sidebar-close-width: 3rem;
  --sidebar-open-width: 14rem;
  --sidebar-padding: 0.25rem;
  --table-header-background: #3176dd;
  --table-header-color: white;
  --body-padding: 1rem 2rem 0 2rem;
  --body-padding-top: 1rem;
  --body-padding-side: 2rem;

  display: grid;
  grid-template-rows: var(--header-height) 1fr;
  grid-template-columns: var(--sidebar-width) 1fr;
  grid-template-areas:
    "sidebar header"
    "sidebar body";

  height: 100%;
  width: 100%;

  .main-content-container {
    overflow: auto;
    padding: var(--body-padding);
  }
}
.main-content-container {
  width: 100%;
  height: 100%;
  overflow: auto;
  .pre {
    white-space: pre-wrap;
    white-space: -moz-pre-wrap;
    white-space: -pre-wrap;
    white-space: -o-pre-wrap;
    word-wrap: break-word;
    margin-left: 0.5rem;
  }
  .alert-container {
    position: absolute;
    top: 0;
    width: 100%;
    left: 0;
    display: flex;
    justify-content: center;
    padding: 1rem;
    .alert {
      padding: 1rem 5rem;
    }
  }
}
.v-expansion-panels {
  .v-expansion-panel {
    margin: 0.1rem;
  }
  .v-expansion-panel-text__wrapper {
    padding: 0;
  }
  .v-expansion-panel--active:not(:first-child),
  .v-expansion-panel--active + .v-expansion-panel {
    margin-top: 0;
  }
  .v-expansion-panel--active
    > .v-expansion-panel-title:not(.v-expansion-panel-title--static) {
    min-height: 0;
    background-color: #cfe2ff !important;
    color: #052c65 !important;
  }
  .v-expansion-panel-title {
    background-color: #3176dd !important;
    color: white;
    min-height: 0;
    padding: 0.5rem 2rem;
  }
}
</style>
