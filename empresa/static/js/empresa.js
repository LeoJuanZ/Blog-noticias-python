

$(document).ready(function() {
    $('button').first().addClass('active');
    $('button.page_marker').click(function() {
        $('button').removeClass('active');
        $(this).addClass('active');
    });
});

function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

function doFunction(){
  var s = document.getElementById("text-value").value;
  var url = "?title=" + s;
  var win = window.open(url, '_self');
  return false;
}

document.getElementById("hide").value = dataURL;

console.log(document.getElementById("hide").value)