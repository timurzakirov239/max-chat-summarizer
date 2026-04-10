"""Тесты модуля бота."""

from bot.keyboards import get_main_keyboard, get_period_keyboard
from bot.middleware import RateLimiter


class TestKeyboards:
    def test_main_keyboard_structure(self):
        kb = get_main_keyboard()
        assert kb["type"] == "inline_keyboard"
        assert len(kb["payload"]["buttons"]) == 2

    def test_period_keyboard_structure(self):
        kb = get_period_keyboard()
        assert kb["type"] == "inline_keyboard"


class TestRateLimiter:
    def test_allows_under_limit(self):
        limiter = RateLimiter(limit=3, window=60)
        assert all(limiter.is_allowed(user_id=1) for _ in range(3))

    def test_blocks_over_limit(self):
        limiter = RateLimiter(limit=2, window=60)
        limiter.is_allowed(user_id=1)
        limiter.is_allowed(user_id=1)
        assert not limiter.is_allowed(user_id=1)

    def test_different_users(self):
        limiter = RateLimiter(limit=1, window=60)
        assert limiter.is_allowed(user_id=1)
        assert limiter.is_allowed(user_id=2)
