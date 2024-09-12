<template>
  <component
    :is="to ? 'router-link' : 'a'"
    class="sidebar-menu-item"
    :to="to"
    :href="href"
    :style="label ? '' : 'width: max-content'"
  >
    <div class="sidebar-menu-item-wrapper">
      <div class="sidebar-menu-item-image">
        <div class="sidebar-menu-item-icon">
          <img :src="image" alt="" />
        </div>
      </div>
      <div v-if="full && label" class="sidebar-menu-item-text">
        {{ label }}
      </div>
    </div>
  </component>
</template>
<script>
export default {
  name: "SidebarItem",
  props: {
    full: {
      type: Boolean,
    },
    label: {
      type: String,
      required: false,
    },
    href: {
      type: String,
      required: false,
    },
    to: {
      type: String,
      required: false,
    },
    image: {
      type: String,
    },
  },
};
</script>

<style scoped lang="scss">
.sidebar-menu-item {
  display: flex;
  align-items: center;
  padding: 10px;
  color: #a9b1b7;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
  text-decoration: none;
  position: relative;

  .sidebar-menu-item-wrapper {
    display: flex;
    align-items: center;
    .sidebar-menu-item-image {
      margin-right: 10px;
      .sidebar-menu-item-icon {
        img {
          width: 20px; // Размер иконки
        }
      }
    }
    //.sidebar-menu-item-text {
    //  font-size: 16px;
    //}
  }

  .sidebar-menu-item-title {
    display: none;
    position: absolute;
    left: 100%; // Сдвигаем заголовок вправо
    top: 50%;
    transform: translateY(-50%);
    background-color: #fff;
    padding: 5px 10px;
    border-radius: 5px;
    color: #000;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    white-space: nowrap;
    z-index: 1; // Поверх других элементов

    .sidebar-menu-item-title-text {
      display: flex;
      align-items: center;

      .sidebar-menu-item-title-arrow {
        width: 10px;
        height: 10px;
        background-color: #fff;
        transform: rotate(45deg);
        margin-right: 5px;
      }
    }
  }

  &:hover .sidebar-menu-item-title {
    display: flex;
  }

  &.active,
  &:hover {
    background-color: #fff;
    color: #000;
    border-radius: 5px;
  }
}
</style>
