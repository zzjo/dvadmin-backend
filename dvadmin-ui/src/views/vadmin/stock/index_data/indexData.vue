<template>
  <div class="app-container">

    <el-form ref="queryForm" :inline="true" label-width="68px">
      <el-form-item label="筛选时间">
        <el-date-picker
          v-model="dateRange"
          size="small"
          style="width: 240px"
          value-format="yyyy-MM-dd"
          type="daterange"
          range-separator="-"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery"> 搜索 </el-button>
      </el-form-item>
    </el-form>

    <el-transfer
      v-model="value"
      :titles="['未选指数', '已选指数']"
      filterable
      :filter-method="filterMethod"
      filter-placeholder="请输入指数"
      :data="data"
      @change="handleChange"
    ></el-transfer>

    <el-table
      :data="tableData"
      style="width: 100%"
      :default-sort="{prop: 'date', order: 'descending'}"
    >
      <el-table-column
        prop="name"
        label="指数名称"
        width="100"
      >
      </el-table-column>
      <el-table-column
        prop="highDate"
        label="开始时间"
        sortable
        width="100"
      ></el-table-column>
      <el-table-column
        prop="highDateEnd"
        label="结束时间"
        sortable
        width="100"
      ></el-table-column>
      <el-table-column
        prop="highPeriod"
        label="持续天数"
        sortable
        width="100   "
      ></el-table-column>
      <el-table-column
        prop="high"
        label="最大涨幅"
        sortable
        width="100"
      >
      </el-table-column>
      <el-table-column
        prop="lowDate"
        label="开始时间"
        sortable
        width="100"
      >
      </el-table-column>
      <el-table-column
        prop="lowDateEnd"
        label="结束时间"
        sortable
        width="100"
      ></el-table-column>
      <el-table-column
        prop="lowPeriod"
        label="持续天数"
        sortable
        width="100"
      ></el-table-column>
      <el-table-column
        prop="low"
        sortable
        label="最大跌幅"
        width="100"
      >
      </el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="handleEdit(scope.$index, scope.row)"
          >查看</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div id="lineChart" style="width:900px;height:500px"></div>
  </div>

</template>

