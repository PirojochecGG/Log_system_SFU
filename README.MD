# 🚀 Добро пожаловать в проект Logistics!  

Этот проект создан для упрощения работы с логистикой и автоматизации ваших процессов. Следуйте приведённым ниже шагам, чтобы быстро и легко запустить приложение.  

---
## 📥 1. Клонирование репозитория

Для начала склонируйте репозиторий из GitHub. Выполните следующую команду в терминале:  

```bash
git clone https://github.com/SeIekpann/Log_system_SFU.git
```
## 🛠️ 2. Открытие терминала

Откройте cmd или PowerShell в корневой директории проекта.

## 📦 3. Установка зависимостей

Убедитесь, что у вас установлен Python 3.12.7 и выше. Затем выполните команды:

```bash
pip install requirements.txt
```

## 📝 4. Настройка файла settings.py

Перейдите в каталог logistics
И создайте файл .env в любом текстовом редакторе.
Заполните файл следующими данными:

```.env

SECRET_KEY=django-insecure-ВашСекретныйКлюч
DEBUG=на ваш выбор 

# база данных
NAME=имя вашей бд
USER=имя пользователя
PASSWORD=пароль пользователя
HOST=хост бд
PORT=порт бд

# почта
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=
ADMIN_EMAIL=

```

🔑 Замените на ваши значения.

## ▶️ 5. Выполнение миграций.
Перейди в каталог logistics

```bash
cd logistics
python manage.py makemigrations
python manage.py migrate
```

## ▶️ 6. Запуск проекта.

Перейди в каталог logistics

```bash
cd logistics
python manage.py runserver 9000
```

## 🎉 7. Успешный запуск

Теперь проект запущен и готов к работе! 🌟
Откройте браузер и проверьте, что всё работает. Наслаждайтесь!

## ⚖️ Лицензия

Проект распространяется под лицензией GNU General Public License v3.0.

Если у вас возникли вопросы или предложения, не стесняйтесь открывать issue в репозитории. 💡
