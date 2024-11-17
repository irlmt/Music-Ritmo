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

## Проверка типов с mypy
```bash
mypy . --explicit-package-bases
```