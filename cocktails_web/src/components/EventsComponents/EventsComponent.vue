<template>
  <FullCalendar v-if="userInfo" :options="calendarOptions"> </FullCalendar>
</template>

<script>
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import multiMonthPlugin from "@fullcalendar/multimonth";
import interactionPlugin from "@fullcalendar/interaction";
import { mapGetters } from "vuex";

export default {
  name: "EventsComponent",
  props: ["events"],
  emits: ["handleModal"],
  components: {
    FullCalendar,
  },
  data() {
    return {};
  },
  computed: {
    ...mapGetters(["userInfo", "profile"]),
    calendarOptions() {
      return {
        locale: "ru",
        timeZone: "Europe/Moscow",
        nowIndicator: true,
        editable: true,
        selectable: false,
        selectMirror: false,
        dayMaxEvents: true,
        plugins: [dayGridPlugin, interactionPlugin, multiMonthPlugin],
        initialView: this.profile?.defaultCalendarView ?? "dayGridWeek",
        firstDay: 1,
        headerToolbar: {
          start: "",
          center: "prev title next",
          end: "multiMonthYear,dayGridMonth,dayGridWeek,dayGridDay",
        },
        buttonText: {
          today: "Сегодня",
          year: "год",
          month: "месяц",
          week: "неделя",
          day: "день",
        },
        eventClick: this.eventClickHandler,
        events: this.events,
      };
    },
  },
  methods: {
    async eventClickHandler(item) {
      this.$emit("handleModal", item.event);
    },
  },
};
</script>

<style lang="scss" scoped>
:deep(.fc-col-header .fc-scrollgrid-sync-inner) {
  background-color: #dcdcdc;
}
:deep(.fc-day-sat .fc-col-header-cell-cushion) {
  color: red !important;
}
:deep(.fc-day-sun .fc-col-header-cell-cushion) {
  color: red !important;
}
:deep(.fc-daygrid-day-number) {
  color: black;
}
:deep(.fc-col-header-cell .fc-col-header-cell-cushion) {
  color: black;
}
:deep(.fc-day) {
  border-color: #b2b2b2;
}

:deep(.fc-toolbar.fc-header-toolbar) {
  display: flex;
  justify-content: center;
  align-items: center;
}
:deep(.fc-toolbar-chunk) {
  display: flex;
  align-items: center;
}
:deep(.fc-toolbar-chunk:first-child) {
  margin-right: auto;
}
:deep(.fc-toolbar-chunk:last-child) {
  margin-left: auto;
}

:deep(.fc-button) {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 2.5em;
  line-height: 1;
  font-size: 1.2em;
  padding: 0.5em;
}
</style>
