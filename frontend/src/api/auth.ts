import request from '@/utils/request'
import type { TokenOut, UserOut } from '@/types'

export const authApi = {
    login: (data: { username: string; password: string }) =>
        request.post<TokenOut, TokenOut>('/auth/login', data),

    register: (data: {
        username: string
        email: string
        password: string
        full_name?: string
        role?: string
    }) => request.post<UserOut, UserOut>('/auth/register', data),

    me: () => request.get<UserOut, UserOut>('/auth/me'),
}
