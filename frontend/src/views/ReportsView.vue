<template>
  <div class="page-card">
    <div class="page-header">
      <span class="page-title">测试报告</span>
      <el-input v-model="search" placeholder="搜索报告..." style="width:240px" clearable prefix-icon="Search" />
    </div>

    <el-table :data="filteredReports" v-loading="loading" stripe>
      <el-table-column prop="id"       label="ID"    width="60" />
      <el-table-column prop="job_id"   label="任务 ID" width="90" />
      <el-table-column label="通过率" width="200">
        <template #default="{ row }">
          <div class="pass-rate">
            <el-progress
              :percentage="passRate(row)"
              :color="passRate(row) >= 80 ? '#67c23a' : passRate(row) >= 60 ? '#e6a23c' : '#f56c6c'"
              :stroke-width="10"
              style="width:120px"
            />
            <span class="rate-text">{{ passRate(row) }}%</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="用例统计" width="200">
        <template #default="{ row }">
          <el-tag type="success" size="small" style="margin-right:4px">通过 {{ row.passed }}</el-tag>
          <el-tag type="danger"  size="small" style="margin-right:4px">失败 {{ row.failed }}</el-tag>
          <el-tag type="warning" size="small">跳过 {{ row.skipped }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="duration" label="耗时(s)" width="90">
        <template #default="{ row }">{{ row.duration.toFixed(1) }}s</template>
      </el-table-column>
      <el-table-column prop="created_at" label="时间" width="180">
        <template #default="{ row }">{{ new Date(row.created_at).toLocaleString('zh-CN') }}</template>
      </el-table-column>
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link size="small" @click="viewReport(row)">查看报告</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Allure 报告 iframe 预览 -->
    <el-dialog v-model="showReport" title="Allure 报告预览" width="90%" top="4vh">
      <iframe v-if="reportUrl" :src="reportUrl" style="width:100%;height:70vh;border:none;border-radius:8px" />
      <el-empty v-else description="暂无报告文件，请先执行测试任务" />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import request from '@/utils/request'
import type { ReportOut } from '@/types'

const reports   = ref<ReportOut[]>([])
const loading   = ref(false)
const search    = ref('')
const showReport = ref(false)
const reportUrl  = ref('')

const filteredReports = computed(() =>
  reports.value.filter(r => String(r.job_id).includes(search.value))
)

async function fetchReports() {
  loading.value = true
  // 占位数据（真实场景从接口获取）
  reports.value = [
    { id: 1, job_id: 1, total: 20, passed: 18, failed: 2, skipped: 0, duration: 12.3, report_url: null, created_at: new Date().toISOString() },
    { id: 2, job_id: 2, total: 15, passed: 15, failed: 0, skipped: 0, duration: 9.8,  report_url: null, created_at: new Date(Date.now() - 86400000).toISOString() },
  ]
  loading.value = false
}

function passRate(row: ReportOut) {
  if (!row.total) return 0
  return Math.round((row.passed / row.total) * 100)
}

function viewReport(row: ReportOut) {
  reportUrl.value = row.report_url ?? ''
  showReport.value = true
}

onMounted(fetchReports)
</script>

<style scoped>
.pass-rate { display: flex; align-items: center; gap: 8px; }
.rate-text { font-size: 13px; font-weight: 600; color: #606266; white-space: nowrap; }
</style>