<script>
import { getIndexData, getTimePeriod, getIndexHistory } from "@/api/vadmin/stock/index";
import * as echarts from "echarts";
export default {
  data() {
    return {
      pinyin: [],
      data: [],
      value: [],
      filterMethod(query, item) {
        return item.pinyin.indexOf(query) > -1;
      },
      // 日期范围
      dateRange: [],
      // 查询参数
      queryParams: {
        ids: [],
        dates: []
      },
      leftvalue: [],
      rightvalue: [],
      tableData: [],
      option: {
        title: {
          text: null,
          left: 0
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross"
          }
        },
        legend: {
          data: ["日K", "MA5", "MA10", "MA20", "MA30"]
        },
        grid: {
          left: "10%",
          right: "10%",
          bottom: "15%"
        },
        xAxis: {
          type: "category",
          data: [],
          scale: true,
          boundaryGap: false,
          axisLine: { onZero: false },
          splitLine: { show: false },
          splitNumber: 20,
          min: "dataMin",
          max: "dataMax"
        },
        yAxis: {
          scale: true,
          splitArea: {
            show: true
          }
        },
        dataZoom: [
          {
            type: "inside",
            start: 50,
            end: 100
          },
          {
            show: true,
            type: "slider",
            top: "90%",
            start: 50,
            end: 100
          }
        ],
        series: [
          {
            name: "日K",
            type: "candlestick",
            data: [],
            itemStyle: {
              color: "#ec0000",
              color0: "#00da3c",
              borderColor: "#8A0000",
              borderColor0: "#008F28"
            },
            markPoint: {
              label: {
                formatter: function(param) {
                  return param != null ? Math.round(param.value) : "";
                }
              },
              data: [
                {
                  name: "XX标点",
                  coord: ["2013/5/31", 2300],
                  value: 2300,
                  itemStyle: {
                    color: "rgb(41,60,85)"
                  }
                },
                {
                  name: "highest value",
                  type: "max",
                  valueDim: "highest"
                },
                {
                  name: "lowest value",
                  type: "min",
                  valueDim: "lowest"
                },
                {
                  name: "average value on close",
                  type: "average",
                  valueDim: "close"
                }
              ],
              tooltip: {
                formatter: function(param) {
                  return param.name + "<br>" + (param.data.coord || "");
                }
              }
            },
            markLine: {
              symbol: ["none", "none"],
              data: [
                [
                  {
                    name: "from lowest to highest",
                    type: "min",
                    valueDim: "lowest",
                    symbol: "circle",
                    symbolSize: 10,
                    label: {
                      show: false
                    },
                    emphasis: {
                      label: {
                        show: false
                      }
                    }
                  },
                  {
                    type: "max",
                    valueDim: "highest",
                    symbol: "circle",
                    symbolSize: 10,
                    label: {
                      show: false
                    },
                    emphasis: {
                      label: {
                        show: false
                      }
                    }
                  }
                ],
                {
                  name: "min line on close",
                  type: "min",
                  valueDim: "close"
                },
                {
                  name: "max line on close",
                  type: "max",
                  valueDim: "close"
                }
              ]
            }
          },
          {
            name: "MA5",
            type: "line",
            data: [],
            smooth: true,
            lineStyle: {
              opacity: 0.5
            }
          },
          {
            name: "MA10",
            type: "line",
            data: [],
            smooth: true,
            lineStyle: {
              opacity: 0.5
            }
          },
          {
            name: "MA20",
            type: "line",
            data: [],
            smooth: true,
            lineStyle: {
              opacity: 0.5
            }
          },
          {
            name: "MA30",
            type: "line",
            data: [],
            smooth: true,
            lineStyle: {
              opacity: 0.5
            }
          }
        ]
      },
      lineChart: null,
      candleData: {
        categoryData: [],
        values: []
      },
      data0: []
    };
  },
  created() {
    this.indexList();
  },
  mounted() {

  },
  methods: {
  // 设置折线图
    getLineChart() {
      this.lineChart = echarts.init(document.getElementById("lineChart"));
      this.lineChart.setOption(this.option);
    },
    splitData(rawData) {
      var categoryData = [];
      var values = [];
      for (var i = 0; i < rawData.length; i++) {
        categoryData.push(rawData[i].splice(0, 1)[0]);
        values.push(rawData[i]);
      }
      return {
        categoryData: categoryData,
        values: values
      };
    },
    calculateMA(dayCount) {
      var result = [];
      for (var i = 0, len = this.candleData.values.length; i < len; i++) {
        if (i < dayCount) {
          result.push("-");
          continue;
        }
        var sum = 0;
        for (var j = 0; j < dayCount; j++) {
          sum += this.candleData.values[i - j][1];
        }
        result.push(sum / dayCount);
      }
      return result;
    },
    handleEdit(index, row) {
      debugger;
      var param = { dates: this.dateRange,
        code: row.code };
      getIndexHistory(param).then(response => {
        this.data0 = response.data;
        this.option.title.text = row.name;
        this.candleData = this.splitData(this.data0);
        console.log(this.candleData);
        this.option.xAxis.data = this.candleData.categoryData;
        this.option.series[0].data = this.candleData.values;
        this.option.series[1].data = this.calculateMA(5);
        this.option.series[2].data = this.calculateMA(10);
        this.option.series[3].data = this.calculateMA(20);
        this.option.series[4].data = this.calculateMA(30);
        this.getLineChart();
      });
      console.log(index, row);
    },
    indexList() {
      getIndexData().then(response => {
        this.pinyin = response.data.code;
        response.data.name.forEach((city, index) => {
          this.data.push({
            label: city,
            key: index,
            pinyin: this.pinyin[index]
          });
        });
      });
    },
    handleQuery() {
      this.queryParams.ids = [];
      this.queryParams.dates = [];
      if (this.rightvalue == null || this.rightvalue.length == 0) {
        this.$alert("请先选择指数", "提示", {
          confirmButtonText: "确定"
        });
      } else {
        this.rightvalue.forEach(key => {
          this.queryParams.ids.push(this.data[key].pinyin);
        });
        this.queryParams.dates = this.dateRange;
        this.loading = true;
        getTimePeriod(this.queryParams).then(response => {
          this.tableData = response.data;
          this.loading = false;
        });
      }
    },
    handleChange(value, direction, movedKeys) {
      if (direction === "right") {
        movedKeys.forEach(key => {
          const index = this.leftvalue.findIndex(item => item === key);
          this.leftvalue.splice(index, 1);
        });
        movedKeys.forEach(key => {
          this.rightvalue.push(key);
        });
      } else {
        movedKeys.forEach(key => {
          const index = this.rightvalue.findIndex(item => item === key);
          this.rightvalue.splice(index, 1);
        });
        movedKeys.forEach(key => {
          this.leftvalue.push(key);
        });
      }
    }
  }
};
</script>

<style></style>
