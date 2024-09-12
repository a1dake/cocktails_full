import { createStore } from "vuex";
import { request, requestAuth } from "@/http.js";
import { useCookies } from "vue3-cookies";

export default createStore({
  state() {
    const { cookies } = useCookies();
    let userInfo = null;
    try {
      const userInfoLocalStorage = localStorage.getItem("userInfo");
      userInfo = userInfoLocalStorage ? JSON.parse(userInfoLocalStorage) : null;
    } catch (error) {
      console.error("Error parsing userInfo from localStorage:", error);
    }
    return {
      userInfo,
      authToken: cookies.get("authToken") ?? null,
      appTitle: process.env.VUE_APP_TITLE,
    };
  },
  getters: {
    isAuthenticated(state) {
      return !!state.authToken;
    },
    isAdmin(state) {
      return state.userInfo?.is_admin || state.userInfo?.is_superuser;
    },
    isEditor(state) {
      return (
        state.userInfo?.is_admin ||
        state.userInfo?.is_superuser ||
        state.userInfo?.is_staff
      );
    },
    userInfo(state) {
      return state.userInfo ?? null;
    },
    userName(state) {
      return state.userInfo?.full_name ?? "Гость";
    },
    appTitle(state) {
      return state.appTitle;
    },
    // Права
    canAddUser(state) {
      return state.userInfo?.user_permissions?.includes(93) ?? false;
    },
    canViewUser(state) {
      return state.userInfo?.user_permissions?.includes(96) ?? false;
    },
    canAddRecipe(state) {
      return state.userInfo?.user_permissions?.includes(129) ?? false;
    },
    canViewRecipe(state) {
      return state.userInfo?.user_permissions?.includes(132) ?? false;
    },
    canAddTool(state) {
      return state.userInfo?.user_permissions?.includes(125) ?? false;
    },
    canViewTool(state) {
      return state.userInfo?.user_permissions?.includes(128) ?? false;
    },
    canAddGoods(state) {
      return state.userInfo?.user_permissions?.includes(133) ?? false;
    },
    canViewGoods(state) {
      return state.userInfo?.user_permissions?.includes(136) ?? false;
    },
    canAddAds(state) {
      return state.userInfo?.user_permissions?.includes(65) ?? false;
    },
    canViewAds(state) {
      return state.userInfo?.user_permissions?.includes(68) ?? false;
    },
    canAddDocument(state) {
      return state.userInfo?.user_permissions?.includes(73) ?? false;
    },
    canViewDocument(state) {
      return state.userInfo?.user_permissions?.includes(76) ?? false;
    },
    canAddFaq(state) {
      return state.userInfo?.user_permissions?.includes(77) ?? false;
    },
    canViewFaq(state) {
      return state.userInfo?.user_permissions?.includes(80) ?? false;
    },
    canAddPoint(state) {
      return state.userInfo?.user_permissions?.includes(105) ?? false;
    },
    canViewPoint(state) {
      return state.userInfo?.user_permissions?.includes(108) ?? false;
    },
  },
  mutations: {
    setUserInfo(state, userData) {
      state.userInfo = userData;
      try {
        localStorage.setItem("userInfo", JSON.stringify(userData));
      } catch (error) {
        console.error("Error saving userInfo to localStorage:", error);
      }
    },
    setAuthToken(state, token) {
      state.authToken = token;
      const { cookies } = useCookies();
      cookies.set("authToken", token, "1d");
    },
    clearAuthData(state) {
      state.userInfo = null;
      state.authToken = null;
      const { cookies } = useCookies();
      localStorage.removeItem("userInfo");
      cookies.remove("authToken");
    },
  },
  actions: {
    async getUserInfo({ state, commit }) {
      const response = await request(
        "http://109.71.246.251:8000/api/admin/profile/"
      );
      if (response.email) {
        if (state.userInfo?.email !== response.email) {
          commit("updateUserInfo", response);
        }
      }
    },
    async login({ commit }, credentials) {
      try {
        const response = await requestAuth(
          "http://109.71.246.251:8000/api/admin/auth/sign-in/",
          "POST",
          credentials
        );
        if (response.token) {
          commit("setAuthToken", response.token);
          commit("setUserInfo", response.user);
        }
      } catch (error) {
        console.error("Login failed:", error);
        throw error;
      }
    },
    async fetchUserInfo({ commit }) {
      try {
        const response = await request(
          "http://109.71.246.251:8000/api/admin/profile/"
        );
        if (response.email) {
          commit("setUserInfo", response);
        } else {
          commit("clearAuthData");
        }
      } catch (error) {
        console.error("Failed to fetch user info:", error);
        commit("clearAuthData");
      }
    },
    logout({ commit }) {
      commit("clearAuthData");
    },
  },
});
