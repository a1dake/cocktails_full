<template>
  <div class="login-container">
    <div class="login-box">
      <img :src="LogoImage" alt="Mr. Barmister" class="logo" />
      <h2>Вход</h2>
      <form @submit.prevent="submitForm">
        <div class="input-group">
          <label for="email">Почта</label>
          <input
            v-model="email"
            type="text"
            id="email"
            required
            placeholder="admin@gmail.com"
          />
        </div>
        <div class="input-group">
          <label for="password">Пароль</label>
          <input
            v-model="password"
            type="password"
            id="password"
            required
            placeholder="********"
          />
        </div>
        <button type="submit" class="login-button">Войти</button>
      </form>
    </div>
  </div>
</template>

<script>
import LogoImage from "@/assets/icons/logo.png";
import { mapActions } from "vuex";

export default {
  data() {
    return {
      email: "",
      password: "",
      LogoImage: LogoImage,
    };
  },
  methods: {
    ...mapActions(["login"]),
    async submitForm() {
      try {
        await this.login({ username: this.email, password: this.password });
        this.$router.push({ name: "Пользователи" });
      } catch (err) {
        console.error("Login error:", err);
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.login-box {
  background-color: white;
  padding: 40px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  width: 350px;
  text-align: center;
}

.logo {
  width: 100px;
  margin-bottom: 20px;
}

h2 {
  font-family: "Arial", sans-serif;
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 15px;
  text-align: left;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
  font-size: 14px;
  color: #333;
}

.input-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.login-button {
  background-color: #333;
  color: white;
  padding: 10px;
  width: 100%;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.login-button:hover {
  background-color: #555;
}
</style>
