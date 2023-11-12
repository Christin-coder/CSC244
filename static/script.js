function insertRows() {
    var insertBtn = document.getElementById('insertBtn');
    var insertTable = document.getElementById('insertTable');
    insertTable.classList.remove('d-none');
    insertBtn.classList.add('d-none');
}

function cancelInsert() {
    var insertBtn = document.getElementById('insertBtn');
    var insertTable = document.getElementById('insertTable');

    insertBtn.classList.remove('d-none');
    insertTable.classList.add('d-none');
}

function submitRows() {
    var insertTable = document.getElementById('insertTable');
    var insertBtn = document.getElementById('insertBtn');

    insertTable.classList.add('d-none');
    insertBtn.classList.remove('d-none');
    return true;
}