#!/bin/bash

# Активация виртуального окружения (myvenv в корне проекта)
VENV_DIR="myvenv"
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
else
    echo "Виртуальное окружение не найдено: $VENV_DIR"
    exit 1
fi

# Запуск скрипта aiogram_run.py
python aiogram_run.py