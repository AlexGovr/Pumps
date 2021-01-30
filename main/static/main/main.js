
function set_visible(item_class) {
    document.querySelectorAll('.select').forEach(
      function(page) {
        page.hidden=true;
      }
    ) 
    document.querySelector(`.${item_class}`).hidden = false;
  };

// csrf_token 
function getCookie(name) {
  var cookieValue = null;
  var i = 0;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (i; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function table_add(table) {
  let row_num = table.children.length - 1;
  let row_template = document.querySelector('.select-table-row-template');
  let row = row_template.cloneNode();
  // let col_template = document.querySelector('.select-table-col-template');
  let scope = document.querySelector('.select-table-row-scope').cloneNode();
  let colnum = row_template.children.length - 1;

  table.append(row)

  row.hidden = false;
  row.append(scope);

  scope.innerHTML = row_num+1;
  for (let i=0; i<colnum; i++) {
    let col = document.createElement('td');
    col.innerHTML = '-'
    row.appendChild(col)
  }
}

addEventListener(
"DOMContentLoaded",
function() {
  //// switcher modes
  var table = document.querySelector('.select-table-rows');
  var page_items = document.querySelectorAll('.page-item');
  for (let i = 0; i < page_items.length; i++) {
    page_items[i].onclick = function() {
      set_visible(this.dataset.page);             
      table_add(table);
    }
  }

  //// form ajax button
  document.querySelector('.select-parameters-send').onclick = function() {

    let csrftoken = getCookie('csrftoken');
    
    // open and prepare request
    request = new XMLHttpRequest();
    request.open('POST', '/select/');
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.onload = function() {
      const data = JSON.parse(request.responseText)
      if (data.success) {
          console.log('success');
      }
    }

    // retrieve data to json
    let wpq = document.querySelector('.select-parameters-q').value;
    let wph = document.querySelector('.select-parameters-h').value;
    let datajson = {'wpq': wpq, 'wph': wph};
    // send request
    data = new FormData();
    data.append('marks', JSON.stringify(datajson));
    request.send(data);

    return false;
  }
}
);