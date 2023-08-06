
function setTabClass(tab) {
  $('.tab').removeClass('active');
  $(`#${tab}`).addClass('active');
}

function setActiveTab(tab) {
  let urlParams = new URLSearchParams(window.location.search);
  urlParams.set('tab', tab);
  let url = document.location.pathname + "?" + urlParams.toString();
  window.history.replaceState(null, null, url);
  setTabClass(tab);
}


function addVariable() {

  let doc = $('.environment-list-item').first();
  let newEnv = doc.clone();
  newEnv.appendTo(".env-list");
  newEnv.find("input:text").val("");


}

function removeVar(el) {
  let row = $(el).parent().parent();

  if (row.hasClass('environment-list-item')) {
    row.remove();
  }

}

function addVar(vari) {
  let template = $('template')[0];
  let item = template.content.querySelector("div");
  let a = document.importNode(item, true);
  $('#env-list').append(a);

  let items = $('#env-list').find(".environment-list-item");
  const last = $(items).last();
  const lastInputs = $(last[0]).find("input[type=text]");

  if (vari) {
    $(lastInputs[0]).val(vari.key);
    $(lastInputs[1]).val(vari.value);
  }

  for (let i = 0; i < items.length; i++) {

    const envInputs = $(items[i]).find("input[type=text]");

    $(items[i]).attr("name", "env" + i);

    $(envInputs[0]).attr('name', `keyval-${i}`);
    $(envInputs[1]).attr('name', `keyval-${i}`);
  }
}

function populateEnv(vars) {

  if (vars.env.length > 0) {
    for (let variable of vars.env) {
      addVar(variable);
    }
  }
  else {
    addVar();
  }

}