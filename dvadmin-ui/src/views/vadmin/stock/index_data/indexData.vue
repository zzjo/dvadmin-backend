<template>
  <div class="app-container">
    <el-form ref="queryForm" :inline="true" label-width="68px">
      <el-form-item label="创建时间">
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
  </div>
</template>

<script>
import { getIndexData, getTimePeriod } from "@/api/vadmin/stock/index";
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
      rightvalue: []
    };
  },
  created() {
    this.indexList();
  },
  methods: {
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
        console.log(this.dateRange);
        // this.loading = true;
        getTimePeriod(this.queryParams).then(response => {
          // this.typeList = response.data.results;
          // this.total = response.data.count;
          // this.loading = false;
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
