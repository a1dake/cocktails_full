import { createRouter, createWebHistory } from "vue-router";
import { useCookies } from "vue3-cookies";

const routes = [
  {
    path: "/",
    name: "Пользователи",
    component: () => import("@/views/UsersView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/recipes",
    name: "Каталог рецептов",
    component: () => import("@/views/RecipesView.vue"),
  },
  {
    path: "/tools",
    name: "Инструменты",
    component: () => import("@/views/ToolsView.vue"),
  },
  {
    path: "/shop",
    name: "Магазин",
    component: () => import("@/views/ShopView.vue"),
  },
  {
    path: "/support",
    name: "Тех. поддержка",
    component: () => import("@/views/SupportView.vue"),
  },
  {
    path: "/statistic",
    name: "Статистика",
    component: () => import("@/views/StatisticView.vue"),
  },
  {
    path: "/points",
    name: "Баллы",
    component: () => import("@/views/PointsView.vue"),
  },
  {
    path: "/ads",
    name: "Реклама",
    component: () => import("@/views/AdsView.vue"),
  },
  {
    path: "/profile",
    name: "Личный кабинет",
    component: () => import("@/views/ProfileView.vue"),
  },
  {
    path: "/auth",
    name: "Авторизация",
    props: (route) => ({ next: route.query.next }),
    component: () => import("@/views/AuthPage.vue"),
  },
  {
    path: "/detail/:type/:id",
    name: "Detail",
    component: () => import("@/views/DetailView.vue"),
    props: (route) => ({
      type: route.params.type,
      id: route.params.id,
    }),
  },
  { path: "/:pathMatch(.*)*", redirect: "/" },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const { cookies } = useCookies();
  const isAuthenticated = cookies.get("authToken");

  if (
    to.matched.some((record) => record.meta.requiresAuth) &&
    !isAuthenticated
  ) {
    next({ name: "Авторизация" });
  } else {
    document.title = `${process.env.VUE_APP_TITLE} | ${to.name}`;
    next();
  }
});

export default router;
