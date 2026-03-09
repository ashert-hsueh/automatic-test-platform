<template>
  <div>
    <!-- 触发任务 -->
    <div class="page-card" style="margin-bottom:20px">
      <div class="page-header">
        <span class="page-title">执行任务</span>
        <el-button type="primary" icon="VideoPlay" @click="showTrigger = true">触发新任务</el-button>
      </div>

      <el-table :data="jobs" v-loading="loading" stripe>
        <el-table-column prop="id"   label="ID"    width="60" />
        <el-table-column prop="name" label="任务名称" min-width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <span :class="`status-badge status-${row.status}`">{{ statusLabel(row.status) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">{{ new Date(row.created_at).toLocaleString('zh-CN') }}</template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewLog(row)">查看日志</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 实时日志面板 -->
    <div v-if="activeJob" class="page-card">
      <div class="page-header">
        <span class="page-title">实时日志 — {{ activeJob.name }}</span>
        <el-button type="info" link @click="activeJob = null">关闭</el-button>
      </div>
      <div class="log-panel" ref="logPanel">
        <div v-for="(line, i) in logLines" :key="i" class="log-line" :class="logClass(line)">
          {{ line }}
        </div>
        <div v-if="wsConnecting" class="log-line log-info">⏳ 正在连接日志流...</div>
      </div>
    </div>

    <!-- 触发任务对话框 -->
    <el-dialog v-model="showTrigger" title="触发测试任务" width="440px">
      <el-form :model="triggerForm" label-width="80px">
        <el-form-item label="任务名称" required>
          <el-input v-model="triggerForm.name" placeholder="例：冒烟测试-20260309" />
        </el-form-item>
        <el-form-item label="项目 ID" required>
          <el-input-number v-model="triggerForm.project_id" :min="1" style="width:100%" />
        </el-form-item>
        <el-form-item label="用例 ID 列表" required>
          <el-input v-model="triggerForm.case_ids_raw" placeholder="输入用例 ID，逗号分隔，如 1,2,3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showTrigger = false">取消</el-button>
        <el-button type="primary" :loading="triggering" @click="submitTrigger">立即执行</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import type { JobOut } from '@/types'

const jobs      = ref<JobOut[]>([])
const loading   = ref(false)
const showTrigger = ref(false)
const triggering  = ref(false)
const activeJob = ref<JobOut | null>(null)
const logLines  = ref<string[]>([])
const wsConnecting = ref(false)
const logPanel  = ref<HTMLElement>()

const triggerForm = reactive({ name: '', project_id: 1, case_ids_raw: '' })

async function fetchJobs() {
  loading.value = true
  try { jobs.value = await request.get('/jobs') } finally { loading.value = false }
}

async function viewLog(job: JobOut) {
  activeJob.value = job
  logLines.value = []
  if (!job.celery_task_id) return
  wsConnecting.value = true

  const protocol = location.protocol === 'https:' ? 'wss' : 'ws'
  const ws = new WebSocket(`${protocol}://${location.host}/api/v1/jobs/ws/${job.celery_task_id}`)

  ws.onopen = () => { wsConnecting.value = false }
  ws.onmessage = async ({ data }) => {
    logLines.value.push(data)
    await nextTick()
    if (logPanel.value) logPanel.value.scrollTop = logPanel.value.scrollHeight
  }
  ws.onclose = () => { wsConnecting.value = false }
}

async function submitTrigger() {
  if (!triggerForm.name.trim()) return ElMessage.warning('请填写任务名称')
  const ids = triggerForm.case_ids_raw
    .split(',').map(s => parseInt(s.trim())).filter(n => !isNaN(n))
  if (!ids.length) return ElMessage.warning('请输入有效的用例 ID')

  triggering.value = true
  try {
    const job = await request.post<JobOut, JobOut>('/jobs', {
      name: triggerForm.name,
      project_id: triggerForm.project_id,
      case_ids: ids,
    })
    ElMessage.success('任务已提交！')
    showTrigger.value = false
    jobs.value.unshift(job)
    viewLog(job)
  } finally { triggering.value = false }
}

const statusLabel = (s: string) =>
  ({ pending: '待执行', running: '执行中', success: '通过', failed: '失败', cancelled: '已取消' }[s] ?? s)

const logClass = (line: string) => {
  if (line.startsWith('[PASS]')) return 'log-pass'
  if (line.startsWith('[FAIL]')) return 'log-fail'
  if (line.startsWith('[DONE]')) return 'log-done'
  if (line.startsWith('[RUN]')) return 'log-run'
  return 'log-info'
}

onMounted(fetchJobs)
</script>

<style scoped>
.log-panel {
  background: #0d1117;
  border-radius: 8px;
  padding: 16px;
  height: 320px;
  overflow-y: auto;
  font-family: 'Fira Code', 'Consolas', monospace;
  font-size: 13px;
  line-height: 1.8;
}
.log-line { white-space: pre-wrap; word-break: break-all; }
.log-pass { color: #3fb950; }
.log-fail { color: #f85149; }
.log-done { color: #e3b341; font-weight: bold; }
.log-run  { color: #58a6ff; }
.log-info { color: #8b949e; }
</style>
