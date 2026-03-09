import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { UserOut } from '@/types'

export const useAuthStore = defineStore('auth', () => {
    const token = ref<string | null>(localStorage.getItem('access_token'))
    const user = ref<UserOut | null>(null)

    const isLoggedIn = computed(() => !!token.value)

    function setToken(t: string) {
        token.value = t
        localStorage.setItem('access_token', t)
    }

    function setUser(u: UserOut) {
        user.value = u
    }

    async function login(username: string, password: string) {
        const data = await authApi.login({ username, password })
        setToken(data.access_token)
        setUser(data.user)
        return data
    }

    async function fetchMe() {
        if (!token.value) return
        const me = await authApi.me()
        setUser(me)
    }

    function logout() {
        token.value = null
        user.value = null
        localStorage.removeItem('access_token')
    }

    return { token, user, isLoggedIn, login, fetchMe, logout }
})
