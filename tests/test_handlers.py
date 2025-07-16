# المسار: tests/test_handlers.py

import pytest
from unittest.mock import AsyncMock, MagicMock

# استيراد الدالة التي نريد اختبارها
from src.alsaada_bot.handlers.start import start_command


@pytest.mark.asyncio
async def test_start_command_sends_reply_with_keyboard():
    """
    يختبر ما إذا كان الأمر /start يستجيب برسالة تحتوي على لوحة مفاتيح.
    """
    # 1. الإعداد (Arrange):
    # نقوم بإنشاء كائنات وهمية (Mock) لتحاكي التحديث القادم من تليجرام
    update = AsyncMock()
    # إعداد كائن المستخدم الوهمي
    update.effective_user = MagicMock(
        first_name="TestUser",
        id=12345,
        mention_html=lambda: "<a href='tg://user?id=12345'>TestUser</a>",
    )
    # إعداد كائن الرسالة الوهمي الذي يحتوي على دالة للرد
    update.message = AsyncMock()

    # 2. التنفيذ (Act):
    # نقوم باستدعاء دالة المعالج التي نريد اختبارها
    await start_command(update, context=AsyncMock())

    # 3. التحقق (Assert):
    # نتأكد من أن دالة الرد (reply_html) قد تم استدعاؤها مرة واحدة بالضبط
    update.message.reply_html.assert_called_once()
    # نتأكد من أن الرد يحتوي على لوحة المفاتيح (reply_markup)
    call_args, call_kwargs = update.message.reply_html.call_args
    assert "reply_markup" in call_kwargs, "The reply should contain a keyboard."
