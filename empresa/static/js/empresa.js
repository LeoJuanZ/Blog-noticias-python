$(document).ready(function () {
  // switch:
  //   finanza: $("#finanzas").addClass("active")
  $("a").first().addClass("active");
  $("a.page_marker").click(function () {
    $("a").removeClass("active");
    $(this).addClass("active");
  });
});

function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

console.log(window.location.search.split("=")[1])

function doFunction() {
  var s = document.getElementById("text-value").value;
  var url = "?title=" + s;
  var win = window.open(url, "_self");
  return false;
}

document.getElementById("hide").value = dataURL;

console.log(document.getElementById("hide").value);
