"""
Простой conftest.py для tests/ папки.
Обеспечивает что pytest может запуститься даже если основной conftest имеет проблемы.
"""
import sys
import os
from pathlib import Path

# Добавляем родительскую директорию в path чтобы импорты работали
tests_dir = Path(__file__).parent
parent_dir = tests_dir.parent
sys.path.insert(0, str(parent_dir))

import pytest
import allure

# Пытаемся импортировать основной conftest, но не падаем если он имеет проблемы
try:
    # Импортируем все из родительского conftest.py
    from conftest import *  # noqa: F401, F403
except Exception as e:
    print(f"⚠️  Warning: Could not import parent conftest: {e}")
    # Это OK - smoke тесты будут работать без этого
    pass

