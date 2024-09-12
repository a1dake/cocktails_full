<template>
  <v-dialog :persistent="true" v-model="isOpened" max-width="750px">
    <v-card height="500px" max-height="900px">
      <v-card-title>
        <div class="d-flex">
          <span class="fw-bold">
            {{ isCreating ? "Создать событие" : editItem.title }}
          </span>
          <v-spacer />
          <button
            class="btn-close btn-close-grey"
            @click="isOpened = false"
          ></button>
        </div>
      </v-card-title>
      <v-card-text v-if="canEdit || isCreating">
        <div style="border-bottom: #6c757d solid 1px">
          <div class="line-container">
            <div class="first_column">Тип события</div>
            <div class="second_column">
              <VueSelect
                label="name"
                v-bind="$attrs"
                v-model="editItem.extendedProps.type"
                :options="types"
                :filterable="false"
                :searchable="false"
                :multiple="false"
                track-by="id"
                selectedLabel="Выбрано"
                selectLabel=""
                deselectLabel=""
                :closeOnSelect="true"
                placeholder="Выберите тип события..."
              >
                <template #noResult>Не найдено.</template>
              </VueSelect>
            </div>
          </div>
          <div
            class="line-container"
            v-if="editItem.extendedProps.type?.name === 'Отпуск'"
          >
            <div class="first_column">Тип отпуска</div>
            <div class="second_column">
              <VueSelect
                label="name"
                v-bind="$attrs"
                v-model="editItem.extendedProps.vacationType"
                :options="vacationTypes"
                :filterable="false"
                :searchable="false"
                :multiple="false"
                track-by="id"
                selectedLabel="Выбрано"
                selectLabel=""
                deselectLabel=""
                :closeOnSelect="true"
                placeholder="Выберите тип отпуска..."
              >
                <template #noResult>Не найдено.</template>
              </VueSelect>
            </div>
          </div>
          <div class="line-container" v-if="isCreating">
            <div class="first_column">Сотрудник</div>
            <div class="second_column">
              <VueSelect
                label="full_name"
                v-bind="$attrs"
                v-model="editItem.extendedProps.user"
                :options="users"
                :filterable="true"
                :searchable="true"
                :multiple="false"
                track-by="id"
                selectedLabel="Выбрано"
                selectLabel=""
                deselectLabel=""
                :closeOnSelect="true"
                placeholder="Выберите сотрудника..."
              >
                <template #noResult>Не найдено.</template>
              </VueSelect>
            </div>
          </div>
          <div class="line-container">
            <div class="first_column">Передача дел</div>
            <div class="second_column">
              <input
                class="form-control"
                v-model="editItem.extendedProps.transferURL"
                type="url"
              />
            </div>
          </div>
          <div class="line-container">
            <div class="first_column">Доп. информация</div>
            <div class="second_column">
              <textarea
                class="form-control"
                v-model="editItem.extendedProps.description"
              />
            </div>
          </div>
          <div class="line-container">
            <div class="first_column">
              {{
                timeRange !== null &&
                timeRange.length === 2 &&
                timeRange.join("").length >= 11
                  ? `Период (${timeRangeDuration})`
                  : "Период"
              }}
            </div>
            <div class="second_column">
              <Datepicker
                range
                v-model="timeRange"
                ignore-time-validation
                textInput
                showNowButton
                modelType="yyyy-MM-dd"
                format="dd.MM.yyyy"
                locale="ru"
                cancelText="Отмена"
                selectText="Выбрать"
                nowButtonLabel="Сегодня"
                :enable-time-picker="false"
              />
            </div>
          </div>
          <div class="line-container" v-if="intersections.length > 0">
            <div class="first_column">Пересечения</div>
            <div class="second_column">
              <CollapsingCard
                title="Пересечения"
                hiddenTitle="Пересечения"
                :visible="false"
              >
                <div
                  v-for="inter in intersections"
                  :key="inter.id"
                  :title="inter.name"
                >
                  <p>{{ inter.title }} [{{ inter.start }}/{{ inter.end }}]</p>
                </div>
              </CollapsingCard>
            </div>
          </div>
        </div>
      </v-card-text>
      <v-card-text v-else>
        <div style="border-bottom: #6c757d solid 1px">
          <div class="line-container">
            <div class="first_column">Тип события</div>
            <div class="second_column">
              <p>{{ editItem.extendedProps.type.name }}</p>
            </div>
          </div>
          <div
            class="line-container"
            v-if="editItem.extendedProps.type?.name === 'Отпуск'"
          >
            <div class="first_column">Тип отпуска</div>
            <div class="second_column">
              <p>{{ editItem.extendedProps.vacationType.name }}</p>
            </div>
          </div>
          <div class="line-container">
            <div class="first_column">Передача дел</div>
            <div class="second_column">
              <p>{{ editItem.extendedProps.transferURL }}</p>
            </div>
          </div>
          <div class="line-container">
            <div class="first_column">Доп. информация</div>
            <div class="second_column">
              <p>{{ editItem.extendedProps.description }}</p>
            </div>
          </div>
          <div class="line-container">
            <div class="first_column">
              {{
                timeRange !== null &&
                timeRange.length === 2 &&
                timeRange.join("").length >= 11
                  ? `Период (${timeRangeDuration})`
                  : "Период"
              }}
            </div>
            <div class="second_column">
              <p>{{ joinedTimeRange }}</p>
            </div>
          </div>
        </div>
      </v-card-text>
      <v-card-actions v-if="canEdit || isCreating">
        <div class="d-flex w-100" v-if="isCreating">
          <v-spacer />
          <v-btn
            class="action-button"
            variant="tonal"
            text="Создать"
            @click="createUpdateEvent(false)"
          />
          <v-btn
            class="action-button"
            variant="tonal"
            text="Создать Еще"
            @click="createUpdateEvent(true)"
          />
        </div>
        <div class="d-flex w-100" v-else>
          <v-btn
            color="red"
            variant="tonal"
            text="Удалить"
            @click="confirmModal = true"
          />
          <v-spacer />
          <v-btn
            class="action-button"
            variant="flat"
            text="Сохранить"
            @click="createUpdateEvent(false)"
          />
        </div>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <ConfirmModal v-model:open="confirmModal" @confirm="deleteEvent" />
