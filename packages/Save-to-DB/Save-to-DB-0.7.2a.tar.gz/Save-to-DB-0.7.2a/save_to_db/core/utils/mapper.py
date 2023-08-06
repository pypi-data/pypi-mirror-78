from collections import defaultdict
from weakref import WeakSet


class Mapper(object):
    """ This class automatically sets up reverse relations for all items. """
    
    def __init__(self):
        # [collection_id][item_cls] = list_of_items
        self._map = defaultdict(lambda: defaultdict(WeakSet))
    
    
    def __contains__(self, item):
        return item in self.__get_item_set(item)
    
    
    def __get_item_set(self, item):
        collection_id = item.get_collection_id()
        item_cls = item.get_item_cls()
        return self._map[collection_id][item_cls]
    
    
    def __get_item_collection_set(self, item):
        collection_id = item.get_collection_id()
        return self._map[collection_id]
    
    
    def item_created(self, item):
        """ Called when an instance of
        :py:class:`~save_to_db.core.item_base.ItemBase` is created.
        
        :param item: An instance of created item.
        """
        self.__get_item_set(item).add(item)
    
    
    def item_value_set(self, item, key, old_value, new_value):
        """ Called when an item attribute is set, for example:
        
            .. code-block:: Python
                
                item[key] = new_value
        
        :param item: An item whose attribute is set.
        :param key: Attribute name of the `item`.
        :param old_value: Old attribute value.
        :param new_value: New attribute value.
        """
        if item.is_bulk_item():
            return  # default value was set
        
        if key not in item.relations:
            return
        
        relation = item.relations[key]
        reverse_key = relation['reverse_key']
        
        this_item, that_item_new = item, new_value
        that_item_old = old_value
        
        if not reverse_key:
                return
        
        if relation['relation_type'].is_one_to_one():
        
            # reverse for old
            if that_item_old and reverse_key in that_item_old.data:
                del that_item_old.data[reverse_key]
            
            # reverse for new
            if that_item_new is None:
                return
        
            that_item_data = that_item_new.data
            if reverse_key in that_item_data and \
                    that_item_data is this_item.data:
                return
            that_item_new.data[reverse_key] = this_item
        
        elif relation['relation_type'].is_one_to_many():
            
            # reverse for old
            if that_item_old:
                for item_in_bulk in that_item_old.bulk:
                    del item_in_bulk.data[reverse_key]
            
            # reverse for new
            if that_item_new:
                for item_in_bulk in that_item_new.bulk:
                    item_in_bulk.data[reverse_key] = this_item
        
        elif relation['relation_type'].is_many_to_one():
            
            # reverse for old item
            if that_item_old:
                if item in that_item_old[reverse_key].bulk:
                    that_item_old[reverse_key].bulk.remove(item)
            
            # reverse for new item
            if that_item_new:
                if item not in that_item_new[reverse_key].bulk:
                    that_item_new[reverse_key].bulk.append(item)
        
        elif relation['relation_type'].is_many_to_many():
            
            # reverse for old item
            if that_item_old:
                for item_in_bulk in that_item_old.bulk:
                    if item in item_in_bulk[reverse_key].bulk:
                        item_in_bulk[reverse_key].bulk.remove(item)
            
            # reverse for new item
            if that_item_new:
                for item_in_bulk in that_item_new.bulk:
                    if item not in item_in_bulk[reverse_key].bulk:
                        item_in_bulk[reverse_key].bulk.append(item)
        
    
    def item_value_deleted(self, item, key, old_value):
        """ Called when an item attribute is deleted, for example:
        
            .. code-block:: Python
                
                del item[key]
        
        :param item: An item whose attribute is deleted.
        :param key: Deleted attribute name.
        :param old_value: Deleted attribute value.
        """
        if item.is_bulk_item():
            return  # default value deleted
        
        if key not in item.relations or old_value is None:
            return
        
        relation = item.relations[key]
        if not relation['reverse_key']:
            return
        
        if relation['relation_type'].is_one_to_one():
            if relation['reverse_key'] in old_value:
                del old_value.data[relation['reverse_key']]
        
        elif relation['relation_type'].is_one_to_many():
            for item_in_bulk in old_value.bulk:
                del item_in_bulk.data[relation['reverse_key']]
        
        elif relation['relation_type'].is_many_to_one():
            old_value[relation['reverse_key']].bulk.remove(item)
            
        elif relation['relation_type'].is_many_to_many():
            for item_in_bulk in old_value:
                item_in_bulk[relation['reverse_key']].bulk.remove(item)
    
    
    def __iter_pointing_items(self, item):
        collection_set = self.__get_item_collection_set(item)
        for that_item_cls in collection_set:
            for that_item in collection_set[that_item_cls]:
                
                for key in set(that_item.data):
                    if that_item.data[key] is item:
                        yield key, that_item

    
    def item_deleted(self, item):
        """ Called when an item is deleted, for example:
        
            .. code-block:: Python
                
                item.delete()
        
        :param item: Deleted item.
        """
        # clearing the item
        # (defaults in bulk items and directs in single items)
        item.data.clear()
        
        for key, that_item in self.__iter_pointing_items(item):
            relation_type = that_item.relations[key]['relation_type']
            reverse_key = that_item.relations[key]['reverse_key']
            if reverse_key:
                if item.is_bulk_item() and relation_type.is_one_to_many():
                    for item_in_bulk in item.bulk:
                        del item_in_bulk.data[reverse_key]
                elif item.is_bulk_item() and item.bulk and \
                        relation_type.is_many_to_many():
                    
                    for this_item_in_bulk in item.bulk:
                        that_bulk = this_item_in_bulk.data[reverse_key]
    
                        for that_item_in_bulk in that_bulk.bulk:
                            
                            if that_item_in_bulk.data[key] is item:
                                that_bulk.bulk.remove(that_item_in_bulk)
            
            # defaults in bulk items and directs in single items
            del that_item.data[key]
                
        # removing from any bulks
        if item.is_single_item():
            collection_set = self.__get_item_collection_set(item)
            for that_item_cls in collection_set:
                for that_item in collection_set[that_item_cls]:
                    if that_item.is_bulk_item():
                        if item in that_item.bulk:
                            that_item.bulk.remove(item)
        else:
            item.bulk.clear()
    
    
    def item_added_to_bulk(self, item, bulk_item):
        """ Called when an item is added to a bulk item, for example:
        
            .. code-block:: Python
                
                bulk_item.add(single_item)
        
        :param item: A single item added to the `bulk_item`.
        :param bulk_item: Bulk item containing `item`.
        """
        collection_set = self.__get_item_collection_set(item)
        
        for that_item_cls in set(collection_set.keys()):
            for that_item in set(collection_set[that_item_cls]):
                if not that_item.is_single_item():
                    continue
                
                for key in set(that_item.data):
                    if that_item.data[key] is not bulk_item:
                        continue
                    
                    relation = that_item.relations[key]
                    reverse_key = that_item.relations[key]['reverse_key']
                    if not reverse_key:
                        continue
                    
                    if relation['relation_type'].is_one_to_many():
                        item.data[reverse_key] = that_item
                        
                    elif relation['relation_type'].is_many_to_many():
                        if that_item not in item[reverse_key].bulk:
                            item[reverse_key].bulk.append(that_item)
    
    
    def item_removed_from_bulk(self, item, bulk_item):
        """ Called when an item is removed from a bulk item, for example:
        
            .. code-block:: Python
                
                bulk_item.remove(single_item)
        
        :param item: A single item removed from the `bulk_item`.
        :param bulk_item: Bulk item that was containing `item`.
        """
        collection_set = self.__get_item_collection_set(item)
        
        for that_item_cls in collection_set:
            for that_item in collection_set[that_item_cls]:
                if not that_item.is_single_item():
                    continue
                
                for key in set(that_item.data):
                    if that_item.data[key] is not bulk_item:
                        continue
                    
                    relation = that_item.relations[key]
                    reverse_key = that_item.relations[key]['reverse_key']
                    
                    if reverse_key:
                        if relation['relation_type'].is_one_to_many():
                            del item.data[reverse_key]
                             
                        elif relation['relation_type'].is_many_to_many():
                            if that_item in item.data[reverse_key].bulk:
                                item.data[reverse_key].bulk.remove(that_item)

mapper = Mapper()