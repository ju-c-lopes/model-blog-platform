function buildTable(rows, cols) {
    let table = "<table class='post-table' data-responsive='true'>";

    for (let r = 0; r < rows; r++) {
        table += "<tr>";

        for (let c = 0; c < cols; c++) {
            table += r === 0 ? "<th>Header</th>" : "<td>Data</td>";
        }

        table += "</tr>";
    }

    table += "</table>";
    return table;
}

function insertTable() {
    const rows = Number.parseInt(document.getElementById("id_row_table").value, 10);
    const cols = Number.parseInt(document.getElementById("id_col_table").value, 10);

    if (!rows || !cols) {
        alert("Please enter rows and columns.");
        return;
    }

    const table = buildTable(rows, cols);

    insertIntoEditor(table);

    const range = window.quillEditor.getSelection(true);
    window.quillEditor.setSelection(range.index + 1);

    closePopup(".table-buttons");

    document.getElementById("id_row_table").value = "";
    document.getElementById("id_col_table").value = "";
}

function initTable() {
    const insertTableBtn = document.querySelector(".insert-tb-btn");

    if (insertTableBtn) {
        insertTableBtn.addEventListener("click", insertTable);
    }
}

window.initTable = initTable;