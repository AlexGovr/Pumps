
class GraphBoard {
    constructor(cls_name) {
        this.board = JXG.JSXGraph.initBoard(cls_name, {boundingbox:[0,5,5,0], axis:true})
        this.board_objects = []
    }

    draw(mark_data) {
        var q_points = mark_data['q_curve_points']
        var h_points = mark_data['h_curve_points']
        var p = []
        for (let i = 0; i < q_points.length; i++) {
            p[i] = this.board.create('point', [q_points[i], h_points[i]], {size: 4, face: 'o'});
            this.board_objects.push(p[i])
        }
        var spline = this.board.create('spline', p, {strokeWidth:3})
        this.board_objects.push(spline)
        this.adjust_scale(q_points, h_points)
    }

    adjust_scale(x, y) {
        var xmin, xmax, ymin, ymax
        xmin = x[0] - 0.5
        xmax = x['length'] + 0.5
        ymax = y[0] + 0.5
        ymin = y['length'] - 0.5
        this.board.setBoundingBox([xmin, ymax, xmax, ymin])
    }

    clear() {
        while (this.board_objects.length) {
            this.board.removeObject(this.board_objects.pop())
        }
    }
    

    
}

var indextokey, list_indextokey, table, select_list, graph_board, board_objects = [], data;
var best_indices, best_indextokey;

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
                        best_indextokey = data['best_indextokey']
                    })
        
        //// create graph boards
        graph_board = new GraphBoard('jxgbox')
        graph_board_p2 = JXG.JSXGraph.initBoard('jxgbox_p2', {boundingbox:[0,37,2,0], axis:true})
        graph_board_eff = JXG.JSXGraph.initBoard('jxgbox_eff', {boundingbox:[0,37,2,0], axis:true})
        graph_board_npsh = JXG.JSXGraph.initBoard('jxgbox_npsh', {boundingbox:[0,37,2,0], axis:true})
        // bound with corresponding toggle-buttons
        document.querySelector('.select-curve-check-p2').dataset.board_class = 'jxgbox_p2'
        document.querySelector('.select-curve-check-eff').dataset.board_class = 'jxgbox_eff'
        document.querySelector('.select-curve-check-npsh').dataset.board_class = 'jxgbox_npsh'
        document.querySelector('.select-curve-check-p2').onclick = selectcheck_onclick
        document.querySelector('.select-curve-check-eff').onclick = selectcheck_onclick
        document.querySelector('.select-curve-check-npsh').onclick = selectcheck_onclick
    }
)


function go_select() {
    // retrieve data to json
    let wpq = document.querySelector('.select-parameters-q').value;
    let wph = document.querySelector('.select-parameters-h').value;
    let datajson = {'wpq': wpq, 'wph': wph};
    // send request
    data = new FormData();
    data.append('parameters', JSON.stringify(datajson));
    ajax_request('/mark/select/', data, 
                    function() {
                    var all_data = JSON.parse(this.responseText)
                    data = all_data['all']
                    best_indices = all_data['best']
                    table_reset(data);
                    // graph_draw(data[0]);
                    graph_board.clear()
                    graph_board.draw(data[0])
                    best_reset(data, best_indices)
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
}

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
    for (var key of Object.keys(indextokey)) {
        let col = document.createElement('td');
        col.innerHTML = get_deep(data, indextokey[key]);
        row.appendChild(col)
    }
    // fill select list
    list_scope.innerHTML = row_num+1
    list_row.onclick = selectlistrow_onclick
    list_row.dataset['index'] = index
    for (var key of Object.keys(list_indextokey)) {
        let col = document.createElement('td')
        col.innerHTML = get_deep(data, indextokey[key])
        list_row.appendChild(col)
    }
}

function best_reset(data, indices) {
    for (var key of Object.keys(indices)) {
        var class_name = `.best-solutions-table-row-${key}`
        var tbl_row = document.querySelector(class_name)
        var tbl_cols = tbl_row.children
        var pump_index = indices[key]
        // clear if no data
        if (pump_index == null) {
            for (var col_i of Object.keys(best_indextokey)) {
                var col_key = best_indextokey[col_i]
                tbl_cols[col_i].innerHTML = '-'
                tbl_row.onclick = null
            }
            continue
        }
        // fill
        var best_pump_index = indices[key] 
        var pump_data = data[best_pump_index]
        for (var col_i of Object.keys(best_indextokey)) {
            var col_key = best_indextokey[col_i]
            bestrow = tbl_cols[col_i]
            bestrow.innerHTML = get_deep(pump_data, col_key)
        }

        // make clickable
        tbl_row.onclick = bestrow_onclick
        tbl_row.dataset['index'] = best_pump_index
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
    graph_board.clear()
    graph_board.draw(data[index])
    // graph_clear()
    // graph_draw(data[index])
}

//// toggling check-buttons
function selectcheck_onclick() {
    var board = document.querySelector(`.${this.dataset.board_class}`)
    board.hidden = !board.hidden
}

//// clickable best tables
function bestrow_onclick() {
    var index = this.dataset['index']
    graph_clear()
    graph_draw(data[index])
    set_visible('select-curve')
}