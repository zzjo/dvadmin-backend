import request from "@/utils/request";

// 查询指数数据列表
export function getIndexData() {
  return request({
    url: "/admin/stock/index/getIndexList",
    method: "get"
  });
}
// 查询指数数据列表
export function getTimePeriod(data) {
  return request({
    url: "/admin/stock/index/getTimePeriod",
    method: "post",
    data: data
  });
}
// 查询指数数据列表
export function getIndexHistory(data) {
  return request({
    url: "/admin/stock/index/getIndexHistory",
    method: "post",
    data: data
  });
}
// 查询新发基金
export function getNewFund(data) {
  return request({
    url: "/admin/stock/index/getNewFund",
    method: "post",
    data: data
  });
}
