// 全局类型定义

export interface UserOut {
    id: number
    username: string
    email: string
    full_name: string | null
    role: 'admin' | 'mentor' | 'intern'
    is_active: boolean
    created_at: string
}

export interface TokenOut {
    access_token: string
    token_type: string
    user: UserOut
}

export interface ProjectOut {
    id: number
    name: string
    description: string | null
    base_url: string | null
    owner_id: number
    created_at: string
}

export interface ModuleOut {
    id: number
    name: string
    description: string | null
    project_id: number
    created_at: string
}

export interface TestCaseOut {
    id: number
    name: string
    description: string | null
    case_type: 'api' | 'ui' | 'perf'
    priority: 'P0' | 'P1' | 'P2' | 'P3'
    module_id: number
    creator_id: number
    request_config: Record<string, unknown> | null
    created_at: string
}

export interface JobOut {
    id: number
    name: string
    project_id: number
    creator_id: number
    celery_task_id: string | null
    status: 'pending' | 'running' | 'success' | 'failed' | 'cancelled'
    created_at: string
}

export interface ReportOut {
    id: number
    job_id: number
    total: number
    passed: number
    failed: number
    skipped: number
    duration: number
    report_url: string | null
    created_at: string
}

export interface PaginatedResponse<T> {
    items: T[]
    total: number
    page: number
    size: number
}
