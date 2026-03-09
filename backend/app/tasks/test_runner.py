import time
import asyncio
from app.core.celery_app import celery_app
from app.core.config import settings
import redis


def publish_log(task_id: str, message: str):
    """向 Redis 频道推送执行日志，供 WebSocket 读取"""
    try:
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        r.publish(f"task_log:{task_id}", message)
    except Exception:
        pass  # 日志推送失败不影响主流程


@celery_app.task(bind=True, name="app.tasks.test_runner.run_test_job")
def run_test_job(self, job_id: int, case_ids: list[int]):
    """
    执行测试任务
    - 从数据库加载用例配置
    - 调用 API 引擎执行
    - 实时推送日志到 Redis Channel
    - 写回执行结果
    """
    task_id = self.request.id
    publish_log(task_id, f"[START] 任务开始执行，Job ID: {job_id}")
    publish_log(task_id, f"[INFO]  共 {len(case_ids)} 条用例待执行")

    passed = 0
    failed = 0
    start_time = time.time()

    for idx, case_id in enumerate(case_ids, 1):
        publish_log(task_id, f"[RUN]   执行用例 #{case_id} ({idx}/{len(case_ids)})")
        time.sleep(0.5)  # 模拟执行耗时（真实环境替换为 api_runner）

        # TODO: 替换为真实 API/UI/Perf 引擎调用
        # result = api_runner.run(case_config)
        success = True  # 占位：实际根据引擎返回判断

        if success:
            passed += 1
            publish_log(task_id, f"[PASS]  用例 #{case_id} 通过 ✓")
        else:
            failed += 1
            publish_log(task_id, f"[FAIL]  用例 #{case_id} 失败 ✗")

    duration = round(time.time() - start_time, 2)
    publish_log(task_id, f"[DONE]  执行完毕 | 通过: {passed} | 失败: {failed} | 耗时: {duration}s")

    return {
        "job_id": job_id,
        "total": len(case_ids),
        "passed": passed,
        "failed": failed,
        "skipped": 0,
        "duration": duration,
    }
