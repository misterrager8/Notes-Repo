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

$('#folderCreateForm').on('submit', function(event) {
    event.preventDefault();
    $.post('/add_folder', { name : $('#folderName').val() }, function(data) { $('#allFolders').load(location.href + ' #allFolders'); });
    $('#folderName').val('');
});