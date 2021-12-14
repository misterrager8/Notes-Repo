function folderCreate() {
    $.post('/folder_create', {
        name : $('#folderName').val()
    }, function(data) {
        $('#allFolders').load(location.href + ' #allFolders');
    });
    $('#folderName').val('');
}

function savePage(pageId) {
    $('#saveStatus').text('Saving...');
    $.post('editor', {
        id_ : pageId,
        title : $('#title').val(),
        folder_id : $('#folder_id').val(),
        content : $('#content').html()
    },
    function() {
        $('#saveStatus').text('Saved ' + Date(Date.now()));
    });
}

function folderUpdate(folderId) {
    $.post('folder_update', {
        id_ : folderId,
        name : $('#folderName' + folderId).val(),
        color : $('#folderColor' + folderId).val()
    }, function(data) {
        $('#allFolders').load(location.href + ' #allFolders');
    });
}

function deletePage(pageId) {
    $.get('page_delete', { id_ : pageId }, function(data) { $('#allPages').load(location.href + ' #allPages'); });
}

function deleteFolder(folderId) {
    $.get('folder_delete', { id_ : folderId }, function(data) { $('#allFolders').load(location.href + ' #allFolders'); });
}

function bookmarkPage(pageId) {
    $.get('mark_page', { id_ : pageId }, function(data) { $('#allPages').load(location.href + ' #allPages'); });
}

function hidePage(pageId) {
    $.get('page_visibility', { id_ : pageId }, function(data) { $('#allPages').load(location.href + ' #allPages'); });
}

function format(cmd, val) {
    document.execCommand(cmd, false, val);
}