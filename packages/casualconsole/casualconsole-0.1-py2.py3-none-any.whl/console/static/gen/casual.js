function collapse(){let checkClass=".collapsable"
let className="collapsed";let isCollapsed=$(checkClass).hasClass(className);if(isCollapsed){$(checkClass).removeClass(className);}
else{$(checkClass).addClass(className);}
$.cookie(className,!isCollapsed,{path:'/'});}
function filterServices(){let url="/services";let category=document.getElementById("filter-category");let rows=document.getElementById("filter-rows");let page=document.getElementById("filter-page");let selectedCategory=category.options[category.selectedIndex].value;let selectedRows=rows.options[rows.selectedIndex].value;let queries={}
let query=""
if(selectedCategory!=='all')
{queries.category=selectedCategory;}
if(selectedRows!==10)
{queries.rows=selectedRows;}
if(Object.keys(queries).length>0){let esc=encodeURIComponent;query=Object.keys(queries).map(k=>esc(k)+'='+esc(queries[k])).join('&');}
if(query.length>0)
{query='?'+query;}
return query;}
function applyFilters(){let url="/services";let query=filterServices();window.location.href=url+query;}
function gotoPage(page){const url="/services";let query=filterServices();if(query.length>0){query+=`&page=${page}`;}
else{query+=`?page=${page}`;}
window.location.href=url+query;}
function resetFilters(){let url="/services";window.location.href=url;}
function setTabClass(tab){$('.tab').removeClass('active');$(`#${tab}`).addClass('active');}
function setActiveTab(tab){let urlParams=new URLSearchParams(window.location.search);urlParams.set('tab',tab);let url=document.location.pathname+"?"+urlParams.toString();window.history.replaceState(null,null,url);setTabClass(tab);}
function addVariable(){let doc=$('.environment-list-item').first();let newEnv=doc.clone();newEnv.appendTo(".env-list");newEnv.find("input:text").val("");}
function removeVar(el){let row=$(el).parent().parent();if(row.hasClass('environment-list-item')){row.remove();}}
function addVar(vari){let template=$('template')[0];let item=template.content.querySelector("div");let a=document.importNode(item,true);$('#env-list').append(a);let items=$('#env-list').find(".environment-list-item");const last=$(items).last();const lastInputs=$(last[0]).find("input[type=text]");if(vari){$(lastInputs[0]).val(vari.key);$(lastInputs[1]).val(vari.value);}
for(let i=0;i<items.length;i++){const envInputs=$(items[i]).find("input[type=text]");$(items[i]).attr("name","env"+i);$(envInputs[0]).attr('name',`keyval-${i}`);$(envInputs[1]).attr('name',`keyval-${i}`);}}
function populateEnv(vars){if(vars.env.length>0){for(let variable of vars.env){addVar(variable);}}
else{addVar();}}