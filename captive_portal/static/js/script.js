$(function () {
  $("#buttonSetGov").click(function (e) {
    e.preventDefault();
    $(".setInstitucional").hide();
    $(this).hide();
    $("#buttonsetInstitucional").show();
    $(".gov").show();
  });

  $("#buttonsetInstitucional").click(function (e) {
    e.preventDefault();
    $(".gov").hide();
    $(this).hide();
    $(".setInstitucional").show();
    $("#buttonSetGov").show();
    $("#buttonsetInstitucional").hide();
    $(".gov").hide();
  });

  $("#aceitar_termos").click(function (e) {
    $(".carregando").show();
  });
});
