<template>
  <v-container
    fluid
    fill-height
    class="pb-4 detail-container"
    background-color="#f5f5f5"
  >
    <v-row no-gutters>
      <v-col cols="12" class="detail-col">
        <div class="pt-7 header-section">
          <custom-arrow-button class="arrow-button" />
          <h1 class="pr-3 page-title">{{ tableData.title }}</h1>

          <v-chip v-if="tableData.role" :color="getColor(tableData.role)">
            {{ tableData.role }}
          </v-chip>
        </div>

        <v-toolbar flat v-if="type === 'profile'" class="mb-3 tabs-toolbar">
          <v-tabs v-model="selectedTab">
            <v-tab v-for="tab in tabs" :key="tab" class="tab-item">
              {{ tab }}
            </v-tab>
          </v-tabs>
        </v-toolbar>

        <div class="detail-grid">
          <div
            v-for="(item, index) in formattedData"
            :key="index"
            class="grid-item"
          >
            <div class="item-key">{{ item.key }}</div>
            <div class="item-value" v-html="item.formattedValue"></div>
          </div>
        </div>

        <div class="button-container">
          <v-btn @click="handleDelete" class="delete-button">Удалить</v-btn>
          <v-btn @click="handleEdit" class="edit-button">Редактировать</v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { request } from "@/http";
import CustomArrowButton from "@/components/Main/CustomArrowButton.vue";

export default {
  name: "DetailView",
  components: { CustomArrowButton },
  props: {
    type: {
      type: String,
      required: true,
    },
    id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      data: [],
      tableData: {
        role: "",
        title: "",
      },
      tabs: ["Личные данные", "Чат", "Доступ"],
    };
  },
  computed: {
    formattedData() {
      return this.data.map((item) => ({
        key: item.key,
        formattedValue: this.formatValue(item.value),
      }));
    },
  },
  async mounted() {
    try {
      const response = await request(
        `http://109.71.246.251:8000/api/admin/${this.type}/${this.id}/`
      );
      this.tableData.role = this.getRole(response);
      this.tableData.title =
        response.title || `${response.first_name} ${response.last_name}`;

      this.data = this.formatData(response);
    } catch (error) {
      console.error("Ошибка при получении данных:", error);
    }
  },
  methods: {
    getRole(data) {
      console.log(data);
      let role;

      if (data.is_admin === true || data.is_admin === false) {
        if (data.is_admin || data.is_superuser) {
          role = "Админ";
        } else if (data.is_staff) {
          role = "Менеджер";
        } else {
          role = "Пользователь";
        }
        return role;
      }
      return "";
    },
    getColor(role) {
      if (role === "Админ") return "red";
      else if (role === "Менеджер") return "orange";
      else return "green";
    },
    getValueByKey(data, key) {
      const item = data.find((d) => d.key === key);
      return item ? item.value : null;
    },
    formatData(response) {
      const excludedFields = [
        "user_permissions",
        "permissions",
        "groups",
        "jwt_updated_at",
      ];

      return Object.entries(response)
        .filter(([key]) => !excludedFields.includes(key))
        .map(([key, value]) => ({
          key: this.formatKey(key),
          value: this.formatValue(value),
        }));
    },
    formatKey(key) {
      return key.charAt(0).toUpperCase() + key.slice(1);
    },
    formatValue(value) {
      if (Array.isArray(value)) {
        return value.map((item) => item.name).join(", ");
      } else if (typeof value === "object" && value !== null) {
        return Object.entries(value)
          .map(([k, v]) => `${k}: ${v}`)
          .join("<br />");
      }
      return value;
    },
    handleDelete() {
      console.log("Удалить");
    },
    handleEdit() {
      console.log("Редактировать");
    },
  },
};
</script>

<style scoped>
.detail-container {
  height: 110vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  flex-direction: column;
  padding: 20px;
  background-color: white;
}

.detail-col {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: flex-start;
}

.header-section {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  width: 100%;
  justify-content: flex-start;
}

.arrow-button {
  margin-right: 16px;
}

.page-title {
  font-size: 24px;
  color: #333;
  margin: 0;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 0;
  border: 1px solid #ddd;
  border-radius: 8px;
  max-width: 1200px;
  width: 100%;
  background-color: #fff;
}

.grid-item {
  padding: 16px;
  border: 1px solid #ddd;
  box-sizing: border-box;
  background-color: #fff;
}

.item-key {
  font-weight: bold;
  color: #888;
}

.item-value {
  font-size: 16px;
  color: #000;
}

.button-container {
  padding-bottom: 20px;
  display: flex;
  justify-content: flex-start;
  gap: 16px;
  margin-top: 16px;
  width: 100%;
}

.delete-button {
  background-color: #feeeee;
  color: #ff4d4d;
}

.edit-button {
  background-color: #343434;
  color: #fff;
}

/* Tab styles */
.tabs-toolbar {
  background-color: #ffffff; /* Sets the background color of the v-toolbar to white */
  box-shadow: none; /* Remove the default box shadow if present */
}

.tab-item {
  font-weight: bold;
  color: #4a4a4a;
}

.v-tabs {
  background-color: #ffffff; /* Ensures the background of the tabs is white */
}

.v-tab {
  font-size: 16px;
  padding: 12px 16px;
  border-radius: 4px;
}

.v-tab.v-tab--active {
  background-color: #ffffff;
  border-bottom: 2px solid #3f51b5;
  color: #3f51b5;
}

.v-tabs__container {
  border-bottom: 1px solid #ddd;
}
</style>
