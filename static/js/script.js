let dropArea = document.getElementById('drop-area');
let fileElem = document.getElementById('fileElem');
let previewArea = document.getElementById('markdown-content');
let downloadBtn = document.getElementById('download-btn');
let usageCountSpan = document.getElementById('count');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    dropArea.classList.add('highlight');
}

function unhighlight(e) {
    dropArea.classList.remove('highlight');
}

dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    let dt = e.dataTransfer;
    let files = dt.files;
    handleFiles(files);
}

function handleFiles(files) {
    ([...files]).forEach(uploadFile);
}

function uploadFile(file) {
    let url = '/';
    let formData = new FormData();

    formData.append('file', file);

    fetch(url, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            alert(result.error);
        } else {
            previewArea.innerHTML = marked(result.markdown);
            downloadBtn.style.display = 'block';
            downloadBtn.onclick = () => downloadMarkdown(result.markdown);
            updateUsageCount(result.usage_count);
        }
    })
    .catch(() => {
        alert('发生错误，请重试。');
    });
}

function updateUsageCount(count) {
    usageCountSpan.textContent = count;
}

function downloadMarkdown(content) {
    let blob = new Blob([content], {type: 'text/markdown'});
    let url = URL.createObjectURL(blob);
    let a = document.createElement('a');
    a.href = url;
    a.download = 'formatted_conversation.md';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
//目录
