<template>
  <div class="login-page">
    <div class="login-bg">
      <div class="circle c1"></div>
      <div class="circle c2"></div>
      <div class="circle c3"></div>
    </div>

    <div class="login-card">
      <div class="login-header">
        <div class="brand">
          <el-icon class="brand-icon"><Monitor /></el-icon>
          <span class="brand-name">AutoTest Platform</span>
        </div>
        <p class="brand-desc">自动化测试教学实践平台</p>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" size="large" @submit.prevent="handleLogin">
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="用户名"
            prefix-icon="User"
            clearable
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-button
          type="primary"
          :loading="loading"
          style="width: 100%; margin-top: 8px"
          @click="handleLogin"
        >
          {{ loading ? '登录中...' : '登 录' }}
        </el-button>
      </el-form>

      <div class="login-tip">
        <el-icon><InfoFilled /></el-icon>
        默认账号 <strong>admin</strong> / 密码 <strong>admin123</strong>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'

const router = useRouter()
const auth = useAuthStore()

const formRef = ref<FormInstance>()
const loading = ref(false)
const form = reactive({ username: '', password: '' })

const rules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur', min: 6 }],
}

async function handleLogin() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await auth.login(form.username, form.password)
    ElMessage.success('登录成功 🎉')
    router.push({ name: 'Dashboard' })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #1e2a3a 0%, #2c3e50 50%, #1a252f 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

/* 背景装饰圆 */
.login-bg { position: absolute; inset: 0; pointer-events: none; }
.circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(64, 158, 255, 0.08);
  animation: float 8s ease-in-out infinite;
}
.c1 { width: 400px; height: 400px; top: -100px; left: -100px; animation-delay: 0s; }
.c2 { width: 300px; height: 300px; bottom: -80px; right: -80px; animation-delay: 3s; }
.c3 { width: 200px; height: 200px; top: 50%; left: 60%; animation-delay: 6s; }
@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); }
  50%       { transform: translateY(-20px) scale(1.05); }
}

.login-card {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 16px;
  padding: 48px 40px;
  width: 420px;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.3);
  position: relative;
  z-index: 1;
}

.login-header { text-align: center; margin-bottom: 36px; }
.brand { display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 8px; }
.brand-icon { font-size: 32px; color: #409eff; }
.brand-name { font-size: 22px; font-weight: 700; color: #1e2a3a; }
.brand-desc { color: #909399; font-size: 14px; }

.login-tip {
  margin-top: 20px;
  text-align: center;
  font-size: 12px;
  color: #b0b8c4;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}
.login-tip strong { color: #409eff; }
</style>
