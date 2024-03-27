# cs2_spinner
API для развертывания докер контейнеров с CS2 серверами

## Запуск:

1. Клоинровать репозиторий
2. Создать виртуальное окружение: `python -m venv venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. Перейти в папку src
6. `uvicorn main:app`

API будет доступно на http://localhost:8000


## Документация по умолчанию: http://localhost:8000/docs


## Пример запроса:

POST `http://appname/containers/`

```json
{
    "name": "test",
    "port": 27015,
    "rcon_port": 27020,
    "image": "joedwards32/cs2:latest"
}

```

Response:

```json
{
    "message": "Conmtainer test created",
    "id": "027a27a6e628dc5ad295c426bb497f0e13e5613ce9cfe01a3e02d1e583bf9249"
}
```



GET `http://appname/containers/`

Response:

```json
{
    "containers": [
        {
            "id": "3464a86a42b28d311f6c725f515d86bed515ba29ed54deb5245545d167cab62c",
            "name": "test_two",
            "status": "running"
        },
        {
            "id": "027a27a6e628dc5ad295c426bb497f0e13e5613ce9cfe01a3e02d1e583bf9249",
            "name": "test",
            "status": "running"
        }
    ]
}
```