</template>

<script>
import VueSelect from "vue-multiselect";
import Datepicker from "@vuepic/vue-datepicker";
import { request } from "@/http";
import moment from "moment/moment";
import ConfirmModal from "@/components/common/ConfirmModal.vue";
import CollapsingCard from "@/components/common/CollapsingCard.vue";
import { getDurationName } from "@/utils";

export default {
  name: "EventModal",
  components: { ConfirmModal, Datepicker, VueSelect, CollapsingCard },
  props: [
    "open",
    "item",
    "types",
    "users",
    "vacationTypes",
    "canEdit",
    "sameItems",
  ],
  emits: ["updateList", "update:open"],
  data() {
    return {
      editItem: null,
      confirmModal: false,
      timeRange: [],
      intersections: [],
    };
  },
  async created() {
    if (!this.isCreating) {
      this.editItem = structuredClone(this.item);
      if (this.editItem.end.length)
        this.editItem.end = moment(this.editItem.end)
          .subtract(1, "days")
          .format("YYYY-MM-DD");
      this.timeRange = [this.editItem.start, this.editItem.end];
    } else {
      this.editItem = {
        title: "",
        start: "",
        end: "",
        extendedProps: {
          user: null,
          type: null,
          description: "",
          transferURL: "",
          end: "",
          vacationType: null,
        },
        backgroundColor: "",
        textColor: "",
      };
    }
    this.intersections = [];
  },
  computed: {
    timeRangeDuration() {
      if (this.timeRange === null) return 0;
      const duration =
        moment
          .duration(moment(this.timeRange[1]).diff(this.timeRange[0]))
          .asDays() + 1;
      return getDurationName(duration);
    },
    isCreating() {
      return this.item === null;
    },
    joinedTimeRange() {
      return this.timeRange.join(" - ");
    },
    isOpened: {
      get() {
        return this.open;
      },
      set(value) {
        this.$emit("update:open", value);
      },
    },
  },
  methods: {
    async deleteEvent(value) {
      if (!value) return;
      try {
        await request("api/events/", "DELETE", {
          id: this.editItem.id,
        });
        this.$emit("updateList");
        this.isOpened = false;
      } catch (e) {
        alert("Произошла ошибка");
      }
    },
    async createUpdateEvent(isCopy) {
      if (
        !this.editItem.start ||
        !this.editItem.end ||
        !this.editItem.extendedProps.user ||
        !this.editItem.extendedProps.type.id
      ) {
        alert("Заполните все поля");
        return;
      }
      if (
        this.editItem.extendedProps.type.name === "Отпуск" &&
        !this.editItem.extendedProps.vacationType
      ) {
        alert("Выберите тип отпуска");
        return;
      }
      try {
        const vacationType = this.editItem.extendedProps.vacationType
          ? this.editItem.extendedProps.vacationType.id
          : null;
        if (this.isCreating) {
          await request("api/events/", "POST", {
            user: this.editItem.extendedProps.user.id,
            type: this.editItem.extendedProps.type.id,
            description: this.editItem.extendedProps.description,
            transferURL: this.editItem.extendedProps.transferURL,
            start: this.editItem.start,
            end: this.editItem.end,
            vacation_type: vacationType,
          });
        } else {
          await request("api/events/", "PUT", {
            id: this.editItem.id,
            type: this.editItem.extendedProps.type.id,
            description: this.editItem.extendedProps.description,
            transferURL: this.editItem.extendedProps.transferURL,
            start: this.editItem.start,
            end: this.editItem.end,
            vacation_type: vacationType,
          });
        }
        this.$emit("updateList");
        isCopy ? (this.timeRange = ["", ""]) : (this.isOpened = false);
      } catch (e) {
        alert("Произошла ошибка");
      }
    },
    setIntersections() {
      if (this.sameItems.length > 0 && this.timeRange) {
        const startDate = new Date(this.timeRange[0]);
        const endDate = new Date(this.timeRange[1]);

        this.intersections = this.sameItems.filter((i) => {
          const itemStartDate = new Date(i.start);
          const itemEndDate = new Date(i.end);
          return (
            (itemStartDate >= startDate && itemStartDate <= endDate) ||
            (itemEndDate >= startDate && itemEndDate <= endDate)
          );
        });
      } else {
        this.intersections = [];
      }
    },
  },
  watch: {
    timeRange(newValue) {
      this.editItem.start =
        newValue !== null ? (newValue[0] === null ? "" : newValue[0]) : "";
      this.editItem.end =
        newValue !== null ? (newValue[1] === null ? "" : newValue[1]) : "";
      this.setIntersections();
    },
    "editItem.extendedProps.type"() {
      if (this.editItem.extendedProps.type.name !== "Отпуск") {
        this.editItem.extendedProps.vacationType = null;
      }
    },
  },
};
</script>

<style scoped lang="scss">
.line-container {
  width: 100%;
  height: 18%;
  display: flex;
  justify-content: space-between;

  .first_column {
    border: #6c757d solid 1px;
    border-bottom: none;
    padding: 0.5rem;
    width: 30%;
    font-weight: bold;
    font-size: 1.1rem;
  }
  .second_column {
    border: #6c757d solid 1px;
    border-bottom: none;
    border-left: none;
    padding: 0.5rem;
    width: 70%;
    font-size: 1rem;

    textarea,
    input {
      width: 100%;
    }
  }
}
.action-button {
  color: white;
  background-color: #6c757d;
  &:hover {
    background-color: #5c636a;
  }
}

.v-card-text {
  padding: 10px !important;
}
</style>
