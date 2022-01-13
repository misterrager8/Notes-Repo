function folderCreate() {
    $.post('/folder_create', {
        name : $('#folderName').val()
    }, function(data) {
        refreshDiv('allFolders');
    });
    $('#folderName').val('');
}

function savePage(pageId) {
    showProgress();
    $.post('editor', {
        id_ : pageId,
        title : $('#title').val(),
        folder_id : $('#folder_id').val(),
        content : $('#content').html()
    },
    function(data) {
        showProgress();
    });
}

function folderUpdate(folderId) {
    $.post('folder_update', {
        id_ : folderId,
        name : $('#folderName' + folderId).val(),
        color : $('#folderColor' + folderId).val()
    }, function(data) {
        refreshDiv('allFolders');
    });
}

function deletePage(pageId) {
    $.get('page_delete', { id_ : pageId }, function(data) { refreshDiv('allPages'); });
}

function deleteFolder(folderId) {
    $.get('folder_delete', { id_ : folderId }, function(data) { refreshDiv('allFolders'); });
}

function bookmarkPage(pageId) {
    $.get('mark_page', { id_ : pageId }, function(data) { refreshDiv('allPages'); });
}

function hidePage(pageId) {
    $.get('page_visibility', { id_ : pageId }, function(data) { refreshDiv('allPages'); });
}

function format(cmd, val) {
    document.execCommand(cmd, false, val);
}

function showProgress() {
    $('#loading').toggle();
    $('#done').toggle();
}

function refreshDiv(divId) {
    $('#' + divId).load(location.href + ' #' + divId);
}

function changeTheme() {
    if (localStorage.getItem('notes_repo_theme') == 'default') {
        $('body').addClass('alt-theme');
        localStorage.setItem('notes_repo_theme', 'alt')
    } else {
        $('body').removeClass('alt-theme');
        localStorage.setItem('notes_repo_theme', 'default')
    }
}

$(document).ready(function () {
    if (localStorage.getItem('notes_repo_theme') != 'default') {
        $('body').addClass('alt-theme');
    }
});