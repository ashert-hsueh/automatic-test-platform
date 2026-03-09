<template>
  <div class="page-card">
    <div class="page-header">
      <span class="page-title">测试用例</span>
      <el-button type="primary" icon="Plus" @click="showDialog = true">新建用例</el-button>
    </div>

    <el-table :data="cases" v-loading="loading" stripe>
      <el-table-column prop="id"   label="ID"  width="60" />
      <el-table-column prop="name" label="用例名称" min-width="200" show-overflow-tooltip />
      <el-table-column prop="case_type" label="类型" width="90">
        <template #default="{ row }">
          <el-tag :type="typeColor(row.case_type)" size="small">{{ row.case_type.toUpperCase() }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="priority" label="优先级" width="80">
        <template #default="{ row }">
          <el-tag :type="priorityColor(row.priority)" size="small">{{ row.priority }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">{{ new Date(row.created_at).toLocaleString('zh-CN') }}</template>
      </el-table-column>
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link size="small" @click="editCase(row)">编辑</el-button>
          <el-button type="danger"  link size="small" @click="removeCase(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="showDialog" :title="editTarget ? '编辑用例' : '新建用例'" width="520px" @close="resetForm">
      <el-form :model="form" label-width="90px">
        <el-form-item label="用例名称" required>
          <el-input v-model="form.name" placeholder="请输入用例名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="用例类型">
          <el-select v-model="form.case_type">
            <el-option label="API 接口" value="api" />
            <el-option label="UI 自动化" value="ui" />
            <el-option label="性能测试" value="perf" />
          </el-select>
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="form.priority">
            <el-option v-for="p in ['P0','P1','P2','P3']" :key="p" :label="p" :value="p" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属模块" required>
          <el-input-number v-model="form.module_id" :min="1" placeholder="模块 ID" style="width:100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="submitForm">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { testcaseApi } from '@/api/jobs'
import type { TestCaseOut } from '@/types'

// 用 jobs.ts 里重新导出 testcaseApi
const { list, create, update, remove } = testcaseApi ?? {}

const cases = ref<TestCaseOut[]>([])
const loading  = ref(false)
const saving   = ref(false)
const showDialog = ref(false)
const editTarget = ref<TestCaseOut | null>(null)

const form = reactive({ name: '', description: '', case_type: 'api', priority: 'P2', module_id: 1 })

async function fetchCases() {
  loading.value = true
  try { cases.value = await testcaseApi.list() } finally { loading.value = false }
}

function editCase(row: TestCaseOut) {
  editTarget.value = row
  Object.assign(form, { name: row.name, description: row.description ?? '', case_type: row.case_type, priority: row.priority, module_id: row.module_id })
  showDialog.value = true
}

async function removeCase(id: number) {
  await ElMessageBox.confirm('确定删除该用例？', '警告', { type: 'warning' })
  await testcaseApi.remove(id)
  ElMessage.success('删除成功')
  fetchCases()
}

async function submitForm() {
  if (!form.name.trim()) return ElMessage.warning('请填写用例名称')
  saving.value = true
  try {
    editTarget.value
      ? await testcaseApi.update(editTarget.value.id, form)
      : await testcaseApi.create(form)
    ElMessage.success(editTarget.value ? '更新成功' : '创建成功')
    showDialog.value = false
    fetchCases()
  } finally { saving.value = false }
}

function resetForm() {
  editTarget.value = null
  Object.assign(form, { name: '', description: '', case_type: 'api', priority: 'P2', module_id: 1 })
}

const typeColor = (t: string) => ({ api: 'primary', ui: 'success', perf: 'warning' }[t] ?? '')
const priorityColor = (p: string) => ({ P0: 'danger', P1: 'warning', P2: '', P3: 'info' }[p] ?? '')

onMounted(fetchCases)
</script>
