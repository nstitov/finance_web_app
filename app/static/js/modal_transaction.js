function openCreateTransactionModal() {
    const form = document.getElementById("transaction-form");

    form.reset();
    form.action = "/transactions/create";

    document.getElementById("transaction_id").value = "";
    document.getElementById("transaction-modal-title").innerText = "Add transaction";
    document.getElementById("transaction-submit-button").innerText = "Create";

    document.getElementById("transaction-modal").classList.remove("hidden");
};

function openEditTransactionModal(transaction) {
    const form = document.getElementById("transaction-form");

    form.action = `/transactions/${transaction.id}/update`;

    document.getElementById("transaction_id").value = transaction.id;
    document.getElementById("amount").value = transaction.amount;
    document.getElementById("transaction_type").value = transaction.transaction_type;
    document.getElementById("category_id").value = transaction.category_id;
    document.getElementById("description").value = transaction.description || "";
    document.getElementById("transaction_date").value =
        transaction.transaction_date.slice(0, 10);

    document.getElementById("transaction-modal-title").innerText = "Edit transaction";
    document.getElementById("transaction-submit-button").innerText = "Update";

    document.getElementById("transaction-modal").classList.remove("hidden");
};

function closeTransactionModal() {
    document.getElementById("transaction-modal").classList.add("hidden");
};

window.openCreateTransactionModal = openCreateTransactionModal;
window.openEditTransactionModal = openEditTransactionModal;
window.closeTransactionModal = closeTransactionModal;