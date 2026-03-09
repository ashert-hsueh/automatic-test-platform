import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'

const request = axios.create({
    baseURL: '/api/v1',
    timeout: 30_000,
    headers: { 'Content-Type': 'application/json' },
})

// 请求拦截 — 自动注入 JWT Token
request.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

// 响应拦截 — 统一错误处理
request.interceptors.response.use(
    (response) => response.data,
    (error) => {
        const status = error.response?.status
        const message = error.response?.data?.detail || '网络请求失败'

        if (status === 401) {
            const auth = useAuthStore()
            auth.logout()
            router.push({ name: 'Login' })
            ElMessage.error('登录已过期，请重新登录')
        } else {
            ElMessage.error(message)
        }
        return Promise.reject(error)
    },
)

export default request
