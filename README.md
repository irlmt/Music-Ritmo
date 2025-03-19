# MusicRitmo App

## Настройка окружения

1. Клонируйте репозиторий с помощью 
```bash
https://github.com/BenSerg/Music-Ritmo.git
```
2. Чтобы создать виртуальное окружение, перейдите в директорию проекта, а затем выполните команду
    
    Для Windows: 
    ```bash
    py -m venv venv
    venv\Scripts\activate
    ```
    Для Linux/macOS:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Установите зависимости
    ```bash
    pip install -r requirements.txt
    ```

## Запуск приложения
1. Запуск приложения
    ```bash
    uvicorn src.app.main:app
    ```

2. Запуск тестов
    ```bash
    pytest tests/
    ```
    Чтобы выводился print() в тестах, добавляем опцию -s

## Работа с БД через SQLModel
Есть туториал (https://sqlmodel.tiangolo.com/tutorial/), где всё описано, даже есть раздел с FastAPI.

## Просмотр БД
DB Browser for SQLite https://sqlitebrowser.org/

## Проверка типов с mypy
```bash
mypy . --explicit-package-bases
```

## Процесс ведения разработки
Доска в YouGile с описанием задач: https://ru.yougile.com/team/648d0d0eb67a/Music-Ritmo
Соответствие цветов задачам:
1) Задачи связанные с фронтендом - бесцветные
2) Задачи связанные с бекэндом - голубые
3) Задачи связанные с тестированием - зелёные
4) Прочие задачи (документация, настройки репозитория) - жёлтые
