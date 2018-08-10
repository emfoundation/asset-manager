// If Jquery not imported, use django's built in version and set it to use $
if (!$) {
    $ = django.jQuery;
}

$(document).ready(function() {
  $input = $('#id_file');
  MAX_FILE_SIZE = 100000000;

  // Watch for file changes
  $input.on("change", function(e) {
    file_size = this.files[0].size;
    if (file_size >= MAX_FILE_SIZE) {
      // File too big, add error message
      $("<ul>")
        .addClass("errorlist filesize_exceeded")
        .append($("<li>")
          .text("The file you have selected is too large, please choose a file under 100MB and try again."))
        .insertBefore("#id_file");
      // Remove file from input
      $input.replaceWith($input.val('').clone(true));
      $('#id_file').css({"border":"1px solid #ba2121", "border-radius":"5px"});
    }
    else {
      // File not too big, remove error message and styling
      $(".filesize_exceeded").remove();
      $('#id_file').css("border", "none");
    }
  });
});

document.addEventListener("DOMContentLoaded", function(event) {
  const fileInput = document.querySelector('#id_file');
  const fileContainer = fileInput.parentElement;
  let errorList = document.createElement("ul");
  errorList.setAttribute('id', 'customErrorList');
  errorList.classList.add("errorlist");

  fileInput.addEventListener('change', function(){
    var fileName = fileInput.files[0].name;
    var re = /^[\w\-.]+$/;

    if (!re.test(fileName)) {
      // Add error
      var li = document.createElement("li");
      var node = document.createTextNode("Filename fail!");
      li.appendChild(node);
      errorList.appendChild(li);
      fileContainer.insertBefore(errorList, fileInput);

      // clear file
      fileInput.value = '';

      // add css
      fileInput.style.border = '1px solid #ba2121';
      fileInput.style.borderRadius = '5px';
    } else {
      fileInput.style.border = 'none';
      errorList.parentNode.removeChild(errorList);
    }
  });
});
