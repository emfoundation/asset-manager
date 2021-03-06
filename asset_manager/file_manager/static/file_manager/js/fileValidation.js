document.addEventListener("DOMContentLoaded", function(event) {
  const fileInput = document.querySelector('#id_file');
  const errorList = document.createElement("ul");
  errorList.setAttribute('id', 'customErrorList');
  errorList.classList.add("errorlist");
  fileInput.parentElement.insertBefore(errorList, fileInput);

  fileInput.addEventListener('change', function(){
    // test filename
    var fileName = fileInput.files[0].name;
    var re = /^[\w\-.]+$/;

    let errorId = 'filenameError';
    if (!re.test(fileName)) {
      let msg = `Invalid file name: ${fileName}. ` + config.FILE_NAME_ERROR
      createError(errorId, msg, errorList);
    } else {
      removeError(errorId);
    }

    errorId = 'filesizeError';
    if (fileInput.files[0].size > config.MAX_UPLOAD_SIZE) {
      let msg = `File size of ${Math.floor(fileInput.files[0].size/1000000)}mb is too large. ` + config.FILE_SIZE_ERROR
      createError(errorId, msg, errorList);
    } else {
      removeError(errorId);
    }

    // clear file and set styling
    fileInput.style.marginLeft = 0;
    if (errorList.childElementCount > 0) {
      fileInput.value = '';
      fileInput.style.border = '1px solid #ba2121';
      fileInput.style.borderRadius = '5px';
      if (errorList.childElementCount > 1) {
        fileInput.style.marginLeft = '160px';
      }
    } else {
      fileInput.style.border = 'none';
    }
  });
});

function createError(errorId, errorMsg, errorList) {
  let error = document.getElementById(errorId);
  if (!error) {
    let li = document.createElement("li");
    li.setAttribute('id', errorId);
    let node = document.createTextNode(errorMsg);
    li.appendChild(node);
    errorList.appendChild(li);
  } else {
    if (error.childNodes[0].nodeValue != errorMsg) {
      error.childNodes[0].nodeValue = errorMsg;
    }
  }
}

function removeError(errorId) {
  let li = document.getElementById(errorId);
  if (li) {li.parentNode.removeChild(li)};
}
