<template>
  <div class="sidebar-wrapper" :class="{ full: full }">
    <div class="logo">
      <img :src="LogoImage" alt="Logo" style="padding-bottom: 10px" />
    </div>
    <div v-for="(items, position) in fullSidebarItems" :key="position">
      <SidebarItem
        v-for="(item, index) in items"
        :key="index"
        :href="item.href"
        :to="item.to"
        :label="item.label"
        @click="item.callback"
        :full="full"
        :image="item.image"
        :style="item.style"
      />
      <slot :name="position" :full="full"></slot>
    </div>
  </div>
</template>

<script>
import SidebarItem from "@/shared/components/SidebarItem.vue";
import LogoImage from "@/assets/icons/logo.png";

export default {
  name: "MainSidebar",
  components: { SidebarItem },
  props: ["sidebarItems"],
  data() {
    return {
      full: true,
      LogoImage: LogoImage,
    };
  },
  computed: {
    fullSidebarItems() {
      if (this.sidebarItems) {
        const items = JSON.parse(JSON.stringify(this.sidebarItems));
        if (!items.bottom) items.bottom = [];
        return items;
      }
      return [];
    },
  },
  methods: {
    triggerFull() {
      this.full = !this.full;
    },
  },
};
</script>

<style scoped lang="scss">
.sidebar-wrapper {
  grid-area: sidebar;
  width: var(--sidebar-width);
  height: 100vh;
  background-color: #f5f7f9;
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;

  &.full {
    width: var(--sidebar-width); // Ширина при полном раскрытии
  }

  .sidebar-item {
    margin-bottom: 10px;
  }
}
</style>
