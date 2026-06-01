function openCreateTransactionModal() {
    const form = document.getElementById("transaction-form");

    form.reset();
    form.action = "/transactions/create";

    document.getElementById("transaction-modal-title").innerText = "Add transaction";
    document.getElementById("transaction-submit-button").innerText = "Create";

    document.getElementById("amount").value = 1;
    document.getElementById("spent_at").value = new Date().toISOString().split('T')[0];

    document.getElementById("transaction-modal").classList.remove("hidden");
};

function openEditTransactionModal(transaction) {
    const form = document.getElementById("transaction-form");

    form.action = `/transactions/${transaction.id}/update`;

    document.getElementById("transaction_id").value = transaction.id;
    document.getElementById("title").value = transaction.title;
    document.getElementById("unit_price").value = transaction.unit_price;
    document.getElementById("currency").value = transaction.currency;
    document.getElementById("category_id").value = transaction.category_id;
    document.getElementById("amount").value = transaction.amount;
    document.getElementById("comment").value = transaction.comment || "";
    document.getElementById("spent_at").value = transaction.spent_at.split("T")[0];

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