<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside :width="sidebarWidth" class="sidebar">
      <div class="logo">
        <el-icon class="logo-icon"><Monitor /></el-icon>
        <transition name="fade">
          <span v-if="!isCollapsed" class="logo-text">AutoTest</span>
        </transition>
      </div>

      <el-menu
        :default-active="activeRoute"
        :collapse="isCollapsed"
        :collapse-transition="false"
        router
        background-color="#1e2a3a"
        text-color="#a8b2c1"
        active-text-color="#ffffff"
        class="sidebar-menu"
      >
        <el-menu-item v-for="item in menuItems" :key="item.path" :index="item.path">
          <el-icon><component :is="item.icon" /></el-icon>
          <template #title>{{ item.title }}</template>
        </el-menu-item>
      </el-menu>

      <div class="sidebar-collapse" @click="toggleCollapse">
        <el-icon><component :is="isCollapsed ? 'Expand' : 'Fold'" /></el-icon>
      </div>
    </el-aside>

    <!-- 主内容区 -->
    <el-container class="main-container">
      <!-- 顶部 Header -->
      <el-header class="header" height="56px">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <div class="avatar-wrap">
              <el-avatar :size="32" :style="{ background: '#409eff' }">
                {{ auth.user?.username?.charAt(0).toUpperCase() ?? 'U' }}
              </el-avatar>
              <span class="username">{{ auth.user?.username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 页面内容 -->
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const isCollapsed = ref(false)
const sidebarWidth = computed(() => (isCollapsed.value ? '64px' : '220px'))
const activeRoute = computed(() => route.path)
const currentTitle = computed(
  () => menuItems.find((m) => m.path === route.path)?.title ?? '页面',
)

const menuItems = [
  { path: '/dashboard',  title: '仪表盘',  icon: 'Odometer' },
  { path: '/projects',   title: '项目管理', icon: 'FolderOpened' },
  { path: '/testcases',  title: '测试用例', icon: 'Document' },
  { path: '/jobs',       title: '执行任务', icon: 'VideoPlay' },
  { path: '/reports',    title: '测试报告', icon: 'DataAnalysis' },
]

function toggleCollapse() {
  isCollapsed.value = !isCollapsed.value
}

async function handleCommand(cmd: string) {
  if (cmd === 'logout') {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', { type: 'warning' })
    auth.logout()
    ElMessage.success('已退出登录')
    router.push({ name: 'Login' })
  }
}

onMounted(() => auth.fetchMe())
</script>

<style scoped>
.layout-container { height: 100vh; }

.sidebar {
  background: #1e2a3a;
  display: flex;
  flex-direction: column;
  transition: width 0.25s;
  overflow: hidden;
}

.logo {
  height: 56px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 20px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  color: #fff;
  font-weight: 700;
  font-size: 16px;
  white-space: nowrap;
}
.logo-icon { font-size: 22px; color: #409eff; flex-shrink: 0; }

.sidebar-menu { border-right: none; flex: 1; }

.sidebar-collapse {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a8b2c1;
  cursor: pointer;
  border-top: 1px solid rgba(255,255,255,0.08);
  transition: color 0.2s;
  font-size: 18px;
}
.sidebar-collapse:hover { color: #fff; }

.main-container { overflow: hidden; }

.header {
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.header-right { display: flex; align-items: center; gap: 12px; }
.avatar-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
}
.avatar-wrap:hover { background: #f5f7fa; }
.username { font-size: 14px; font-weight: 500; }

.main-content {
  background: var(--bg-page);
  padding: 24px;
  overflow-y: auto;
}
</style>
