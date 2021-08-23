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

function addInput() {
    var form_ = document.getElementById("form_");
    var input_ = document.createElement("input");
    input_.className = "form-control mb-2";
    input_.placeholder = "Name";
    input_.type = "text";
    input_.autocomplete = "off";
    input_.name = "name";

    form_.insertBefore(input_, document.getElementById("add_button"));
    input_.focus();
}