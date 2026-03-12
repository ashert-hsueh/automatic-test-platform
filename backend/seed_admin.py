"""
初始化管理员账号
运行: python seed_admin.py
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.security import hash_password
from app.models.user import User, UserRole


async def seed():
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    Session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

    async with Session() as db:
        # 检查是否已存在
        result = await db.execute(select(User).where(User.username == "admin"))
        if result.scalar_one_or_none():
            print("✅ admin 用户已存在，无需重复创建")
            return

        admin = User(
            username="admin",
            email="admin@autotest.local",
            hashed_password=hash_password("admin123"),
            full_name="管理员",
            role=UserRole.ADMIN,
            is_active=True,
        )
        db.add(admin)
        await db.commit()
        print("✅ admin 用户创建成功！")
        print("   用户名: admin")
        print("   密码:   admin123")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
