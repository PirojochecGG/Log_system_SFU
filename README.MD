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

Убедитесь, что у вас установлен Node.js. Затем выполните команды:

```bash
cd logistics-backend
npm install
cd ..\logistics-frontend
npm install
```

## 📝 4. Настройка файла .env

Перейдите в каталог logistics-backend.
Создайте файл .env.
Заполните файл следующими данными:

```.env
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=your_port
DB_NAME=logistics_db
JWT_SECRET=your_jwt_secret
```

🔑 Замените your_username, your_password и your_jwt_secret на ваши значения.

## ▶️ 5. Запуск проекта. Запуск backend

Перейди в каталог logistics-backend и выполни команду:

```bash
cd logistics-backend
node app.js
```

## ▶️ 6. Запуск проекта. Запуск frontend

Перейди в каталог logistics-frontend и выполни команду:

```bash
cd logistics-frontend
npm start
```

## 🎉 7. Успешный запуск

Теперь проект запущен и готов к работе! 🌟
Откройте браузер и проверьте, что всё работает. Наслаждайтесь!

## ⚖️ Лицензия

Проект распространяется под лицензией GNU General Public License v3.0.

Если у вас возникли вопросы или предложения, не стесняйтесь открывать issue в репозитории. 💡