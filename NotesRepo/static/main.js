$(document).ready(function () {
    if (localStorage.getItem('notes_repo_theme') != 'default') {
        $('body').addClass('alt-theme');
        $('nav').removeClass('navbar-light');
        $('nav').addClass('navbar-dark');
    }
});

function changeTheme() {
    if (localStorage.getItem('notes_repo_theme') == 'default') {
        $('body').addClass('alt-theme');
        $('nav').removeClass('navbar-light');
        $('nav').addClass('navbar-dark');
        localStorage.setItem('notes_repo_theme', 'alt')
    } else {
        $('body').removeClass('alt-theme');
        $('nav').addClass('navbar-light');
        $('nav').removeClass('navbar-dark');
        localStorage.setItem('notes_repo_theme', 'default')
    }
}

function refreshPage() {
    $('#pageContent').load(location.href + ' #pageContent');
    $('#navContent').load(location.href + ' #navContent');
}

function toggleDiv(divId) {
    $('#' + divId).toggle();
}

function format(cmd, val) {
    document.execCommand(cmd, false, val);
}

// Notes

function noteEdit(noteId) {
    $('#loading').toggle();
    $('#done').toggle();
    $.post('editor', {
        id_: noteId,
        title: $('#title').val(),
        folder_id: $('#folderId').val(),
        content: $('#content').html()
    }, function(data) {
        refreshPage();
    });
}

function noteDelete(noteId) {
    $.get('note_delete', {
        id_: noteId
    }, function(data) {
        refreshPage();
    });
}

function noteFavorite(noteId) {
    $.get('note_favorite', {
        id_: noteId
    }, function(data) {
        refreshPage();
    });
}

// Folders

function folderCreate() {
    $.post('folder_create', {
        name: $('#name').val()
    }, function(data) {
        refreshPage();
    });
}

function folderEdit(folderId) {
    $.post('folder_edit', {
        id_: folderId,
        name: $('#name' + folderId).val(),
        color: $('#color' + folderId).val()
    }, function(data) {
        refreshPage();
    });
}

function folderDelete(folderId) {
    $.get('folder_delete', {
        id_: folderId
    }, function(data) {
        refreshPage();
    });
}

// Links

function linkCreate() {
    $.post('link_create', {
        url: $('#url').val(),
        title: $('#title').val()
    }, function(data) {
        refreshPage();
    });
}

function linkEdit(linkId) {
    $.post('link_edit', {
        id_: linkId,
        url: $('#url' + linkId).val(),
        title: $('#title' + linkId).val()
    }, function(data) {
        refreshPage();
    });
}

function toggleRead(linkId) {
    $.get('toggle_read', {
        id_: linkId
    }, function(data) {
        refreshPage();
    });
}

function linkDelete(linkId) {
    $.get('link_delete', {
        id_: linkId
    }, function(data) {
        refreshPage();
    });
}

function getTitle() {
    $.post("get_title", { url : $('#url').val() }, function(data) { $('#title').val(data); });
}