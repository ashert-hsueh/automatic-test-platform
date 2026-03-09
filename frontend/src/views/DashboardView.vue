<template>
  <div>
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stat-row">
      <el-col v-for="s in stats" :key="s.label" :span="6">
        <div class="stat-card" :style="{ borderTop: `4px solid ${s.color}` }">
          <div class="stat-icon" :style="{ background: s.color + '18', color: s.color }">
            <el-icon :size="22"><component :is="s.icon" /></el-icon>
          </div>
          <div class="stat-body">
            <div class="stat-value">{{ s.value }}</div>
            <div class="stat-label">{{ s.label }}</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 图表区 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="16">
        <div class="page-card">
          <div class="page-header">
            <span class="page-title">近 7 天执行趋势</span>
          </div>
          <v-chart :option="lineOption" style="height: 280px" autoresize />
        </div>
      </el-col>
      <el-col :span="8">
        <div class="page-card">
          <div class="page-header">
            <span class="page-title">用例状态分布</span>
          </div>
          <v-chart :option="pieOption" style="height: 280px" autoresize />
        </div>
      </el-col>
    </el-row>

    <!-- 最近任务 -->
    <div class="page-card" style="margin-top: 20px">
      <div class="page-header">
        <span class="page-title">最近执行任务</span>
        <el-button type="primary" link @click="$router.push('/jobs')">查看全部 →</el-button>
      </div>
      <el-table :data="recentJobs" size="small" stripe>
        <el-table-column prop="name" label="任务名称" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <span :class="`status-badge status-${row.status}`">{{ statusLabel(row.status) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">{{ new Date(row.created_at).toLocaleString('zh-CN') }}</template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, LineChart, PieChart, GridComponent, TooltipComponent, LegendComponent])

const stats = [
  { label: '项目总数',  value: 8,   icon: 'FolderOpened', color: '#409eff' },
  { label: '用例总数',  value: 136, icon: 'Document',      color: '#67c23a' },
  { label: '今日执行',  value: 24,  icon: 'VideoPlay',     color: '#e6a23c' },
  { label: '通过率',    value: '91%', icon: 'DataAnalysis', color: '#f56c6c' },
]

const days = ['3-3', '3-4', '3-5', '3-6', '3-7', '3-8', '3-9']
const lineOption = {
  tooltip: { trigger: 'axis' },
  legend: { data: ['通过', '失败'] },
  grid: { left: 40, right: 20, top: 40, bottom: 30 },
  xAxis: { type: 'category', data: days },
  yAxis: { type: 'value' },
  series: [
    { name: '通过', type: 'line', smooth: true, data: [18, 22, 30, 28, 35, 40, 42], itemStyle: { color: '#67c23a' }, areaStyle: { opacity: 0.1 } },
    { name: '失败', type: 'line', smooth: true, data: [3,  2,  4,  2,  3,  5,  2 ], itemStyle: { color: '#f56c6c' }, areaStyle: { opacity: 0.1 } },
  ],
}

const pieOption = {
  tooltip: { trigger: 'item' },
  legend: { orient: 'vertical', left: 'left' },
  series: [{
    type: 'pie', radius: ['40%', '70%'],
    data: [
      { value: 92, name: '通过', itemStyle: { color: '#67c23a' } },
      { value: 8,  name: '失败', itemStyle: { color: '#f56c6c' } },
      { value: 3,  name: '跳过', itemStyle: { color: '#e6a23c' } },
    ],
    label: { formatter: '{b}: {d}%' },
  }],
}

const recentJobs = ref([
  { name: '用户模块回归测试', status: 'success', created_at: new Date(Date.now() - 3_600_000).toISOString() },
  { name: '订单接口全量测试', status: 'failed',  created_at: new Date(Date.now() - 7_200_000).toISOString() },
  { name: '登录功能冒烟测试', status: 'running', created_at: new Date(Date.now() - 300_000).toISOString() },
])

const statusLabel = (s: string) => ({ pending: '待执行', running: '执行中', success: '通过', failed: '失败', cancelled: '已取消' }[s] ?? s)
</script>

<style scoped>
.stat-row { margin-bottom: 0; }
.stat-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
.stat-icon {
  width: 48px; height: 48px;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.stat-value { font-size: 26px; font-weight: 700; line-height: 1.2; }
.stat-label { font-size: 13px; color: #909399; margin-top: 4px; }
</style>
