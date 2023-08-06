from collections import defaultdict
from .merge_items import merge_items
from ..item_base import ItemBase
from save_to_db.exceptions import MultipleItemsMatch


def complete_item_structure(item):
    """ Takes an item, merges items that must point to same model (if allowed),
    checkes collisions and returns a structure like this:
    
        .. code-block:: Python
            
            {
                item_cls: [item_instance, ...],
                ...
            }
            
    Where keys are a subclasses of :py:class:`~.item.Item` and values are
    instances of that class.
    """
    top_item = item
    
    # item class to a list of instances
    structure = defaultdict(list)
    default_structure = defaultdict(list)
    
    __add_flat_item_to_structure(top_item, structure, default_structure)
    
    # merging items and checking collisions
    all_items = []
    for items in structure.values():
        all_items.extend(items)

    for item_cls in structure.keys():
        if item_cls.allow_merge_items:
            merge_items(top_item,
                        structure[item_cls], default_structure[item_cls],
                        all_items)
        else:
            __check_item_collisions(structure[item_cls])
     
    return structure


def __add_flat_item_to_structure(item, structure, default_structure,
                                 is_default_item=False):
    
    if is_default_item:
        store_to_structure = default_structure
    else:
        store_to_structure = structure
    
    if item.is_single_item():
        if item in store_to_structure[type(item)]:
            return
        store_to_structure[type(item)].append(item)
        
        for key in item.relations:
            if key not in item or item[key] is None:
                continue
            
            __add_flat_item_to_structure(
                item[key], store_to_structure, default_structure,
                is_default_item=is_default_item
            )
                        
    else:
        # defaults in bulk
        for key, default_item in item.data.items():
            if not isinstance(default_item, ItemBase):
                continue
            
            __add_flat_item_to_structure(
                default_item, store_to_structure, default_structure,
                is_default_item=True
            )
        
        # normal values in bulk
        for inner_item in item.bulk:
            __add_flat_item_to_structure(
                inner_item, store_to_structure, default_structure,
                is_default_item=is_default_item
            )


def __check_item_collisions(item_list):
    if not item_list:
        return
    
    # `item_list` must contain items of the same class
    getter_groups = item_list[0].getters
    
    if not getter_groups:
        return
    
    for left_item in item_list:
        for right_item in item_list:
            if left_item is right_item:
                continue
             
            for getters in getter_groups:
                same_by_group = True
                for key in getters:
                    if key not in left_item.data or key not in right_item.data \
                            or left_item[key] is None or \
                            left_item[key] != right_item[key]:
                        same_by_group = False
                        break
      
                     
                if same_by_group:
                    raise MultipleItemsMatch(None, left_item, right_item,
                                             getters)