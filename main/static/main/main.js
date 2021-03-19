
class GraphBoard {
    constructor(tag_cls, data_field, wp_field) {
        this.board = JXG.JSXGraph.initBoard(tag_cls, {boundingbox:[0,5,5,0], axis:true})
        this.board_objects = {}
        this.x = {}
        this.y = {}
        this.data_field = data_field
        this.wp_field = wp_field
    }

    draw(mark_data, key) {
        var q_points = mark_data['q_curve_points']
        var y_points = mark_data[this.data_field]
        this.x[key] = q_points
        this.y[key] = y_points
        var p = []
        var mark_board_objects = []
        this.board_objects[key] = mark_board_objects
        for (var i in q_points) {
            p[i] = this.board.create('point', [q_points[i], y_points[i]]);
        }
        var spline = this.board.create('spline', p, {strokeWidth:3})
        mark_board_objects.push(spline)
        this.adjust_scale()
        // add working point
        var x_wp = mark_data['q_wp']
        var y_wp = mark_data[this.wp_field]
        var wp = this.board.create('point', [x_wp, y_wp], {size: 4, face: 'o'})
        mark_board_objects.push(wp)
        // remove spline points
        for (var i in p) {
            this.board.removeObject(p[i])
        }
    }

    adjust_scale() {
        var xmin, xmax, ymin, ymax
        xmin = xmax = ymin = ymax = 0
        for(var key of Object.keys(this.x)) {
            var x = this.x[key]
            var y = this.y[key]
            xmin = Math.min.apply(null, x.concat([xmin])) - 0.5
            xmax = Math.max.apply(null, x.concat([xmax])) + 0.5
            ymax = Math.max.apply(null, y.concat([ymax])) + 0.5
            ymin = Math.min.apply(null, y.concat([ymin])) - 0.5
        }
        this.board.setBoundingBox([xmin, ymax, xmax, ymin])
    }

    clear(key) {
        var mark_board_objects = this.board_objects[key]
        while (mark_board_objects.length) {
            this.board.removeObject(mark_board_objects.pop())
            delete this.board_objects[key]
            delete this.x[key]
            delete this.y[key]
        }
    }

    clearall() {
        for (key of Object.keys(this.board_objects)) {
            this.clear(key)
        }
    }

    is_drawn(index) {
        console.log(this.board_objects)
        return index in this.board_objects
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
        graph_board = new GraphBoard('jxgbox', 'h_curve_points', 'h_wp')
        graph_board_p2 = new GraphBoard('jxgbox_p2', 'p2_curve_points', 'p2_wp')
        graph_board_eff = new GraphBoard('jxgbox_eff', 'efficiency_curve_points', 'eff_wp')
        graph_board_npsh = new GraphBoard('jxgbox_npsh', 'npsh_curve_points', 'npsh_wp')
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
                    clearall_graphs()
                    draw_graphs(0)
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
    function _get_mark_data(id) {
        for(var ind in data) {
            if(data[ind]['id'] == id) {return ind}
        }
        return null
    }
    for (var key of Object.keys(indices)) {
        var class_name = `.best-solutions-table-row-${key}`
        var tbl_row = document.querySelector(class_name)
        var tbl_cols = tbl_row.children
        var pump_id = indices[key]
        // clear if no data
        if (pump_id == null) {
            for (var col_i of Object.keys(best_indextokey)) {
                var col_key = best_indextokey[col_i]
                tbl_cols[col_i].innerHTML = '-'
                tbl_row.onclick = null
            }
            continue
        }
        // fill
        var mark_index = _get_mark_data(pump_id)
        var mark_data = data[mark_index]
        for (var col_i of Object.keys(best_indextokey)) {
            var col_key = best_indextokey[col_i]
            bestrow = tbl_cols[col_i]
            bestrow.innerHTML = get_deep(mark_data, col_key)
        }

        // make clickable
        tbl_row.onclick = bestrow_onclick
        tbl_row.dataset['index'] = mark_index
    }
}

function get_deep(data, strpath) {
    var keys = strpath.split('-');
    console.log(data)
    var val = data[keys[0]];
    for (let i = 1; i < keys.length; i++) {
        if (!(keys[i] in val)) {
            return null;
        }
        val = val[keys[i]];
    }
    return val
}

function draw_graphs(index) {
    var mark_data = data[index]
    graph_board.draw(mark_data, index)
    graph_board_p2.draw(mark_data, index)
    graph_board_eff.draw(mark_data, index)
    graph_board_npsh.draw(mark_data, index)
}

function clear_graphs(index) {
    graph_board.clear(index)
    graph_board_p2.clear(index)
    graph_board_eff.clear(index)
    graph_board_npsh.clear(index)
}

function clearall_graphs() {
    graph_board.clearall()
    graph_board_p2.clearall()
    graph_board_eff.clearall()
    graph_board_npsh.clearall()
}

//// clickable select list
function selectlistrow_onclick() {
    var index = this.dataset['index']
    if (graph_board.is_drawn(index)) {
        clear_graphs(index)
    }
    else {
        draw_graphs(index)
    }
}

//// toggling check-buttons
function selectcheck_onclick() {
    var board = document.querySelector(`.${this.dataset.board_class}`)
    board.hidden = !board.hidden
}

//// clickable best tables
function bestrow_onclick() {
    var mark_index = this.dataset.index
    draw_graphs(mark_index)
    set_visible('select-curve')
}