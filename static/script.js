$(document).ready(function () {
    $('a[name="updateValue"]').click(function (e) {
        e.preventDefault();
        var url = $(this).attr('href');
        window.location.href = url;
    });
});
function insertRows() {
    var searchAndInsertButton = document.getElementById('searchAndInsertButton');
    var insertTable = document.getElementById('insertTable');
    insertTable.classList.remove('d-none');
    searchAndInsertButton.classList.add('d-none');
}

function updateRows() {
    var searchAndInsertButton = document.getElementById('searchAndInsertButton');
    var cancelUpdate = document.getElementById('cancelUpdate');
    var updateRow = document.getElementsByName('updateRow');

    searchAndInsertButton.classList.add('d-none');
    cancelUpdate.classList.remove('d-none');
    for (var i = 0; i < updateRow.length; i++) {
        updateRow[i].classList.remove('d-none');
    }
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
        deleteRow[i].classList.remove('d-none');
    }
    searchAndInsertButton.classList.add('d-none');
    cancelDelete.classList.remove('d-none');
}

function cancelDelete() {
    var searchAndInsertButton = document.getElementById('searchAndInsertButton');
    var cancelDelete = document.getElementById('cancelDelete');
    var deleteRow = document.getElementsByName('deleteRow');
    for (var i = 0; i < deleteRow.length; i++) {
        deleteRow[i].classList.add('d-none');
    }
    searchAndInsertButton.classList.remove('d-none');
    cancelDelete.classList.add('d-none');
}

function cancelUpdate() {
    var searchAndInsertButton = document.getElementById('searchAndInsertButton');
    var cancelUpdate = document.getElementById('cancelUpdate');
    var updateRow = document.getElementsByName('updateRow');
    for (var i = 0; i < updateRow.length; i++) {
        updateRow[i].classList.add('d-none');
    }
    searchAndInsertButton.classList.remove('d-none');
    cancelUpdate.classList.add('d-none');
}

