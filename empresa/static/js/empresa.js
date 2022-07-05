const urlSearchParams = new URLSearchParams(window.location.search);

const params = Object.fromEntries(urlSearchParams.entries());

params.category = params.category?? ''

function doFunction() {

  var s = document.getElementById("text-value").value;
  var url = `?category=${params.category}&title=${s}`

  console.log(url)

  var win = window.open(url, "_self");
  return false;
}

$(document).ready(function () {
  if(!params.category == '') {
    $(`a#${params.category}`).addClass("active")
  } else {
    $(`a#todo`).addClass("active")
  }
  $("a.page_marker").click(function () {
    $("a").removeClass("active");
    $(this).addClass("active");
  });
});

function navegacion() {
  window.location.search.split("=")[1]
}

function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

document.getElementById("hide").value = dataURL;
