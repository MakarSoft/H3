```
h3_fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── const/
│   │   ├── __init__.py
│   │   ├── const.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── types.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── exceptions.py
│   │   ├── intersection.py
│   │   ├── h3_utils.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints.py
│   │   ├── models.py
├── tests/
│   ├── __init__.py
│   ├── test_endpoints.py
├── requirements.txt
├── Dockerfile
├── .github/
│   ├── workflows/
│   │   ├── ci_cd.yml
├── README.md
```

```
Запуск
uvicorn app.main:app --reload


Проверка ...
curl -X GET "http://127.0.0.1:8000/hex" -H "parenthex: 8c11aa6483607ff"

curl -X GET "http://127.0.0.1:8000/avg" -H "resolution: 12"  

curl -X GET "http://127.0.0.1:8000/bbox" -H "border: 55.999, 37.999,55.999, 38.001,56.001, 38.001,56.001, 37.999,55.999, 37.999"

curl -X GET "http://127.0.0.1:8000/bbox" -H "border: 55.5,37.5,55.5,38.5,56.5,38.5,55.5,37.5"
```
