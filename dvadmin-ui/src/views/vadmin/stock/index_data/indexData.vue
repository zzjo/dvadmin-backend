<template>
  <div class="app-container">
    <el-form v-show="showSearch" ref="queryForm" :model="queryParams" :inline="true" label-width="68px">
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
      filterable
      :filter-method="filterMethod"
      filter-placeholder="请输入城市拼音"
      :data="data"
    ></el-transfer>
  </div>
</template>

<script></script>

<style></style>
