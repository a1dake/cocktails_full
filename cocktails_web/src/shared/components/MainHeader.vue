<template>
  <div class="topbar">
    <div class="search-bar">
      <img :src="SearchImage" alt="Logo" />
      <!--      <span class="search-icon">{{ SearchImage }}</span>-->
      <input type="text" placeholder="Поиск" />
    </div>
    <div class="profile-btn">
      <img :src="ProfileImage" alt="Logo" style="padding-right: 10px" />
      <!--      <span class="icon">{{ ProfileImage }}</span>-->
      <span class="text">Администратор</span>
    </div>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
import SearchImage from "@/assets/icons/header/search.svg";
import ProfileImage from "@/assets/icons/header/profile.svg";

export default {
  name: "MainHeader",
  emits: ["resize"],
  data() {
    return {
      height: 0,
      SearchImage: SearchImage,
      ProfileImage: ProfileImage,
    };
  },
  updated() {
    if (this.height !== this.$el.clientHeight) {
      this.height = this.$el.clientHeight;
      this.$emit(
        "resize",
        `${
          Math.round(
            this.$el.clientHeight /
              parseFloat(getComputedStyle(document.documentElement).fontSize)
          ) + 1
        }rem`
      );
    }
  },
  computed: {
    ...mapGetters(["appTitle"]),
  },
};
</script>

<style scoped lang="scss">
.topbar {
  grid-area: header;
  height: var(--header-height);
  background-color: #fff;
  display: flex;
  align-items: center;
  padding: 0 20px;
  box-sizing: border-box;
  border-bottom: 1px solid #ddd;
  z-index: 1; // Убедитесь, что верхнее меню выше бокового меню

  .search-bar {
    flex-grow: 1;
    display: flex;
    align-items: center;
    background-color: #f5f7f9;
    padding: 5px 10px;
    border-radius: 5px;
    margin-right: 20px;

    input {
      border: none;
      background: none;
      outline: none;
      flex-grow: 1;
      padding-left: 10px;
      color: #333;
      //font-size: 16px;
    }

    .search-icon {
      color: #a9b1b7;
    }
  }

  .profile-btn {
    display: flex;
    align-items: center;
    background-color: #f5f7f9;
    padding: 10px 15px;
    border-radius: 5px;
    cursor: pointer;

    .icon {
      margin-right: 10px;
    }
  }
}
</style>
