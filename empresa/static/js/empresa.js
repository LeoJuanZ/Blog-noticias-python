

$(document).ready(function() {
    $('button').first().addClass('activo');
    $('button.marcador').click(function() {
        $('button').removeClass('activo');
        $(this).addClass('activo');
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

