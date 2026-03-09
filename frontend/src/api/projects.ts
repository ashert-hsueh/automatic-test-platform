import request from '@/utils/request'
import type { ProjectOut, ModuleOut } from '@/types'

export const projectApi = {
    list: () => request.get<ProjectOut[], ProjectOut[]>('/projects'),
    create: (data: { name: string; description?: string; base_url?: string }) =>
        request.post<ProjectOut, ProjectOut>('/projects', data),
    get: (id: number) => request.get<ProjectOut, ProjectOut>(`/projects/${id}`),
    update: (id: number, data: Partial<{ name: string; description: string; base_url: string }>) =>
        request.put<ProjectOut, ProjectOut>(`/projects/${id}`, data),
    remove: (id: number) => request.delete(`/projects/${id}`),

    // Modules
    listModules: (projectId: number) =>
        request.get<ModuleOut[], ModuleOut[]>(`/projects/${projectId}/modules`),
    createModule: (projectId: number, data: { name: string; description?: string }) =>
        request.post<ModuleOut, ModuleOut>(`/projects/${projectId}/modules`, data),
}
