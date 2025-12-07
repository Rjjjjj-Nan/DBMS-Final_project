document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("optionsModal");
    const closeModal = document.getElementById("closeModal");
    let selectedReportId = null;

    document.querySelectorAll(".clickable-img").forEach(img => {
        img.addEventListener("click", function() {
            selectedReportId = this.dataset.reportId;
            modal.style.display = "block";
        });
    });

    closeModal.addEventListener("click", function() {
        modal.style.display = "none";
    });

    document.getElementById("updateBtn").addEventListener("click", function() {
        window.location.href = "/update/" + selectedReportId;
    });

    document.getElementById("deleteBtn").addEventListener("click", function() {
        if (confirm("Are you sure you want to delete this report?")) {
            window.location.href = "/delete/" + selectedReportId;
        }
    });

    window.addEventListener("click", function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const tableRows = document.querySelectorAll("table tbody tr");

    // Stop Enter from reloading page
    searchInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            filterTable();
        }
    });

    // Filter while typing
    searchInput.addEventListener("input", filterTable);

    function filterTable() {
        const filter = searchInput.value.toLowerCase();

        tableRows.forEach(row => {
            const rowText = row.innerText.toLowerCase();
            row.style.display = rowText.includes(filter) ? "" : "none";
        });
    }
});