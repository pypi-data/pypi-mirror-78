function collapse() {

  let checkClass = ".collapsable"
  let className = "collapsed";
  let isCollapsed = $(checkClass).hasClass(className);
  if (isCollapsed) {
    $(checkClass).removeClass(className);
  }
  else {
    $(checkClass).addClass(className);
  }

  $.cookie(className, !isCollapsed, {path: '/'});
}

function filterServices() {

  let url = "/services";
  let category = document.getElementById("filter-category");
  let rows = document.getElementById("filter-rows");
  let page = document.getElementById("filter-page");
  let selectedCategory = category.options[category.selectedIndex].value;
  let selectedRows = rows.options[rows.selectedIndex].value;
  let queries = {}
  let query = ""
  if(selectedCategory !== 'all')
  {
    queries.category = selectedCategory;
    //url += `?category=${selectedCategory}`
  }
  if(selectedRows !== 10)
  {
    queries.rows = selectedRows;
  }

  if(Object.keys(queries).length > 0) {

    let esc = encodeURIComponent;
    query = Object.keys(queries)
    .map(k => esc(k) + '=' + esc(queries[k])).join('&');
  }
  if(query.length > 0)
  {
    query = '?' + query;
  }
  return query;
}

function applyFilters() {
  let url = "/services";
  let query = filterServices();

  window.location.href=url+query;
  
}

function gotoPage(page) {
  const url = "/services";
  let query = filterServices();
  if(query.length > 0) {
    query += `&page=${page}`;
  }
  else {
    query += `?page=${page}`;
  }
  
  window.location.href=url+query;
  
}

function resetFilters() {
  let url = "/services";
  window.location.href = url;
}