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
    <div id="chartLineBox" style="width:1100px;height:700px">
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
          data: []
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
            name: "募集份额",
            min: 0,
            max: 4000,
            interval: 500,
            axisLabel: {
              formatter: "{value}亿"
            }
          },
          {
            type: "value",
            name: "数量",
            min: 0,
            max: 400,
            interval: 50,
            axisLabel: {
              formatter: "{value}只"
            }
          }
        ],
        series: []
      },
      chartLineBox: null
    };
  },
  // 生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
  },
  // 方法集合
  methods: {
    handleQuery() {
      this.queryParams.dates = this.monthrange;
      getNewFund(this.queryParams).then(response => {
        console.log(response);
        debugger;
        this.option.legend.data = response.data.legend;
        this.option.xAxis[0].data = response.data.xAxis;
        this.option.yAxis[0].max = response.data.amount_max;
        this.option.yAxis[1].max = response.data.num_max;
        this.option.series = response.data.series;
        this.chartLineBox = echarts.init(document.getElementById("chartLineBox"));
        console.log(this.option);
        this.chartLineBox.setOption(this.option);
      });
    }
  } // 如果页面有keep-alive缓存功能，这个函数会触发
};
</script>

<style></style>
