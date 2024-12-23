function sortTable(columnIndex, headerElement) {
    const table = document.getElementById("productsTable");
    const rows = Array.from(table.rows).slice(1);
    const isAscending = table.dataset.sortOrder === "asc";

    rows.sort((rowA, rowB) => {
        const cellA = rowA.cells[columnIndex].innerText.trim();
        const cellB = rowB.cells[columnIndex].innerText.trim();

        if (!isNaN(cellA) && !isNaN(cellB)) {
            return isAscending ? cellA - cellB : cellB - cellA;
        }
        return isAscending 
            ? cellA.localeCompare(cellB, undefined, { numeric: true }) 
            : cellB.localeCompare(cellA, undefined, { numeric: true });
    });

    table.tBodies[0].append(...rows);
    table.dataset.sortOrder = isAscending ? "desc" : "asc";

    const allHeaders = table.querySelectorAll("th span");
    allHeaders.forEach(span => span.textContent = "");
    headerElement.querySelector("span").textContent = isAscending ? "\u2191" : "\u2193";
}

const searchForm = document.getElementById("searchForm");
searchForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(searchForm);
    const searchParams = new URLSearchParams(formData);
    console.log(searchParams.toString());

    const response = await fetch("search?"  + searchParams.toString(), {
        method: "GET",
    });

    if (response.ok) {
        const data = await response.json();
        console.log(data);

        const tbody = document.querySelector("#productsTable tbody");
        tbody.innerHTML = data.map(product => `
            <tr>
                <td>${product.code}</td>
                <td>${product.name}</td>
                <td>${product.quantity}</td>
                <td>${product.unit}</td>
                <td>${product.price}</td>
                <td>${product.total_price}</td>
            </tr>
        `).join("");
    } else {
        console.error("Ошибка при получении данных", response.status, response.statusText)
        const text = await response.text();
        console.log(text);
    }
});

document.getElementById("resetSearch").addEventListener("click", async (event) => {
    event.preventDefault();
    const response = await fetch("search?", { method: "GET" });

    if (response.ok) {
        const data = await response.json();
        const tbody = document.querySelector("#productsTable tbody");
        tbody.innerHTML = data.map(product => `
            <tr>
                <td>${product.code}</td>
                <td>${product.name}</td>
                <td>${product.quantity}</td>
                <td>${product.unit}</td>
                <td>${product.price}</td>
                <td>${product.total_price}</td>
            </tr>
        `).join("");
    }
});