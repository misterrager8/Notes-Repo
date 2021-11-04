function bold() {
    var v = document.getElementById("content");

    var selectedText = v.value.slice(v.selectionStart, v.selectionEnd);
    var before = v.value.slice(0, v.selectionStart);
    var after = v.value.slice(v.selectionEnd);

    var text = before + "**" + selectedText + "**" + after;
    v.innerHTML = text;
}

function italic() {
    var v = document.getElementById("content");

    var selectedText = v.value.slice(v.selectionStart, v.selectionEnd);
    var before = v.value.slice(0, v.selectionStart);
    var after = v.value.slice(v.selectionEnd);

    var text = before + "*" + selectedText + "*" + after;
    v.innerHTML = text;
}

function bullet() {
    var v = document.getElementById("content");

    var selectedText = v.value.slice(v.selectionStart, v.selectionEnd);
    var before = v.value.slice(0, v.selectionStart);
    var after = v.value.slice(v.selectionEnd);

    var text = before + "- " + selectedText + after;
    v.innerHTML = text;
}

function heading() {
    var v = document.getElementById("content");

    var selectedText = v.value.slice(v.selectionStart, v.selectionEnd);
    var before = v.value.slice(0, v.selectionStart);
    var after = v.value.slice(v.selectionEnd);

    var text = before + "# " + selectedText + after;
    v.innerHTML = text;
}

function hyperlink() {
    var v = document.getElementById("content");

    var selectedText = v.value.slice(v.selectionStart, v.selectionEnd);
    var before = v.value.slice(0, v.selectionStart);
    var after = v.value.slice(v.selectionEnd);

    var text = before + "[]()" + selectedText + after;
    v.innerHTML = text;
}

function code() {
    var v = document.getElementById("content");

    var selectedText = v.value.slice(v.selectionStart, v.selectionEnd);
    var before = v.value.slice(0, v.selectionStart);
    var after = v.value.slice(v.selectionEnd);

    var text = before + "        " + selectedText + after;
    v.innerHTML = text;
}

function toggleDiv(parentId, divId) {
    $('#' + divId).fadeToggle();
    if ($('#' + divId).css('display') == 'none') {
        $('#' + parentId).css('z-index', 1);
    } else {
        $('#' + parentId).css('z-index', 2);
    }
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
    $.post('editor?id_=' + $('#pageId').val(), { content : $('#content').val() }, function() { $('#saveStatus').text('Saved ' + Date(Date.now())); });
}