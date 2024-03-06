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

  /*$("#entrarComGovBr").click(function(e) {
        console.log("chegou aqui")
        var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        var param = 'solicita_gov'
        $.ajax({
            type: "get",
            url: "/gov/",
            data: {
                csrfmiddlewaretoken: token,
                'param': param
            },
            dataType: "json",
            success: function(response) {

            }
        });
    });*/
});
