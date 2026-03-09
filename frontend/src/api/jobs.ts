import request from '@/utils/request'
import type { TestCaseOut } from '@/types'

export const testcaseApi = {
    list: (moduleId?: number) =>
        request.get<TestCaseOut[], TestCaseOut[]>('/testcases', {
            params: moduleId ? { module_id: moduleId } : {},
        }),
    create: (data: {
        name: string
        module_id: number
        description?: string
        case_type?: string
        priority?: string
        request_config?: Record<string, unknown>
    }) => request.post<TestCaseOut, TestCaseOut>('/testcases', data),
    get: (id: number) => request.get<TestCaseOut, TestCaseOut>(`/testcases/${id}`),
    update: (id: number, data: Partial<TestCaseOut>) =>
        request.put<TestCaseOut, TestCaseOut>(`/testcases/${id}`, data),
    remove: (id: number) => request.delete(`/testcases/${id}`),
}
