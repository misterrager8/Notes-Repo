function bold() {
    var v = document.getElementById("content");

    var selectedText = v.value.slice(v.selectionStart, v.selectionEnd);
    var before = v.value.slice(0, v.selectionStart);
    var after = v.value.slice(v.selectionEnd);

    var text = before + "**" + selectedText + "**" + after;
    $('#content').val(text);
}

function italic() {
    var v = document.getElementById("content");

    var selectedText = v.value.slice(v.selectionStart, v.selectionEnd);
    var before = v.value.slice(0, v.selectionStart);
    var after = v.value.slice(v.selectionEnd);

    var text = before + "*" + selectedText + "*" + after;
    $('#content').val(text);
}

function bullet() {
    var v = document.getElementById("content");

    var selectedText = v.value.slice(v.selectionStart, v.selectionEnd);
    var before = v.value.slice(0, v.selectionStart);
    var after = v.value.slice(v.selectionEnd);

    var text = before + "- " + selectedText + after;
    $('#content').val(text);
}

function heading() {
    var v = document.getElementById("content");

    var selectedText = v.value.slice(v.selectionStart, v.selectionEnd);
    var before = v.value.slice(0, v.selectionStart);
    var after = v.value.slice(v.selectionEnd);

    var text = before + "#" + selectedText + after;
    $('#content').val(text);
}

function hyperlink() {
    var v = document.getElementById("content");

    var selectedText = v.value.slice(v.selectionStart, v.selectionEnd);
    var before = v.value.slice(0, v.selectionStart);
    var after = v.value.slice(v.selectionEnd);

    var text = before + "[]()" + selectedText + after;
    $('#content').val(text);
}

function code() {
    var v = document.getElementById("content");

    var selectedText = v.value.slice(v.selectionStart, v.selectionEnd);
    var before = v.value.slice(0, v.selectionStart);
    var after = v.value.slice(v.selectionEnd);

    var text = before + "        " + selectedText + after;
    $('#content').val(text);
}

$('#folderCreateForm').on('submit', function(event) {
    event.preventDefault();
    $.post('/add_folder', { name : $('#folderName').val() }, function(data) { $('#allFolders').load(location.href + ' #allFolders'); });
    $('#folderName').val('');
});

$('#pageContent').on('submit', function(event) {
    event.preventDefault();
    save();
});

function save() {
    $('#saveStatus').text('Saving...');
    $.post('editor?id_=' + $('#pageId').val(), { content : $('#content').val(), title : $('#title').val() },
        function() {
            $('#saveStatus').text('Saved ' + Date(Date.now()));
        });
}

function folderUpdate(folderId) {
    $.post('edit_folder', {
        id_ : folderId,
        name : $('#folderName' + folderId).val(),
        description : $('#folderDesc' + folderId).val(),
        color : $('#folderColor' + folderId).val()
    }, function(data) {
        $('#allFolders').load(location.href + ' #allFolders');
    });
}

function deletePage(pageId) {
    $.get('delete_page', { id_ : pageId }, function(data) { $('#allPages').load(location.href + ' #allPages'); });
}

function deleteFolder(folderId) {
    $.get('delete_folder', { id_ : folderId }, function(data) { $('#allFolders').load(location.href + ' #allFolders'); });
}

function bookmarkPage(pageId) {
    $.get('mark', { id_ : pageId }, function(data) { $('#allPages').load(location.href + ' #allPages'); });
}