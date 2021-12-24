import request from "@/utils/request";

// 查询指数数据列表
export function getIndexData() {
  return request({
    url: "/admin/stock/index/getIndexList",
    method: "get"
  });
}
