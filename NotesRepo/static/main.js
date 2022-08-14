$(document).ready(function() {
    document.documentElement.setAttribute('data-theme', localStorage.getItem('NotesRepo'));
});

function changeTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('NotesRepo', theme);
}

function refreshPage() {
    $('#pageContent').load(location.href + ' #pageContent');
    $('#navContent').load(location.href + ' #navContent');
}

function toggleDiv(divId) {
    $('#' + divId).fadeToggle(250);
}

function noteEdit(noteId) {
    $('#loading').toggle();
    $.post('editor', {
        id_: noteId,
        title: $('#notetitle').val(),
        folder_id: $('#folderId').val(),
        content: $('#content').val()
    }, function(data) {
        refreshPage();
    });
}

function noteFavorite(noteId) {
    $('#spinner').show();
    $.get('note_favorite', {
        id_: noteId
    }, function(data) {
        refreshPage();
    });
}

function folderEdit(folderId) {
    $('#spinner').show();
    $.post('folder_edit', {
        id_: folderId,
        name: $('#name').val()
    }, function(data) {
        refreshPage();
    });
}

function changePassword() {
    $('#spinner').show();
    $.post('change_password', {
        old_password: $('#oldPassword').val(),
        new_password: $('#newPassword').val(),
        new_password_confirm: $('#newPasswordConfirm').val()
    }, function(data) {
        refreshPage();
    });
}

function changeUsername() {
    $('#spinner').show();
    $.post('account', {
        username: $('#username').val()
    }, function(data) {
        refreshPage();
    });
}