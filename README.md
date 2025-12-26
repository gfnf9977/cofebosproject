# cofebos

Вебзастосунок для керування кав’ярнею (користувачі, замовлення, напої, випічка, вакансії, бонуси).  
Проєкт складається з frontend (Vue.js) та backend (Python) і працює з локальною базою даних **MS SQL Server**.

Для запуску frontend:
```bash
npm install
npm run serve

Backend підключається до бази даних через pyodbc. Параметри підключення знаходяться у файлі app.py:

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=legion;'
        'Database=coffeebes;'
        'Trusted_Connection=yes;'
    )
    return conn

Проєкт використовує локальну MS SQL Server з Windows-аутентифікацією. Назва бази даних — coffeebes.
Якщо база даних відсутня або проєкт запускається на новому пристрої, її необхідно створити вручну.

У корені проєкту є файл db_script.txt, який містить повний SQL-скрипт створення бази даних з нуля (створення БД, усіх таблиць і зв’язків).
Для ініціалізації БД потрібно відкрити db_script.txt у SQL Server Management Studio, скопіювати весь вміст і виконати скрипт.

Проєкт не створює базу автоматично, без виконання SQL-скрипта backend працювати не буде.
За потреби змініть ім’я сервера, назву БД або тип автентифікації у файлі app.py.