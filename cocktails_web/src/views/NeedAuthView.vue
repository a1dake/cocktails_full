<template>
  <div class="need-auth">
    Для просмотра данного ресурса необходимо
    <a :href="authUrl">запросить доступ</a>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "NeedAuthView",
  props: {
    next: {
      type: String,
    },
  },
  computed: {
    ...mapGetters(["settings", "userName"]),
    admins() {
      return (
        this.settings?.["Администраторы, добавляющие пользователей в группы"] ??
        "aigusarov@vtb.ru"
      );
    },
    authUrl() {
      return `mailto:${this.admins}?subject=[hiring] Выдача прав пользователю ${this.userName}.`;
    },
  },
};
</script>

<style lang="scss">
.need-auth {
  width: 100%;
  text-align: center;
  font-size: 1.5rem;
}
</style>
