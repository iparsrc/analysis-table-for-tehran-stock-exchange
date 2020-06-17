let tbody = document.querySelector("tbody");
let mean_sum_beta = 0;
let mean_num_beta = 0;
let mean_sum_cov = 0;
let mean_num_cov = 0;
let mean_sum_sd = 0;
let mean_num_sd = 0;
let mean_sum_tr = 0;
let mean_num_tr = 0;
let mean_sum_cv = 0;
let mean_num_cv = 0;
let mean_beta;
let mean_cov;
let mean_sd;
let mean_tr;
let mean_cv;

const numToGroup = [
    "فعالیت های هنری، سرگرمی و خلاقانه",
    "خدمات فنی و مهندسی",
    "اطلاعات و ارتباطات",
    "رایانه و فعالیتهای وابسته یه آن",
    "فعالیت مهندسی، تجزیه، تحلیل و آزمایش فنی",
    "انبوه سازی، املاک و مستغلات",
    "صندوق سرمایه گذاری قابل معامله",
    "فعالیتهای کمکی به نهادهای مالی واسط",
    "بیمه وصندوق بازنشستگی به جز تامین اجتماعی",
    "واسطه گری های مالی و پولی",
    "مخابرات",
    "حمل و نقل آبی",
];

const calcMean = function() {
    mean_beta = (mean_sum_beta/mean_num_beta);
    mean_cov = (mean_sum_cov/mean_num_cov);
    mean_sd = (mean_sum_sd/mean_num_sd);
    mean_tr = (mean_sum_tr/mean_num_tr);
    mean_cv = (mean_sum_cv/mean_num_cv);
    if (Number.isNaN(mean_beta)) mean_beta = 0;
    if (Number.isNaN(mean_cov)) mean_cov = 0;
    if (Number.isNaN(mean_sd)) mean_sd = 0;
    if (Number.isNaN(mean_cv)) mean_cv = 0;
    let inHtm =  `<td class="tbody-header" title="میانگین صنعت" style="background-color: #c4ffba !important;">${"میانگین"}</td>`;
    inHtm +=   `<td title="${mean_beta}">${mean_beta.toFixed(2)}</td>`;
    inHtm +=   `<td title="${mean_cov}">${mean_cov.toFixed(2)}</td>`;
    inHtm +=   `<td title="${mean_sd}">${mean_sd.toFixed(2)}</td>`;
    inHtm +=   `<td title="${mean_tr}">${mean_tr.toFixed(2)}</td>`;
    inHtm +=   `<td title="${mean_cv}">${mean_cv.toFixed(2)}</td>`;
    let mean_node = document.createElement("tr");
    mean_node.innerHTML = inHtm;
    mean_node.className = "tr-mean";
    tbody.appendChild(mean_node);
    mean_sum_beta = 0;
    mean_num_beta = 0;
    mean_sum_cov = 0;
    mean_num_cov = 0;
    mean_sum_sd = 0;
    mean_num_sd = 0;
    mean_sum_tr = 0;
    mean_num_tr = 0;
    mean_sum_cv = 0;
    mean_num_cv = 0;
}

const groupData = function(group_num) {
    if (group_num != 1) {
        calcMean();
    }
    group_name = numToGroup[group_num-1];
    let node = document.createElement("tr");
    node.innerHTML = `<td colspan="6" class="td-group">${group_name}</td>`;
    tbody.appendChild(node);
}

const appendDataToTable = function(ticker, rBeta, rCov, rSd, rTr, rCv) {
    if (rBeta != "") {
        mean_sum_beta += +rBeta;
        mean_num_beta += 1;
    }
    if (rCov != "") {
        mean_sum_cov += +rCov;
        mean_num_cov += 1;
    }
    if (rSd != "") {
        mean_sum_sd += +rSd;
        mean_num_sd += 1;
    }
    if (rTr != "") {
        mean_sum_tr += +rTr;
        mean_num_tr += 1
    }
    if (rCv != "") {
        mean_sum_cv += +rCv;
        mean_num_cv += 1
    }
    htm = "";
    let beta = parseFloat(rBeta).toFixed(2);
    let cov = parseFloat(rCov).toFixed(2);
    let sd = parseFloat(rSd).toFixed(2);
    let tr = parseFloat(rTr).toFixed(2);
    let cv = parseFloat(rCv).toFixed(2);
    if (rBeta == "") beta = "-";
    if (rCov == "") cov = "-";
    if (rSd == "") sd = "-";
    if (rTr == "") tr = "-";
    if (rCv == "") cv = "-";
    htm += `<td class="tbody-header" title=${ticker}>${ticker}</td>`;
    htm += `<td title=${rBeta}>${beta}</td>`;
    htm += `<td title=${rCov} >${cov}</td>`;
    htm += `<td title=${rSd}>${sd}</td>`;
    htm += `<td title=${rTr}>${tr}</td>`;
    htm += `<td title=${rCv}>${cv}</td>`;
    let node = document.createElement("tr");
    node.className = "tr-group";
    node.innerHTML = htm;
    tbody.appendChild(node);
}

let vizData = function(time_delta) { // This function gets csv data from site and then adds data to table using d3.js librariy.
    let csv_file_url = "/beta/data/csv?time_delta=" + time_delta;
    let i = 0;
    let j = 0;
    tbody.textContent = "";
    d3.csv(csv_file_url)
        .then((data) => {
            let array_length = data.length;
            for (d of data) {
                if (+d.group_name != i && +d.group_name < 13) {
                    groupData(parseInt(d.group_name));
                    i++;
                }
                appendDataToTable(d.ticker, d.beta, d.cov, d.sd, d.tr, d.cv);
                j++;
                if (j == array_length) {
                    calcMean();
                }
            }
        });
}

// Defining timeDelta buttons.
const btn_m1 = document.querySelector("#m1");
const btn_m3 = document.querySelector("#m3");
const btn_m6 = document.querySelector("#m6");
const btn_m9 = document.querySelector("#m9");
const btn_y1 = document.querySelector("#y1");
const btn_y2 = document.querySelector("#y2");
const btn_y3 = document.querySelector("#y3");
const btn_manual = document.querySelector("#manual"); // TODO: Make manual mode.

const btn_list = [btn_m1, btn_m3, btn_m6, btn_m9, btn_y1, btn_y2, btn_y3, btn_manual];
const active_btns = function(btn) { // This function actives clicked timeDelta button and deactives other buttons.
    for (item of btn_list) {
        if (item == btn) {
            btn.className = "active";
            continue;
        }
        item.className = "";
    }
}

// First action.
vizData("m1");
active_btns(btn_m1);

// TimeDelta button acting when clicked.
btn_m1.addEventListener("click", () => {
    vizData("m1");
    active_btns(btn_m1);
});
btn_m3.addEventListener("click", () => {
    vizData("m3");
    active_btns(btn_m3);
});
btn_m6.addEventListener("click", () => {
    vizData("m6");
    active_btns(btn_m6);
});
btn_m9.addEventListener("click", () => {
    vizData("m9");
    active_btns(btn_m9);
});
btn_y1.addEventListener("click", () => {
    vizData("y1");
    active_btns(btn_y1);
});
btn_y2.addEventListener("click", () => {
    vizData("y2");
    active_btns(btn_y2);
});
btn_y3.addEventListener("click", () => {
    vizData("y3");
    active_btns(btn_y3);
});
btn_manual.addEventListener("click", () => {
    active_btns(btn_manual);
});