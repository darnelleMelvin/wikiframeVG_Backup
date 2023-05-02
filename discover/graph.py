from .wd_utils import catch_err
from .enums import RelColor


def load_graph(dataset, relation_types, domain):
    """Loads graph visualizer with item, relations, and edges for all domains.
    Properties list created for on-page graph tooltip via JavaScript. """
    from django.utils.safestring import mark_safe
    from . import db
    import json

    try:
        # prepare two lists to use in Javascript on template.
        # get unique lists of nodes and edges, and a JSON
        # dict of properties by item for graph display.
        item_dict = {}
        relation_dict = {}
        props_dict = {}
        edge_dict = {}

        node_list = []
        edge_list = []
        props_list = []
        # create dictionaries (force uniqueness)
        for i in dataset:

            item_dict[i.item_id] = i.itemlabel
            if domain == 'people':
                props_dict[i.item_id] = {"itemlabel": i.itemlabel, "image": i.image, "dob": i.dob,
                                         "placeofbirth": i.placeofbirthlabel, "dateofdeath": i.dateofdeath,
                                         "placeofdeath": i.placeofdeathlabel,  "mother": i.motherlabel,
                                         "father": i.fatherlabel, "spouse": i.spouselabel,
                                         "child": i.childlabel, "relative": i.relativelabel}
            elif domain == 'corps':
                props_dict[i.item_id] = {"itemlabel": i.itemlabel, "instanceoflabel": i.instanceoflabel,
                                         "describedat": i.describedat,
                                         "inception": str(i.inception), "dissolved": str(i.dissolved),
                                         "locationlabel": i.locationlabel}
            elif domain == 'collections':
                props_dict[i.item_id] = {"itemlabel": i.itemlabel, "donatedbylabel": i.donatedbylabel,
                                         "colltypelabel": i.colltypelabel, "inventorynum": i.inventorynum,
                                         "describedat": i.describedat}
            elif domain == 'orals':
                props_dict[i.item_id] = {"itemlabel": i.itemlabel, "inventorynum": i.inventorynum,
                                         "describedat": i.describedat}

            for r in relation_types:
                if r == 'occupation':
                    if i.occupation_id:
                        relation_dict[i.occupation_id] = {"label": 'occup: ' + i.occupationlabel,
                                                          "color": RelColor.occup.value}
                        edge_dict[i.item_id + i.occupation_id] = \
                            {"from": i.item_id, "to": db.supply_val(i.occupation_id, 'string')}
                elif r == 'fieldofwork':
                    if i.fieldofwork_id:
                        relation_dict[i.fieldofwork_id] = {"label": 'field: ' + i.fieldofworklabel,
                                                           "color": RelColor.fow.value}
                        edge_dict[i.item_id + i.fieldofwork_id] = \
                            {"from": i.item_id, "to": db.supply_val(i.fieldofwork_id, 'string')}
                elif r == 'placeofbirth':
                    if i.placeofbirth_id:
                        edge_dict[i.item_id + i.placeofbirth_id] = \
                                {"from": i.item_id, "to": db.supply_val(i.placeofbirth_id, 'string')}
                        relation_dict[i.placeofbirth_id] = {"label": 'birth: ' + i.placeofbirthlabel,
                                                            "color": RelColor.pob.value}
                elif r == 'placeofdeath':
                    if i.placeofdeath_id:
                        relation_dict[i.placeofdeath_id] = {"label": 'death: ' + i.placeofdeathlabel,
                                                            "color": RelColor.pod.value}
                        edge_dict[i.item_id + i.placeofdeath_id] = \
                            {"from": i.item_id, "to": db.supply_val(i.placeofdeath_id, 'string')}
                elif r == 'instanceof':
                    if i.instanceof_id:
                        relation_dict[i.instanceof_id] = {"label": 'category: ' + i.instanceoflabel,
                                                          "color": RelColor.instanceof.value}
                        edge_dict[i.item_id + i.instanceof_id] = \
                            {"from": i.item_id, "to": i.instanceof_id}

                elif r == 'subject':
                    if i.subject_id:
                        relation_dict[i.subject_id] = {"label": 'subj: ' + i.subjectlabel,
                                                       "color": RelColor.subj.value}
                        edge_dict[i.item_id + i.subject_id] = \
                            {"from": i.item_id, "to": i.subject_id}

        # add item nodes
        for k, v in item_dict.items():
            obj1 = {"id": k, "label": v[:20] + '.', "shape": "ellipse", "color": RelColor.item.value}
            node_list.append(obj1)

        # add relation nodes
        for k, v in relation_dict.items():
            obj2 = {"id": k, "label": v['label'], "shape": "ellipse", "color": v['color']}
            node_list.append(obj2)
            props_list.append(obj2)  # add here to provide on-page label to access via javascript.
        # add edges
        for k, v in edge_dict.items():
            edge_list.append(v)

        # additional properties for items
        for k, v in props_dict.items():
            obj3 = {"id": k, "itemprops": v}
            props_list.append(obj3)

        props_json = json.dumps(props_list, separators=(",", ":"))  # creates ragged json of relation & item nodes

        results = {"nodes": mark_safe(node_list), "edges": mark_safe(edge_list), 'properties': mark_safe(props_json)}
        return results
    except Exception as e:
        errors = catch_err(e, "graph.load_graph")
        return errors
