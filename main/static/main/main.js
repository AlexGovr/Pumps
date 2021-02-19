
var indextokey, table, graph_board, board_objects = [];

//// init 
addEventListener(
    "DOMContentLoaded",
    function() {
        table = document.querySelector('.select-table-rows');
        //// switcher modes
        var page_items = document.querySelectorAll('.page-item');
        for (let i = 0; i < page_items.length; i++) {
            page_items[i].onclick = function() {
                set_visible(this.dataset.page);             
            }
        }

        //// form ajax button
        document.querySelector('.select-parameters-send').onclick = function() {
            // retrieve data to json
            let wpq = document.querySelector('.select-parameters-q').value;
            let wph = document.querySelector('.select-parameters-h').value;
            let datajson = {'wpq': wpq, 'wph': wph, 'eqtype': '1s'};
            // send request
            data = new FormData();
            data.append('parameters', JSON.stringify(datajson));
            ajax_request('/mark/select/', data, 
                            function() {
                            const data = JSON.parse(this.responseText)
                            table_reset(data);
                            graph_draw(data);
                            })
            return false;
        }

        // get initial data
        ajax_request('/init/select', data=new FormData(), 
                    function() {
                        let data = JSON.parse(this.responseText);
                        indextokey = data['indextokey']
                    })
        
        //// create graph board
        graph_board = JXG.JSXGraph.initBoard('jxgbox', {boundingbox:[0,37,5,0], axis:true})
    }
);

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

function graph_draw(data) {
    graph_clear()
    var mark_data = data[0]
    var q_points = mark_data['q_curve_points']
    var h_points = mark_data['h_curve_points']
    var p = []
    for (let i = 0; i < q_points.length; i++) {
        p[i] = graph_board.create('point', [q_points[i], h_points[i]], {size: 4, face: 'o'});
        board_objects.push(p[i])
    }
    graph_board.create('spline', p, {strokeWidth:3})
}

function graph_clear() {
    while (board_objects.length) {
        graph_board.removeObject(board_objects.pop())
    }
}