
var indextokey, table;

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
          name += '=';
          let cookie = cookies[i];
          let ind = cookie.search();
          if (ind >= 0){
            cookieValue = decodeURIComponent(cookie.substring(name.length + ind));
          }
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 2) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 2));
              break;
          }
      }
  }
  return cookieValue;
}

function table_reset(data){
  console.log('here');
  table_clear();
  for (let i=0; i<data.length; i++) {
    table_add(data[i]);
  }
}

function table_clear() {
  var left = document.querySelector('.reset');
  while (left) {
    left.remove();
    var left = document.querySelector('.reset');
  }
}

function table_add(data) {
  let row_num = table.children.length - 1;
  let row_template = document.querySelector('.select-table-row-template');
  let row = row_template.cloneNode();
  // add class to remove tag later
  row.classList.add('reset');
  // let col_template = document.querySelector('.select-table-col-template');
  let scope = document.querySelector('.select-table-row-scope').cloneNode();
  let colnum = row_template.children.length - 1;

  table.append(row)

  row.hidden = false;
  row.append(scope);

  scope.innerHTML = row_num+1;
  for (let i=0; i<colnum; i++) {
    let col = document.createElement('td');
    col.innerHTML = get_deep(data, indextokey[i]);
    row.appendChild(col)
  }
}

function get_deep(data, strpath) {
  var keys = strpath.split('-');
  var val = data[keys[0]];
  for (let i = 1; i < keys.length; i++) {
    if (!(keys[i] in val)) {
      return null;
    }
    val = val[keys[i]];
  }
  return val
}

addEventListener(
"DOMContentLoaded",
function() {
  indextokey = {
    0: 'eqtype-eqmodel-manufacturer-name',
    1: 'eqtype-eqmodel-eqmodel',
    2: 'eqmark',
    3: 'eqmark',
    4: 'eqmark',
    5: 'eqmark',
    6: 'eqmark',
    7: 'eqmark',
    8: 'eqmark',
    9: 'eqmark',
  }
  table = document.querySelector('.select-table-rows');
  //// switcher modes
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
    request.open('POST', '/mark/select/');
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.onload = function() {
      const data = JSON.parse(request.responseText)
      console.log('success');
      table_reset(data);
    }

    // retrieve data to json
    let wpq = document.querySelector('.select-parameters-q').value;
    let wph = document.querySelector('.select-parameters-h').value;
    let datajson = {'wpq': wpq, 'wph': wph, 'eqtype': '1s'};
    // send request
    data = new FormData();
    data.append('parameters', JSON.stringify(datajson));
    request.send(data);
    return false;
  }
}
);