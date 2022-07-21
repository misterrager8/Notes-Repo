$(document).ready(function() {
    document.documentElement.setAttribute('data-theme', localStorage.getItem('notesrepo_theme'));
});

function changeTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('notesrepo_theme', theme);
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

function formatText(format) {
    if (format=='bold') {
        document.getElementById('content').value += '\n**bold**';
    } else if (format=='italic') {
        document.getElementById('content').value += '\n*italic*';
    } else if (format=='link') {
        document.getElementById('content').value += '\n[url](text)';
    } else if (format=='heading') {
        document.getElementById('content').value += '\n### ';
    } else if (format=='indent') {
        document.getElementById('content').value += '    ';
    } else if (format=='code') {
        document.getElementById('content').value += '\n<code>\n</code>';
    }
}

function folderEdit(folderId) {
    $('#spinner').show();
    $.post('folder_edit', {
        id_: folderId,
        name: $('#name').val(),
        color: $('#color').val()
    }, function(data) {
        refreshPage();
    });
}
function linkEdit(linkId) {
    $('#spinner').show();
    $.post('link_edit', {
        id_: linkId,
        url: $('#url' + linkId).val(),
        title: $('#title' + linkId).val()
    }, function(data) {
        refreshPage();
    });
}

function toggleRead(linkId) {
    $('#spinner').show();
    $.get('toggle_read', {
        id_: linkId
    }, function(data) {
        refreshPage();
    });
}

function linkDelete(linkId) {
    $('#spinner').show();
    $.get('link_delete', {
        id_: linkId
    }, function(data) {
        refreshPage();
    });
}

function getTitle() {
    $.post("get_title", { url : $('#url').val() }, function(data) { $('#title').val(data); });
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