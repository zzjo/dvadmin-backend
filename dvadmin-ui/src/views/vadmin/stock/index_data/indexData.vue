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
        <!-- <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery"> 搜索 </el-button> -->
      </el-form-item>
    </el-form>
    <el-transfer
      v-model="value"
      filterable
      :filter-method="filterMethod"
      filter-placeholder="请输入城市拼音"
      :data="data"
    ></el-transfer>
  </div>
</template>

<script>
import { getIndexData } from "@/api/vadmin/stock/index";
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
      dateRange: []
    };
  },
  created() {
    this.indexList();
  },
  methods: {
    indexList() {
      getIndexData().then(response => {
        this.pinyin = response.data;
        response.data.forEach((city, index) => {
          this.data.push({
            label: city,
            key: index,
            pinyin: this.pinyin[index]
          });
        });
        console.log(response.data);
      });
    }
  }
};
</script>

<style></style>
