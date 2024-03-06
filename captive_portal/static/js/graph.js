$(".opt-periodo").click(function () {
    let last_date = $(this).text();
    let token = $("input[name=csrfmiddlewaretoken]").val();
    let action = 'last_date'
    $.ajax({
        url: "/action/",
        type: "post",
        data: {
            "last_date": last_date,
            "csrfmiddlewaretoken": token,
            "action": action
        },
        success: function (data) {
            //atualiza a página
            location.reload();
        }
    });
});
/**####################################################################### */
/*gráfico que mostra a quantidade de acessos por dia, no mês escolhido */
var ctx = document.getElementById('graphMounth').getContext('2d');


/*converte os dados recebidos do django para json*/
let data_by_mounth_gov = JSON.parse(data_by_mounth_gov_str);
let data_by_mounth_ufsm = JSON.parse(data_by_mounth_ufsm_str);
let data_by_mounth_eduroam = JSON.parse(data_by_mounth_eduroam_str);


let label_mounth_day_gov = [];
let label_mounth_day_ufsm = [];
let label_mounth_day_eduroam = [];

let data_qtd_by_day_gov = [];
let data_qtd_by_day_ufsm = [];
let data_qtd_by_day_eduroam = [];


for (let i = 0; i < data_by_mounth_gov.length; i++) {
    label_mounth_day_gov.push(data_by_mounth_gov[i].date);
    data_qtd_by_day_gov.push(data_by_mounth_gov[i].qtd);
}

for (let i = 0; i < data_by_mounth_ufsm.length; i++) {
    label_mounth_day_ufsm.push(data_by_mounth_ufsm[i].date);
    data_qtd_by_day_ufsm.push(data_by_mounth_ufsm[i].qtd);
}

for (let i = 0; i < data_by_mounth_eduroam.length; i++) {
    label_mounth_day_eduroam.push(data_by_mounth_eduroam[i].date);
    data_qtd_by_day_eduroam.push(data_by_mounth_eduroam[i].qtd);
}

var accessByDay = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: label_mounth_day_gov,
        datasets: [{
            label: 'Gov.Br',
            data: data_qtd_by_day_gov,
            backgroundColor: [
                'rgba(255, 255, 0, 0.7)',
            ],
            borderColor: [
                'rgba(0, 100, 0, 1)',
            ],
            borderWidth: 3
        },
        {
            label: 'UFSM',
            data: data_qtd_by_day_ufsm,
            backgroundColor: [
                'rgba( 0, 0, 139, 0.8)',
            ],
            borderColor: [
                'rgba(0, 0, 255, 1)',
            ],
            borderWidth: 1
        },
        {
            label: 'eduroam',
            data: data_qtd_by_day_eduroam,
            backgroundColor: [
                'rgba(255, 127, 80, 1)',
            ],
            borderColor: [
                'rgba(0, 0, 0, 1)',
            ],
            borderWidth: 1
        }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                position: 'bottom',
            }
        },
        title: {
            display: true,
            text: 'Acessos por dia',
        },
    }
});
/**####################################################################### */
/**####################################################################### */

/*gráfico que mostra a quantidade de acessos por mês durante o ano*/
var ctx = document.getElementById('graphYear').getContext('2d');
let data_mounth_year_gov = JSON.parse(data_mounth_year_str);
let data_mounth_year_ufsm = JSON.parse(data_mounth_year_ufsm_str);
let data_mounth_year_eduroam = JSON.parse(data_mounth_year_eduroam_str);
/** ### */
let label_mounth_year_gov = [];
let label_mounth_year_ufsm = [];
let label_mounth_year_eduroam = [];

let data_qtd_by_mounth_gov = [];
let data_qtd_by_mounth_ufsm = [];
let data_qtd_by_mounth_eduroam = [];


/** ### */
for (let i = 0; i < data_mounth_year_gov.length; i++) {
    label_mounth_year_gov.push(data_mounth_year_gov[i].date);
    data_qtd_by_mounth_gov.push(data_mounth_year_gov[i].qtd);
}
/** ### */
for (let i = 0; i < data_mounth_year_ufsm.length; i++) {
    label_mounth_year_ufsm.push(data_mounth_year_ufsm[i].date);
    data_qtd_by_mounth_ufsm.push(data_mounth_year_ufsm[i].qtd);
}

/** ### */
for (let i = 0; i < data_mounth_year_eduroam.length; i++) {
    label_mounth_year_eduroam.push(data_mounth_year_eduroam[i].date);
    data_qtd_by_mounth_eduroam.push(data_mounth_year_eduroam[i].qtd);
}


var accessByMounth = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: label_mounth_year_gov,
        datasets: [{
            label: 'Gov.Br',
            data: data_qtd_by_mounth_gov,
            backgroundColor: [
                'rgba(255, 255, 0, 0.7)',
            ],
            borderColor: [
                'rgba(0, 100, 0, 1)',
            ],
            borderWidth: 1
        },
        {
            label: 'UFSM',
            data: data_qtd_by_mounth_ufsm,
            backgroundColor: [
                'rgba( 0, 0, 139, 0.8)',
            ],
            borderColor: [
                'rgba(0, 0, 255, 1)',
            ],
            borderWidth: 1
        },
        {
            label: 'eduroam',
            data: data_qtd_by_mounth_eduroam,
            backgroundColor: [
                'rgba(255, 127, 80, 1)',
            ],
            borderColor: [
                'rgba(0, 0, 0, 1)',
            ],
            borderWidth: 1
        }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                position: 'bottom',
            }
        },
        title: {
            display: true,
            text: 'Acessos por mês',
        },

    }
});

