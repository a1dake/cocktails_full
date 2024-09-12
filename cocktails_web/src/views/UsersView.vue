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
      tableName: "Users",
      detailName: "profile",
      items: [],
      filters: {
        is_admin: [true, false],
        is_staff: [true, false],
      },
      loaded: false,
      headers: [
        { title: "ИД", key: "id", width: "10%" },
        { title: "Роль", key: "role", width: "10%" },
        { title: "Имя и Фамилия", key: "fio", width: "30%" },
        { title: "Телефон", key: "phone", width: "20%" },
        { title: "Эл. почта", key: "email", width: "20%" },
        { title: "", key: "actions", width: "20%", sortable: false },
      ],
      tableHeader: "Пользователи",
    };
  },
  setup() {},
  async mounted() {
    try {
      const response = await request(
        "http://109.71.246.251:8000/api/admin/profile/"
      );
      this.loadTable(response);
    } catch (error) {
      console.error("Ошибка при получении данных:", error);
    }
  },
  methods: {
    loadTable(response) {
      this.items = response.map((i, index) => {
        return {
          index: index + 1,
          id: i.id,
          fio: this.getFio(i),
          email: i.email,
          phone: i.phone,
          role: this.getRole(i),
          other: {
            avatar: i.avatar,
            date_of_birth: i.date_of_birth,
            gender: i.gender,
            groups: i.groups,
            is_active: i.is_active,
            is_admin: i.is_admin,
            is_staff: i.is_staff,
            username: i.username,
          },
        };
      });
      this.loaded = true;
    },
    getFio(data) {
      return `${data.first_name} ${data.last_name}`;
    },
    getRole(data) {
      let role;

      if (data.is_admin || data.is_superuser) {
        role = "Админ";
      } else if (data.is_staff) {
        role = "Менеджер";
      } else {
        role = "Пользователь";
      }
      return role;
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
