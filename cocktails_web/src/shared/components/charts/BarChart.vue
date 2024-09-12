<template>
  <Bar :plugins="plugins" :options="chartOptions" :data="chartData" />
</template>

<script>
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  Colors,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  Colors
);

export default {
  name: "BarChart",
  components: { Bar },
  props: {
    chartId: {
      type: String,
      default: "bar-chart",
    },
    datasetIdKey: {
      type: String,
      default: "label",
    },
    width: {
      type: Number,
      default: 400,
    },
    height: {
      type: Number,
      default: 250,
    },
    cssClasses: {
      default: "",
      type: String,
    },
    styles: {
      type: Object,
      default: () => {},
    },
    plugins: {
      type: Array,
      default: () => [
        {
          id: "custom_bgcolor",
          beforeDraw: (chart, args, options) => {
            const { ctx } = chart;
            ctx.save();
            ctx.globalCompositeOperation = "destination-over";
            ctx.fillStyle = options.color;
            ctx.fillRect(0, 0, chart.width, chart.height);
            ctx.restore();
          },
          defaults: {
            color: "white",
          },
        },
        {
          id: "bar_labels",
          afterDatasetsDraw: function (chart, args, options) {
            const ctx = chart.ctx;
            ctx.fillStyle = "black";
            const fontSize = 16;
            ctx.font = fontSize + " normal Helvetica Neue";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            const max_data = chart.data.datasets
              .map((i) => i.data)
              .flat()
              .sort((i, j) => j - i)[0];
            if (options.countPercent !== undefined) {
              const mainDataset = isNaN(options.countPercent)
                ? chart.data.datasets.find(
                    (i) => i.label === options.countPercent
                  )
                : null;
              chart.data.datasets.forEach(function (dataset, i) {
                const meta = chart.getDatasetMeta(i);
                if (!meta.hidden) {
                  meta.data.forEach(function (element, index) {
                    if (dataset.data[index] === 0) return;
                    const devider = isNaN(options.countPercent)
                      ? mainDataset.data[index] !== 0
                      : dataset.data[options.countPercent];
                    const position = element.tooltipPosition();
                    const needPercent =
                      dataset.label !== options.countPercent &&
                      devider !== 0 &&
                      index !== options.countPercent &&
                      dataset.data[index] !== 0;
                    let label = needPercent
                      ? `${dataset.data[index]} (${(
                          (dataset.data[index] / devider) *
                          100
                        ).toFixed(0)}%)`
                      : dataset.data[index];
                    if (
                      dataset.data[index] / max_data < 0.2 ||
                      max_data === 0
                    ) {
                      if (options.indexAxis === "x") {
                        if (dataset.data[index])
                          ctx.fillText(
                            label,
                            position.x,
                            position.y - fontSize * 0.4
                          );
                      } else {
                        ctx.fillText(
                          label,
                          position.x + ctx.measureText(label).width,
                          position.y
                        );
                      }
                    } else {
                      if (options.indexAxis === "x") {
                        if (dataset.data[index])
                          ctx.fillText(
                            label,
                            position.x,
                            position.y + fontSize * 0.6
                          );
                      } else {
                        ctx.fillText(
                          label,
                          position.x - ctx.measureText(label).width,
                          position.y
                        );
                      }
                    }
                  });
                }
              });
            } else
              chart.data.datasets.forEach(function (dataset, i) {
                const meta = chart.getDatasetMeta(i);
                if (!meta.hidden) {
                  meta.data.forEach(function (element, index) {
                    const position = element.tooltipPosition();
                    if (dataset.data[index])
                      if (options.indexAxis === "x")
                        ctx.fillText(
                          dataset.data[index],
                          position.x,
                          position.y +
                            (dataset.data[index] / max_data < 0.2 ||
                            max_data === 0
                              ? -fontSize * 0.4
                              : fontSize * 0.6)
                        );
                      else
                        ctx.fillText(
                          dataset.data[index],
                          position.x -
                            ctx.measureText(dataset.data[index]).width,
                          position.y
                        );
                  });
                }
              });
          },
        },
      ],
    },
    chartData: {
      type: Object,
      default: () => ({
        labels: ["1", "2", "3"],
        datasets: [
          {
            label: "My First Dataset",
            data: [65, 59, 80],
            borderWidth: 1,
          },
          {
            label: "My Second Dataset",
            data: [6, 5, 8],
            borderWidth: 1,
          },
        ],
      }),
    },
    chartOptions: {
      type: Object,
      default: () => ({
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            stacked: true,
          },
          y: {
            stacked: true,
          },
        },
        plugins: {
          bar_labels: false,
          legend: {
            display: false,
          },
        },
      }),
    },
  },
};
</script>
