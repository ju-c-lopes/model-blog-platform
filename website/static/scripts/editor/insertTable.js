document.addEventListener("DOMContentLoaded", () => {

    const tableBtn = document.querySelector(".table-btn");
    const tablePopup = document.querySelector(".table-buttons")
    const insertTableBtn = document.querySelector(".insert-tb-btn");
    const closeTableButton = document.querySelector(".close-tb-btn");

    if (tableBtn && tablePopup) {
        tableBtn.addEventListener("click", () => {
            tablePopup.style.display = "flex";
        });
    }

    if (closeTableButton && tablePopup) {
        closeTableButton.addEventListener("click", () => {
            tablePopup.style.display = "none";
        });
    }

    if (insertTableBtn) {
        insertTableBtn.addEventListener("click", () => {
            const rows = Number.parseInt(document.getElementById("id_row_table").value);
            const cols = Number.parseInt(document.getElementById("id_col_table").value);

            if (!rows || !cols) {
                alert("Please enter rows and columns.");
                return;
            }

            let table = "<table class='post-table' data-responsive='true'>";

            for (let r = 0; r < rows; r++) {
                table += "<tr>";
                for (let c = 0; c < cols; c++) {
                    if (r === 0) {
                        table += "<th>Header</th>";
                    } else {
                        table += "<td>Data</td>";
                    }
                }
                table += "</tr>";
            }
            table += "</table>";
            insertHtmlAtCursor(table);
            const range = window.quillEditor.getSelection(true);
            window.quillEditor.setSelection(range.index + 1);
            tablePopup.style.display = "none";

            document.getElementById("id_row_table").value = "";
            document.getElementById("id_col_table").value = "";
        });
    }
});
