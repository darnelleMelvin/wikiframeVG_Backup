// initialize global variables.

let my_edges;
let my_nodes;
let network;
let the_data;

// This method is responsible for drawing the graph, returns the drawn network
function drawGraph() {
  let container = document.getElementById('vis-container');
  // create objects for network
    try {
        my_nodes = new vis.DataSet(inbound_nodes);
        my_edges = new vis.DataSet(inbound_edges);

        // adding nodes and edges to the graph
        the_data = {nodes: my_nodes, edges: my_edges};
        let options = {
            interaction: {
                hover: true
            }
        };

        network = new vis.Network(container, the_data, options);
    } catch (err) {
        alert("There was a problem drawing the graph. " + err.toString())
    }
    initialize(network);
    return network;
}

//wrote this to explicitly initialize needed events. Couldn't make it work otherwise.
function initialize(net) {
    net.on('selectNode', function (params) {
        let s = document.getElementById('id_selected_text');
        s.value = params['nodes'][0];
        let label_data = getLabel(params['nodes'][0]);
        let color_data = getColorType(params['nodes'][0]);
        document.getElementById('id_shape_label').value = label_data;
        document.getElementById('id_color_type').value = color_data;
    })

    net.on('hoverNode', function (params) {
        try {
        tooltip_div.innerText = showProperties(params['node']);
        tooltip_div.style.left = mouse_x + 'px';
        tooltip_div.style.top = mouse_y + 'px';
        tooltip_div.hidden = false;
        } catch (err) {
            alert(err.message)
        }
    })

    net.on('blurNode', function () {
        tooltip_div.hidden = true;
    })

}

function setChecks() {
    //picks up js array of checkboxes to set, based on prior user selections.
    //checkboxes are referred to by ordinal position; 0. 1. 2...
    if (inbound_checks.length === 0) {
        $('#id_relation_types_0').prop('checked', true);
    } else {
        inbound_checks.forEach(function (c) {
            let the_key = '#id_relation_types_' + c.toString();
            $(the_key).prop('checked', true);
        });
    }
}

function getColorType(pitem_id) {
    //finds and returns color-as-guid for graph nodes.
    let color_data = _.find(inbound_nodes, function (o) //inbound nodes init on template render.
    {return o.id === pitem_id;}, 0);
    if (color_data['color']) {
        return color_data['color'];
    } else {
        alert("Could not find color!")
        return "#00BFFF"
    }
}
function getLabel(pitem_id) {
    try {
        let lbl;
        let label_data = _.find(js_objects, function (o) //js_objects init on window load.
            {return o.id === pitem_id;}, 0);
        if (label_data['label']) {
            lbl = label_data['label'];
        } else {
             lbl = label_data.itemprops['itemlabel'];
        }
        return lbl;
    } catch (err) {
        alert(err.message + " " + pitem_id);
    }
}
