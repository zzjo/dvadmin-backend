<template>
  <div class="app-container">
    <el-form ref="queryForm" :inline="true" label-width="68px">
      <el-form-item label="筛选时间">
        <el-date-picker
          v-model="monthrange"
          size="small"
          style="width: 240px"
          value-format="yyyy-MM"
          type="monthrange"
          range-separator="至"
          start-placeholder="开始月份"
          end-placeholder="结束月份"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery"> 搜索 </el-button>
      </el-form-item>
    </el-form>
    <div id="chartLineBox" style="width:900px;height:500px">
    </div>
  </div>
</template>

<script>
import { getNewFund } from "@/api/vadmin/stock/index";
import * as echarts from "echarts";

export default {
  // 定义属性
  data() {
    return {
      monthrange: [],
      queryParams: {
        dates: []
      },
      option: {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            crossStyle: {
              color: "#999"
            }
          }
        },
        toolbox: {
          feature: {
            dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ["line", "bar"] },
            restore: { show: true },
            saveAsImage: { show: true }
          }
        },
        legend: {
          data: ["Evaporation", "Precipitation", "Temperature"]
        },
        xAxis: [
          {
            type: "category",
            data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            axisPointer: {
              type: "shadow"
            }
          }
        ],
        yAxis: [
          {
            type: "value",
            name: "Precipitation",
            min: 0,
            max: 250,
            interval: 50,
            axisLabel: {
              formatter: "{value} ml"
            }
          },
          {
            type: "value",
            name: "Temperature",
            min: 0,
            max: 25,
            interval: 5,
            axisLabel: {
              formatter: "{value} °C"
            }
          }
        ],
        series: [
          {
            name: "Evaporation",
            type: "bar",
            data: [
              2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3
            ]
          },
          {
            name: "Precipitation",
            type: "bar",
            data: [
              2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3
            ]
          },
          {
            name: "Temperature",
            type: "line",
            yAxisIndex: 1,
            data: [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2]
          }
        ]
      },
      chartLineBox: null
    };
  },
  // 生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {

  },
  // 方法集合
  methods: {
    getChartLineBox() {
      this.chartLineBox = echarts.init(document.getElementById("chartLineBox"));
      this.chartLineBox.setOption(this.option);
    },
    handleQuery() {
      this.queryParams.dates = this.monthrange;
      getNewFund(this.queryParams).then(response => {
        console.log(response);
      });
    }
  } // 如果页面有keep-alive缓存功能，这个函数会触发
};
</script>

<style></style>
