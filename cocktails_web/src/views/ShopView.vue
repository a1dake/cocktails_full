<template>ShopView</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "ShopView",
  components: {},
  setup() {
    const MIN_FONT_SIZE = 10;
    const MAX_FONT_SIZE = 22;
    return { MIN_FONT_SIZE, MAX_FONT_SIZE };
  },
  computed: {
    ...mapGetters(["userName", "userUnits", "profile"]),
  },
  methods: {},
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
