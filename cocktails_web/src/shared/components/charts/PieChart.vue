<template>
  <Pie
    :plugins="plugins"
    :options="chartOptions"
    :data="chartData"
  /><!-- :chart-id="chartId"
:dataset-id-key="datasetIdKey"
:plugins="plugins"
:css-classes="cssClasses"
:styles="styles"
:width="width"
:height="height" -->
</template>
<script>
import { Pie } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  SubTitle,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
  Colors,
} from "chart.js";

ChartJS.register(
  Title,
  SubTitle,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
  Colors
);

export default {
  name: "PieChart",
  components: { Pie },
  props: {
    chartId: {
      type: String,
      default: "doughnut-chart",
    },
    datasetIdKey: {
      type: String,
      default: "label",
    },
    width: {
      type: Number,
      default: 300,
    },
    height: {
      type: Number,
      default: 300,
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
          id: "data_labels",
          afterDatasetsDraw: function (chart) {
            var ctx = chart.ctx;
            var centerX = chart.chartArea.left + chart.chartArea.width / 2;
            var centerY = chart.chartArea.top + chart.chartArea.height / 2;
            ctx.fillStyle = "black";
            var fontSize = 16;
            ctx.font = fontSize + " normal Helvetica Neue";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            chart.data.datasets.forEach(function (dataset, i) {
              var meta = chart.getDatasetMeta(i);
              if (!meta.hidden) {
                var sumData = dataset.data.reduce((i, j) => i + j);
                if (sumData == 0)
                  ctx.fillText("Все значения нулевые", centerX, centerY);
                else {
                  meta.data.forEach(function (element, index) {
                    if (Math.abs(element.endAngle - element.startAngle) > 0.1) {
                      var percent = (dataset.data[index] / sumData) * 100;
                      if (percent > 2) {
                        var position = element.tooltipPosition();
                        ctx.fillText(
                          percent.toFixed(0) + "%",
                          position.x,
                          position.y
                        );
                        // ctx.fillText(
                        //   dataset.data[index],
                        //   centerX + (position.x - centerX) * 1.2,
                        //   centerY + (position.y - centerY) * 1.2
                        // );
                      }
                    }
                  });
                }
              }
            });
          },
        },
      ],
    },
    chartData: {
      type: Object,
      default() {
        const data = {
          labels: ["VueJs", "EmberJs", "ReactJs", "AngularJs"],
          datasets: [
            {
              backgroundColor: ["#41B883", "#E46651", "#00D8FF", "#DD1B16"],
              data: [40, 20, 80, 10],
            },
          ],
        };
        return data;
      },
    },
    chartOptions: {
      type: Object,
      default: () => ({
        responsive: true,
        maintainAspectRatio: false,
      }),
    },
  },
};
</script>
