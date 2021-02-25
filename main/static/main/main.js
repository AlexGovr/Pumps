
var indextokey, list_indextokey, table, select_list, graph_board, board_objects = [], data, best_indices;

//// init 
addEventListener(
    "DOMContentLoaded",
    function() {
        table = document.querySelector('.select-table-rows');
        select_list = document.querySelector('.select-list-rows');
        //// switcher modes
        var page_items = document.querySelectorAll('.page-item');
        for (let i = 0; i < page_items.length; i++) {
            page_items[i].onclick = function() {
                set_visible(this.dataset.page);             
            }
        }

        //// form ajax button
        document.querySelector('.select-parameters-send').onclick = go_select

        // get initial data
        ajax_request('/init/select', data=new FormData(), 
                    function() {
                        var data = JSON.parse(this.responseText);
                        indextokey = data['indextokey']
                        list_indextokey = data['list_indextokey']
                    })
        
        //// create graph board
        graph_board = JXG.JSXGraph.initBoard('jxgbox', {boundingbox:[0,37,2,0], axis:true})
    }
);


function go_select() {
    // retrieve data to json
    let wpq = document.querySelector('.select-parameters-q').value;
    let wph = document.querySelector('.select-parameters-h').value;
    let datajson = {'wpq': wpq, 'wph': wph, 'eqtype': '1s'};
    // send request
    data = new FormData();
    data.append('parameters', JSON.stringify(datajson));
    ajax_request('/mark/select/', data, 
                    function() {
                    var all_data = JSON.parse(this.responseText)
                    data = all_data['all']
                    best_indices = all_data['best']
                    table_reset(data);
                    graph_draw(data[0]);
                    })
    return false;
}


function ajax_request(url, data, handler) {
    let csrftoken = getCookie('csrftoken');
    // open and prepare request
    request = new XMLHttpRequest();
    request.open('POST', url);
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.send(data);
    request.onload = handler;
}

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
    table_clear();
    for (let i=0; i<data.length; i++) {
        table_add(data[i], i);
    }
}

function table_clear() {
    var left = document.querySelector('.reset');
        while (left) {
            left.remove();
            var left = document.querySelector('.reset');
    }
}

function table_add(data, index) {
    let row_num = table.children.length - 1;

    let row = document.querySelector('.select-table-row-template').cloneNode();
    let scope = document.querySelector('.select-table-row-scope').cloneNode();
    let list_row = document.querySelector('.select-list-row-template').cloneNode()
    let list_scope = document.querySelector('.select-list-row-scope').cloneNode();
    // add class to remove tag later
    row.classList.add('reset');
    list_row.classList.add('reset');

    table.append(row)
    select_list.append(list_row)

    row.hidden = false;
    row.append(scope);
    list_row.hidden = false
    list_row.append(list_scope)

    // fill table
    scope.innerHTML = row_num+1;
    for (var key in Object.keys(indextokey)) {
        let col = document.createElement('td');
        col.innerHTML = get_deep(data, indextokey[key]);
        row.appendChild(col)
    }
    // fill select list
    list_scope.innerHTML = row_num+1
    list_row.onclick = selectlistrow_onclick
    list_row.dataset['index'] = index
    for (var key in Object.keys(list_indextokey)) {
        let col = document.createElement('td')
        col.innerHTML = get_deep(data, indextokey[key])
        list_row.appendChild(col)
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

function graph_draw(mark_data) {
    graph_clear()
    var q_points = mark_data['q_curve_points']
    var h_points = mark_data['h_curve_points']
    var p = []
    for (let i = 0; i < q_points.length; i++) {
        p[i] = graph_board.create('point', [q_points[i], h_points[i]], {size: 4, face: 'o'});
        board_objects.push(p[i])
    }
    var spline = graph_board.create('spline', p, {strokeWidth:3})
    board_objects.push(spline)
}

function graph_clear() {
    while (board_objects.length) {
        graph_board.removeObject(board_objects.pop())
    }
}

//// clickable select list
function selectlistrow_onclick() {
    var index = this.dataset['index']
    graph_clear()
    graph_draw(data[index])
}