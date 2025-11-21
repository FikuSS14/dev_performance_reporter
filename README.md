## Скрипт для анализа эффективности разработчиков по CSV-файлам

Скрипт читает файлы с данными о закрытых задачах и формирует отчет

---

### Структура проекта
```
src/          # основной код
tests/        # unit-тесты (pytest)
data/         # примеры CSV 
requirements.txt
README.md
```
---

### Запуск
#### Установить зависимости 
pip install -r requirements.txt
#### Генерация отчёта 
python src/reporter.py --files data/sample1.csv data/sample2.csv --report performance
#### Пример вывода
<img width="459" height="455" alt="image" src="https://github.com/user-attachments/assets/8596ad8f-1663-4185-acfd-9a0987ee9ea4" />

#### Запуск тестов
python -m pytest tests/ -v
#### Пример вывода:

---

