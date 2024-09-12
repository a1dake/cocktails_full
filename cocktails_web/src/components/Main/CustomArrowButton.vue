<template>
  <v-btn icon @click="$router.go(-1)" class="custom-arrow-btn">
    <v-icon>
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M15 6L9 12L15 18"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </v-icon>
  </v-btn>
</template>

<script>
export default {
  name: "CustomArrowButton",
};
</script>

<style scoped>
.custom-arrow-btn {
  background: transparent;
  box-shadow: none;
  border: none;
  padding: 0;
  min-width: auto;
}

.custom-arrow-btn .v-icon {
  margin: 0;
  background: none;
  border: none;
}
</style>
