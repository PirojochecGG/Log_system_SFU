document.addEventListener('DOMContentLoaded', function () {
    const operationsTable = document.getElementById('operationsTable');
    const productsTableContainer = document.getElementById('productsTableContainer');
    const productsTableBody = document.getElementById('productsTable').getElementsByTagName('tbody')[0];
    
    operationsTable.addEventListener('click', function (event) {
        const row = event.target.closest('tr');
        if (!row || !row.hasAttribute('data-operation-id')) return;

        const operationId = row.getAttribute('data-operation-id');
        
        const previouslyHighlightedRow = operationsTable.querySelector('.highlighted');
        if (previouslyHighlightedRow) {
            previouslyHighlightedRow.classList.remove('highlighted');
        }
        
        row.classList.add('highlighted');
        toggleProductsTable(operationId);
        
    });

    function toggleProductsTable(operationId) {
       productsTableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-muted">Загрузка товаров...</td>
            </tr>
       `;

        productsTableContainer.style.display = 'block';

        fetch(`/get_products_by_operation/${operationId}/`)
            .then(response =>  {
                if(!response.ok){
                    throw new Error(`Ошибка: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                productsTableBody.innerHTML = '';
                if (data.products.length === 0) {
                    const row = productsTableBody.insertRow();
                    const cell = row.insertCell(0);
                    cell.colSpan = 6;
                    cell.textContent = 'Нет товаров для этой операции.';
                    cell.classList.add('text-center', 'text-muted');
                } else {
                    data.products.forEach(product => {
                        const row = productsTableBody.insertRow();
                        row.insertCell(0).textContent = product.code;
                        row.insertCell(1).textContent = product.name;
                        row.insertCell(2).textContent = product.quantity;
                        row.insertCell(3).textContent = product.unit;
                        row.insertCell(4).textContent = product.price;
                        row.insertCell(5).textContent = product.total_price;
                    });
                }
            })
            .catch(error => {
                console.error('Ошибка загрузки товаров:', error);
                productsTableBody.innerHTML = `<tr>
                    <td colspan="6" class="text-center text-danger">Не удалось загрузить товары.</td>
                </tr>`;
            });
    }

    // Получение CSRF-токена из cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    let qrReader;
    let isProcessing = false;

    const startQRReader = () => {
        if (isProcessing) return;

        isProcessing = true;

        qrReader = new Html5Qrcode("qr-reader");
        qrReader.start(
            { facingMode: "environment" }, // Запускаем заднюю камеру (если доступно)
            {
                fps: 30, // Частота кадров
                qrbox: { width: 250, height: 250 }, // Область считывания
            },
            (decodedText) => {
                // QR-код успешно считан
                alert("Считано: " + decodedText);
                fetch('/add_product/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ qr_data: decodedText })
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message || "Данные успешно обработаны!");
                    qrReader.stop();
                    document.getElementById('qr-reader-container').style.display = 'none';
                    isProcessing = false;
                })
                .catch(error => {
                    alert("Ошибка при обработке данных: " + error.message);
                    isProcessing = false;
                });
            },
            (errorMessage) => {
                console.log("Ошибка сканирования:", errorMessage);
                isProcessing = false;
            }
        ).catch((err) => {
            console.error("Ошибка при запуске камеры:", err);
            alert("Не удалось включить камеру. Проверьте разрешения в браузере.");
            isProcessing = false;
        });
    };


    document.getElementById('accept-product-btn').addEventListener('click', () => {
        if (isProcessing) return;
        document.getElementById('qr-reader-container').style.display = 'block';
        startQRReader();
    });

    document.getElementById('stop-scan-btn').addEventListener('click', () => {
        if (qrReader) {
            qrReader.stop().then(() => {
                document.getElementById('qr-reader-container').style.display = 'none';
                isProcessing = false;
            }).catch((err) => console.error("Ошибка при остановке камеры:", err));
        }
    });

});