/** Grafico Gov.Br. Uso interno e externo */
var ctxIntExt = document.getElementById('graphGovIntExt').getContext('2d');

let data_mounth_year_gov_intext = JSON.parse(data_mounth_year_gov_intext_str);

let data_mounth_year_gov_int = JSON.parse(data_mounth_year_gov_int_str);
let data_mounth_year_gov_ext = JSON.parse(data_mounth_year_gov_ext_str);
/** ### */
let label_mounth_year_gov_intext = [];
let label_mounth_year_gov_int = [];
let label_mounth_year_gov_ext = [];

let data_qtd_by_mounth_gov_intext = [];
let data_qtd_by_mounth_gov_int = [];
let data_qtd_by_mounth_gov_ext = [];

/** ### */
for (let i = 0; i < data_mounth_year_gov_intext.length; i++) {
    label_mounth_year_gov_intext.push(data_mounth_year_gov_intext[i].date);
    data_qtd_by_mounth_gov_intext.push(data_mounth_year_gov_intext[i].qtd);
}

/** ### */
for (let i = 0; i < data_mounth_year_gov_int.length; i++) {
    label_mounth_year_gov_int.push(data_mounth_year_gov_int[i].date);
    data_qtd_by_mounth_gov_int.push(data_mounth_year_gov_int[i].qtd);
}

/** ### */
for (let i = 0; i < data_mounth_year_gov_ext.length; i++) {
    label_mounth_year_gov_ext.push(data_mounth_year_gov_ext[i].date);
    data_qtd_by_mounth_gov_ext.push(data_mounth_year_gov_ext[i].qtd);
}


var accessGovIntExt = new Chart(ctxIntExt, {
    type: 'bar',
    data: {
        labels: label_mounth_year_gov_intext,
        datasets: [{
            label: 'Gov.Br',
            data: data_qtd_by_mounth_gov_intext,
            backgroundColor: [
                'rgba(255, 255, 0, 0.7)',
            ],
            borderColor: [
                'rgba(0, 100, 0, 1)',
            ],
            borderWidth: 1
        },
        {
            label: 'Interno',
            data: data_qtd_by_mounth_gov_int,
            backgroundColor: [
                'rgba( 0, 0, 139, 0.8)',
            ],
            borderColor: [
                'rgba(0, 0, 255, 1)',
            ],
            borderWidth: 1
        },
        {
            label: 'Externo',
            data: data_qtd_by_mounth_gov_ext,
            backgroundColor: [
                'rgba(0, 255, 0, 1)',
            ],
            borderColor: [
                'rgba(0, 0, 0, 1)',
            ],
            borderWidth: 1
        }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                position: 'bottom',
            }
        },
        title: {
            display: true,
            text: 'Acessos Gov.Br',
        },
    }
});




/**####################################################################### */
/**#####################     actions                ####################### */
/**####################################################################### */


function saveLog() {
    console.log("Salvando logs de hoje");
    let action = 'saveLogs';
    let token = $("input[name=csrfmiddlewaretoken]").val();
    $("#msg_update").html(`<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>`);
    $("#modalTitleUpdate").text("Salvando Logs...");
    $.ajax({
        url: "/action/",
        type: "post",
        data: {
            "csrfmiddlewaretoken": token,
            "action": action
        },
        success: function () {
            $("#modalTitleUpdate").text("Finalizado com sucesso");
            $("#msg_update").html("<h3>Atualizado!</h3><br>");
        },
        error: function () {
            $("#msg_update").html("<h3>Erro ao salvar logs!</h3><br>");
        }
    });
}

function filterLog() {
    let action = 'filterLogs';
    let token = $("input[name=csrfmiddlewaretoken]").val();
    $("#modalTitleUpdate").text("Filtrando Logs...");
    $("#msg_update").html(`<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>`);
    $.ajax({
        url: "/action/",
        type: "post",
        data: {
            "csrfmiddlewaretoken": token,
            "action": action
        },
        success: function () {
            saveLog();
            //atualiza página
            location.reload();



        },
        error: function () {
            $("#msg_update").html("<h3>Erro ao filtrar logs!</h3><br>");
        }
    });
}


$("#getLogsTodayNow").click(function () {
    console.log("Buscando logs de hoje");
    let token = $("input[name=csrfmiddlewaretoken]").val();
    let action = 'getLogsTodayNow'
    $.ajax({
        url: "/action/",
        type: "post",
        data: {
            "csrfmiddlewaretoken": token,
            "action": action
        },
        success: function () {
            filterLog();
        },
        error: function () {
            $("#msg_update").html("<h3>Erro ao obter logs!</h3><br>");
        }
    });
});