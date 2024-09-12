<template>
  <v-data-table
    v-model="selected"
    :headers="headers"
    :items="filteredItems"
    show-select
    class="custom-table"
    hide-default-footer
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title class="custom-toolbar-title">
          {{ tableHeader }}
        </v-toolbar-title>

        <v-btn class="mb-2 mr-2 filter-btn" @click="openFilterModal">
          <v-icon left>mdi-filter</v-icon> Фильтры
        </v-btn>

        <v-btn class="mb-2 create-btn" @click="openModal">
          <v-icon left>mdi-plus</v-icon> Создать
        </v-btn>
      </v-toolbar>

      <v-toolbar flat v-if="tableName === 'Users'">
        <v-tabs v-model="selectedTab" @change="applyTabFilter">
          <v-tab v-for="tab in tabs" :key="tab">
            {{ tab }}
          </v-tab>
        </v-tabs>
      </v-toolbar>

      <v-toolbar flat v-if="tableName === 'Recipe'">
        <v-tabs v-model="selectedTab" @change="applyTabFilter">
          <v-tab v-for="tab in recipeTabs" :key="tab">
            {{ tab }}
          </v-tab>
        </v-tabs>
      </v-toolbar>
    </template>

    <template
      v-slot:header.data-table-select="{ allSelected, selectAll, someSelected }"
    >
      <v-checkbox-btn
        :indeterminate="someSelected && !allSelected"
        :model-value="allSelected"
        color="primary"
        @update:model-value="selectAll(!allSelected)"
      ></v-checkbox-btn>
    </template>

    <template
      v-slot:item.data-table-select="{ internalItem, isSelected, toggleSelect }"
    >
      <v-checkbox-btn
        :model-value="isSelected(internalItem)"
        color="primary"
        @update:model-value="toggleSelect(internalItem)"
      ></v-checkbox-btn>
    </template>

    <template v-slot:item.role="{ item, value }">
      <v-chip :color="getColor(value)">
        {{ value }}
      </v-chip>
    </template>

    <template v-slot:item.actions="{ item }">
      <div class="action-icons">
        <v-icon class="action-icon" size="small" @click="viewDetails(item)">
          mdi-pencil
        </v-icon>
        <v-icon class="action-icon" size="small" @click="deleteItem(item)">
          mdi-delete
        </v-icon>
      </div>
    </template>
  </v-data-table>

  <v-dialog v-model="dialogFilter" max-width="400px">
    <v-card>
      <v-card-title class="text-h5">Фильтры</v-card-title>
      <v-card-text>
        <v-select
          v-model="selectedFilter"
          :items="filterOptions"
          label="Выберите фильтр"
          outlined
          dense
          class="filter-select"
          @change="applyFilter"
        ></v-select>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue-darken-1" variant="text" @click="closeFilterModal">
          Закрыть
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  components: {},
  props: {
    headers: {
      type: Array,
      required: true,
    },
    items: {
      type: Array,
      required: true,
    },
    loaded: {
      type: Boolean,
      required: true,
    },
    tableHeader: {
      type: String,
      required: true,
    },
    tableName: {
      type: String,
      required: true,
    },
    detailName: {
      type: String,
      required: true,
    },
  },
  data: () => ({
    detailView: {
      show: false,
      selectedData: {},
    },
    dialogDelete: false,
    dialogFilter: false,
    editedIndex: -1,
    selected: [],
    selectedFilter: null,
    filterOptions: ["Все", "Админ", "Менеджер", "Пользователь"],

    selectedTab: 0,
    tabs: ["Все", "Пользователи", "Менеджеры"],
    recipeTabs: ["Все", "Заявки"],
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Item" : "Edit Item";
    },
    filteredItems() {
      let items = this.items;

      if (this.tableName === "Users") {
        if (this.selectedTab === 1) {
          items = items.filter((item) => item.role === "Пользователь");
        } else if (this.selectedTab === 2) {
          items = items.filter((item) => item.role === "Менеджер");
        }
      } else if (this.tableName === "Recipe") {
        if (this.selectedTab === 1) {
          items = items.filter((item) => item.bonus === 10);
        }
      }

      if (this.selectedFilter && this.selectedFilter !== "Все") {
        items = items.filter((item) => item.role === this.selectedFilter);
      }

      return items;
    },
  },

  methods: {
    getColor(role) {
      if (role === "Админ") return "red";
      else if (role === "Менеджер") return "orange";
      else return "green";
    },
    viewDetails(item) {
      this.$router.push({
        name: "Detail",
        params: {
          type: this.detailName.toLowerCase(),
          id: item.id,
        },
      });
    },
    openModal() {
      this.dialog = true;
    },
    editItem(item) {
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    deleteItem(item) {
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },
    deleteItemConfirm() {
      this.closeDelete();
    },
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.items[this.editedIndex], this.editedItem);
      } else {
        this.items.push(this.editedItem);
      }
      this.close();
    },
    openDetailView(item) {
      this.detailView.selectedData = item;
      this.detailView.show = true;
    },
    openFilterModal() {
      this.dialogFilter = true;
    },
    closeFilterModal() {
      this.dialogFilter = false;
    },
    applyFilter() {
      this.filteredItems = this.filteredItems();
    },
    applyTabFilter() {
      this.applyFilter();
    },
  },
};
</script>

<style scoped>
.custom-toolbar-title {
  font-size: 24px;
  font-weight: bold;
}

.filter-btn {
  border: 1px solid #c4c4c4;
  background-color: white;
}

.create-btn {
  border: 1px solid black;
  background-color: black;
  color: white;
}

.custom-table .v-data-table-header {
  background-color: #ffffff !important;
}

.custom-table .v-data-table__checkbox {
  margin: 0;
  padding: 0;
}

.custom-table .v-data-table__actions {
  padding: 10px;
}

.custom-table .v-toolbar {
  background-color: #ffffff;
}

.custom-table .v-toolbar__title {
  font-weight: bold;
  color: #4a4a4a;
}

.custom-table .v-chip {
  font-size: 12px;
  font-weight: 500;
  border-radius: 16px;
}

.custom-table .v-chip--red {
  background-color: #ff0000;
}

.custom-table .v-chip--orange {
  background-color: #ff9800;
}

.custom-table .v-chip--green {
  background-color: #4caf50;
}

.custom-table .action-icon {
  color: #9e9e9e;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
}

.custom-table .v-icon:hover {
  color: #4a4a4a;
}

.custom-table .v-data-table__checkbox::before {
  border: 1px solid #c4c4c4;
}

.custom-table .v-data-table__checkbox:checked::before {
  border: 1px solid #3f51b5;
}

.action-icons {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
}

.filter-select {
  margin-right: 16px;
}
</style>
