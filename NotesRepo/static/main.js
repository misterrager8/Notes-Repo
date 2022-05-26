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

function format(cmd, val) {
    document.execCommand(cmd, false, val);
}

function shortcut(event) {
    if (event.ctrlKey) {
        switch (event.key) {
            case 'b':
                format('bold');
                break;
            case 'i':
                format('italic');
        }
    } else if (event.key === '(') { event.preventDefault(); format('insertText', '(' + window.getSelection() + ')');
    } else if (event.key === '[') { event.preventDefault(); format('insertText', '[' + window.getSelection() + ']');
    } else if (event.key === '{') { event.preventDefault(); format('insertText', '{' + window.getSelection() + '}'); }
}

// Notes

function noteEdit(noteId) {
    $('#loading').toggle();
    $.post('editor', {
        id_: noteId,
        title: $('#title').val(),
        folder_id: $('#folderId').val(),
        content: $('#content').val()
    }, function(data) {
        refreshPage();
    });
}

function noteDelete(noteId) {
    $('#spinner').show();
    $.get('note_delete', {
        id_: noteId
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

// Folders

function folderCreate() {
    $('#spinner').show();
    $.post('folder_create', {
        name: $('#name').val()
    }, function(data) {
        refreshPage();
    });
}

function folderEdit(folderId) {
    $('#spinner').show();
    $.post('folder_edit', {
        id_: folderId,
        name: $('#name' + folderId).val(),
        color: $('#color' + folderId).val()
    }, function(data) {
        refreshPage();
    });
}

function folderDelete(folderId) {
    $('#spinner').show();
    $.get('folder_delete', {
        id_: folderId
    }, function(data) {
        refreshPage();
    });
}

// Links

function linkCreate() {
    $('#spinner').show();
    $.post('link_create', {
        url: $('#url').val(),
        title: $('#title').val()
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
