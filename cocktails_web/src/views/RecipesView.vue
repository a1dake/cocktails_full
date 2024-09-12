<template>
  <MainTable
    :items="items"
    :headers="headers"
    :loaded="loaded"
    :tableHeader="tableHeader"
    :tableName="tableName"
    :detailName="detailName"
  ></MainTable>
</template>

<script>
// import usersData from "@/views/data/users.json";
// import { ref } from "vue";
import EditImage from "@/assets/icons/sidebar/portal.svg";
import DeleteImage from "@/assets/icons/sidebar/exit.svg";
import { request } from "@/http";
import MainTable from "@/components/Main/MainTable.vue";

export default {
  name: "UsersView",
  components: { MainTable },
  data() {
    return {
      EditImage: EditImage,
      DeleteImage: DeleteImage,
      tableName: "Recipe",
      detailName: "recipe",
      items: [],
      filters: {
        is_admin: [true, false],
        is_staff: [true, false],
      },
      loaded: false,
      headers: [
        { title: "ИД", key: "id", width: "10%" },
        { title: "Название коктейля", key: "title", width: "40%" },
        { title: "Кол-во баллов", key: "bonus", width: "10%" },
        { title: "Ингредиентов", key: "ingredient_count", width: "10%" },
        { title: "", key: "actions", width: "20%", sortable: false },
      ],
      tableHeader: "Рецепты",
    };
  },
  setup() {},
  async mounted() {
    try {
      const response = await request(
        "http://109.71.246.251:8000/api/admin/recipe/"
      );
      console.log(response);
      this.loadTable(response);
      console.log(this.items);
    } catch (error) {
      console.error("Ошибка при получении данных:", error);
    }
  },
  methods: {
    loadTable(response) {
      this.items = response.results.map((i) => {
        return {
          id: i.id,
          title: i.title,
          bonus: i.ingredient_count,
          ingredient_count: i.ingredient_count,
        };
      });
      this.loaded = true;
    },
  },
};
</script>

<style lang="scss">
.custom-table {
  table {
    border-collapse: collapse;
    width: 100%;
  }

  th,
  td {
    border-bottom: 1px solid #e0e0e0;
    padding: 10px;
    text-align: left;
  }

  th {
    background-color: #f9f9f9;
    font-weight: normal;
  }

  .table-row {
    display: flex;
    align-items: center;
  }

  .role {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 12px;
    color: white;
  }

  .role.user {
    background-color: #6bc950;
  }

  .role.manager {
    background-color: #ff9e43;
  }

  .avatar {
    border-radius: 50%;
    width: 40px;
    height: 40px;
    object-fit: cover;
    margin-right: 10px;
  }

  .icon {
    width: 16px;
    height: 16px;
    margin: 0 5px;
    cursor: pointer;
  }
}
</style>
