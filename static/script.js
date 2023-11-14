function insertRows() {
    var searchAndInsertButton = document.getElementById('searchAndInsertButton');
    var insertTable = document.getElementById('insertTable');
    insertTable.classList.remove('d-none');
    searchAndInsertButton.classList.add('d-none');
}

function searchRows() {
    var searchAndInsertButton = document.getElementById('searchAndInsertButton');
    var searchTable = document.getElementById('searchTable');
    searchTable.classList.remove('d-none');
    searchAndInsertButton.classList.add('d-none');
}

function deleteRows() {
    var searchAndInsertButton = document.getElementById('searchAndInsertButton');
    var cancelDelete = document.getElementById('cancelDelete');
    var deleteRow = document.getElementsByName('deleteRow');
    for (var i = 0; i < deleteRow.length; i++) {
        deleteRow[i].classList.remove('d-none')
    }
    searchAndInsertButton.classList.add('d-none');
    cancelDelete.classList.remove('d-none');
}

function cancelDelete() {
    var searchAndInsertButton = document.getElementById('searchAndInsertButton');
    var cancelDelete = document.getElementById('cancelDelete');
    var deleteRow = document.getElementsByName('deleteRow');
    for (var i = 0; i < deleteRow.length; i++) {
        deleteRow[i].classList.add('d-none')
    }
    searchAndInsertButton.classList.remove('d-none');
    cancelDelete.classList.add('d-none');
}

