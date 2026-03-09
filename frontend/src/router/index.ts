import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/login',
            name: 'Login',
            component: () => import('@/views/LoginView.vue'),
            meta: { requiresAuth: false },
        },
        {
            path: '/',
            component: () => import('@/layouts/MainLayout.vue'),
            meta: { requiresAuth: true },
            children: [
                {
                    path: '',
                    redirect: '/dashboard',
                },
                {
                    path: 'dashboard',
                    name: 'Dashboard',
                    component: () => import('@/views/DashboardView.vue'),
                    meta: { title: '仪表盘', icon: 'Odometer' },
                },
                {
                    path: 'projects',
                    name: 'Projects',
                    component: () => import('@/views/ProjectsView.vue'),
                    meta: { title: '项目管理', icon: 'FolderOpened' },
                },
                {
                    path: 'testcases',
                    name: 'TestCases',
                    component: () => import('@/views/TestCasesView.vue'),
                    meta: { title: '测试用例', icon: 'Document' },
                },
                {
                    path: 'jobs',
                    name: 'Jobs',
                    component: () => import('@/views/JobsView.vue'),
                    meta: { title: '执行任务', icon: 'VideoPlay' },
                },
                {
                    path: 'reports',
                    name: 'Reports',
                    component: () => import('@/views/ReportsView.vue'),
                    meta: { title: '测试报告', icon: 'DataAnalysis' },
                },
            ],
        },
        { path: '/:pathMatch(.*)*', redirect: '/' },
    ],
})

// ── 路由守卫 ──────────────────────────────────────────────
router.beforeEach((to) => {
    const auth = useAuthStore()
    if (to.meta.requiresAuth !== false && !auth.isLoggedIn) {
        return { name: 'Login' }
    }
    if (to.name === 'Login' && auth.isLoggedIn) {
        return { name: 'Dashboard' }
    }
})

export default router
