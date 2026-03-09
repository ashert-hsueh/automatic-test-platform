<template>
  <div class="page-card">
    <div class="page-header">
      <span class="page-title">项目管理</span>
      <el-button type="primary" icon="Plus" @click="showDialog = true">新建项目</el-button>
    </div>

    <el-table :data="projects" v-loading="loading" stripe>
      <el-table-column prop="id"   label="ID"   width="60" />
      <el-table-column prop="name" label="项目名称" min-width="160">
        <template #default="{ row }">
          <span style="font-weight:500; color:#409eff; cursor:pointer" @click="viewProject(row)">{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column prop="base_url"    label="接口地址" show-overflow-tooltip />
      <el-table-column prop="created_at"  label="创建时间" width="180">
        <template #default="{ row }">{{ new Date(row.created_at).toLocaleString('zh-CN') }}</template>
      </el-table-column>
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link size="small" @click="editProject(row)">编辑</el-button>
          <el-button type="danger"  link size="small" @click="removeProject(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新建/编辑对话框 -->
    <el-dialog v-model="showDialog" :title="editTarget ? '编辑项目' : '新建项目'" width="480px" @close="resetForm">
      <el-form :model="form" label-width="80px">
        <el-form-item label="项目名称" required>
          <el-input v-model="form.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="项目描述（可选）" />
        </el-form-item>
        <el-form-item label="接口地址">
          <el-input v-model="form.base_url" placeholder="https://api.example.com" />
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
import { projectApi } from '@/api/projects'
import type { ProjectOut } from '@/types'

const projects = ref<ProjectOut[]>([])
const loading  = ref(false)
const saving   = ref(false)
const showDialog = ref(false)
const editTarget = ref<ProjectOut | null>(null)

const form = reactive({ name: '', description: '', base_url: '' })

async function fetchProjects() {
  loading.value = true
  try { projects.value = await projectApi.list() } finally { loading.value = false }
}

function editProject(row: ProjectOut) {
  editTarget.value = row
  Object.assign(form, { name: row.name, description: row.description ?? '', base_url: row.base_url ?? '' })
  showDialog.value = true
}

function viewProject(row: ProjectOut) {
  ElMessage.info(`项目 ID: ${row.id}，后续跳转模块列表页`)
}

async function removeProject(id: number) {
  await ElMessageBox.confirm('确定删除该项目？此操作不可撤销。', '警告', { type: 'warning' })
  await projectApi.remove(id)
  ElMessage.success('删除成功')
  fetchProjects()
}

async function submitForm() {
  if (!form.name.trim()) return ElMessage.warning('请填写项目名称')
  saving.value = true
  try {
    if (editTarget.value) {
      await projectApi.update(editTarget.value.id, form)
      ElMessage.success('更新成功')
    } else {
      await projectApi.create(form)
      ElMessage.success('创建成功')
    }
    showDialog.value = false
    fetchProjects()
  } finally { saving.value = false }
}

function resetForm() {
  editTarget.value = null
  Object.assign(form, { name: '', description: '', base_url: '' })
}

onMounted(fetchProjects)
</script>
