<template>
  <div class="card mb-3">
    <div
      :class="computedHeaderClasses"
      :style="`${headerColor};`"
      type="button"
      data-bs-toggle="collapse"
      :data-bs-target="`#card-${postfix}`"
      :aria-controls="`card-${postfix}`"
      :aria-expanded="this.visible"
      ref="cardHeader"
      @click="onToggle"
    >
      {{ isExpanded ? showTitle : hiddenTitle }}
    </div>
    <div :id="`card-${postfix}`" :class="computedBodyClasses">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "CollapsingCard",
  props: {
    visible: Boolean,
    showTitle: String,
    hiddenTitle: String,
    center: Boolean,
    headerColor: String,
  },
  data() {
    return {
      isExpanded: this.visible,
      postfix: Math.random().toString(36).substring(7),
    };
  },
  computed: {
    computedHeaderClasses() {
      return [
        "p-2",
        "card-header",
        "text-center",
        this.isExpanded ? "" : "collapsed",
        this.headerColor ? "text-white" : "",
      ];
    },
    computedBodyClasses() {
      let classes = ["card-body", "collapse"];
      if (this.isExpanded) {
        classes.push("show");
        if (this.center) {
          classes.push(
            "d-flex",
            "justify-content-center",
            "align-items-center",
            "text-center"
          );
        }
      }
      return classes;
    },
  },
  methods: {
    onToggle() {
      setTimeout(() => {
        this.isExpanded = this.$refs.cardHeader.ariaExpanded === "true";
      }, 150);
    },
  },
};
</script>
<style lang="scss"></style>
