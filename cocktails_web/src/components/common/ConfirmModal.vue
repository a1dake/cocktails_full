<template>
  <v-dialog :persistent="true" v-model="isOpened" max-width="450px">
    <v-card>
      <v-card-title>{{ title }}</v-card-title>
      <v-card-text>
        <div class="d-flex">
          <v-btn
            color="black"
            variant="tonal"
            :text="cancelButtonText"
            @click="
              $emit('confirm', false);
              isOpened = false;
            "
          />
          <v-spacer />
          <v-btn
            color="primary"
            variant="flat"
            :text="confirmButtonText"
            @click="
              $emit('confirm', true);
              isOpened = false;
            "
          />
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "ConfirmModal",
  props: {
    open: {
      type: Boolean,
      required: true,
    },
    title: {
      type: String,
      default: "Вы подтверждаете действие?",
    },
    confirmButtonText: {
      type: String,
      default: "Подтвердить",
    },
    cancelButtonText: {
      type: String,
      default: "Отмена",
    },
  },
  data() {
    return {
      isOpened: false,
    };
  },
  watch: {
    open(newValue) {
      this.isOpened = newValue;
    },
  },
};
</script>

<style scoped lang="scss"></style>
