
function set_visible(item_class) {
    document.querySelectorAll('.select').forEach(
      function(page) {
        page.hidden=true;
      }
    ) 
    document.querySelector(`.${item_class}`).hidden = false;
  };

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
    // switch modes
    var table = document.querySelector('.select-table-rows');
    var page_items = document.querySelectorAll('.page-item');
    for (let i = 0; i < page_items.length; i++) {
    page_items[i].onclick = function() {
        set_visible(this.dataset.page);             
        table_add(table);
    }
    }
}
);