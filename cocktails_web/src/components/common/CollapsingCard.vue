<template>
  <div class="card">
    <div
      :class="headerClasses"
      type="button"
      data-bs-toggle="collapse"
      :data-bs-target="`#card-${postfix}`"
      :aria-controls="`card-${postfix}`"
      :aria-expanded="this.visible"
      ref="cardHeader"
      @click="onToggle"
    >
      <slot name="header">{{ isExpanded ? title : hiddenTitle }}</slot>
    </div>
    <div ref="cardBody" :id="`card-${postfix}`" :class="initialBodyClasses">
      <slot></slot>
    </div>
  </div>
</template>
<script>
import { Collapse } from "bootstrap";
export default {
  name: "CollapsingCard",
  props: {
    visible: Boolean,
    colored: Boolean,
    title: String,
    hiddenTitle: {
      type: String,
      default(rawProps) {
        return rawProps.title;
      },
    },
  },
  mounted() {
    this.collapseElement = new Collapse(this.$refs.cardBody, {
      toggle: false,
    });
    const that = this;
    this.$refs.cardBody.addEventListener(
      "shown.bs.collapse",
      () => (that.isExpanded = true)
    );
    this.$refs.cardBody.addEventListener(
      "hidden.bs.collapse",
      () => (that.isExpanded = false)
    );
  },
  data() {
    return {
      collapseElement: null,
      isExpanded: this.visible,
      initialHeaderClasses: [
        "card-header",
        "text-center",
        this.visible ? "" : "collapsed",
      ],
      initialBodyClasses: ["card-body", "collapse", this.visible ? "show" : ""],
      postfix: Math.random().toString(36).substring(7),
    };
  },
  computed: {
    headerClasses() {
      let colorClass = this.isExpanded ? "bg-lightblue" : "bg-blue";
      return [...this.initialHeaderClasses, colorClass];
    },
  },
  methods: {
    onToggle() {
      this.collapseElement.toggle();
    },
  },
};
</script>
<style lang="scss">
.bg-blue {
  background-color: #3176dd !important;
  color: #fff;
}
.bg-lightblue {
  background-color: #cfe2ff !important;
  color: #052c65 !important;
}
</style>
