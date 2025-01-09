document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#report-form");
    const input = document.querySelector("#operation_number");
    const errorMessage = document.querySelector("#error-message");
    const submitButton = document.querySelector("#submit-button");
    const loadingSpinner = document.querySelector("#loading-spinner");

    // Прячем спиннер при загрузке страницы
    loadingSpinner.classList.add("hidden");

    form.addEventListener("submit", (event) => {
        // Очищаем сообщение об ошибке
        errorMessage.textContent = "";

        // Получаем значение из поля ввода и удаляем лишние пробелы
        const operationNumber = input.value.trim();

        // Валидация: номер операции должен быть числом от 1 до 20 символов
        if (!/^\d{1,20}$/.test(operationNumber)) {
            event.preventDefault(); // Останавливаем отправку формы
            errorMessage.textContent = "Номер операции должен быть числом от 1 до 20 символов.";
            input.focus();
            return;
        }

        // Показываем спиннер
        loadingSpinner.classList.remove("hidden");
        submitButton.disabled = true; // Блокируем кнопку отправки
    });
});
