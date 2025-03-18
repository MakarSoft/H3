## README

1. исходные данные:
дана область - координаты центра 56 с.ш. 38 в.д, радиус 7 км
создать массив h3 гексагонов 12-го уровня заполняющих эту область, с данными вида
[ [h3_index, level, cell_id], ... ]
где
	level: случайное integer в диапазоне -47... -120
	cell_id: случайное integer в диапазоне 1... 100

2. c использованием фреймворка FastAPI написать API с тремя ендпоинтами:

   - GET /hex
   - header: parent_hex - индекс гексагона
возвращает KMZ-файл - массив гексагонов из исходного датасета входящих в
заданный гексагон

   - GET /bbox
   - header: border - массив координат границ выборки lon/lat
возвращает массив гексагонов из исходного датасета входящих в заданные границы
   - GET /avg
   - header: resolution
возвращает массив гексагонов заданного разрешения, с медианным значением level
сгруппированным по cell_id из исходного датасета

### Структура проекта

```
geo/
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

### Запуск

```bash
uvicorn app.main:app --reload
```

### Проверка ...

```bash
curl -X GET "http://127.0.0.1:8000/hex" -H "parent_hex: 8c11aa6483607ff"
```

```bash
curl -X GET "http://127.0.0.1:8000/avg" -H "resolution: 12"
```

```bash
curl -X GET "http://127.0.0.1:8000/bbox" -H "border: 55.999, 37.999,55.999, 38.001,56.001, 38.001,56.001, 37.999,55.999, 37.999"
```

```bash
# curl -X GET "http://127.0.0.1:8000/bbox" -H "border: 55.5,37.5,55.5,38.5,56.5,38.5,55.5,37.5"
```
