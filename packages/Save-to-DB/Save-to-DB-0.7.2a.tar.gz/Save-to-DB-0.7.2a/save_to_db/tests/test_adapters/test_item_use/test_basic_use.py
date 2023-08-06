from save_to_db.exceptions import BulkItemOneToXDefaultError, WrongAlias
from save_to_db.core.item import Item
from save_to_db.utils.test_base import TestBase



class TestBasicUse(TestBase):
    
    ModelFieldTypes = None
    ModelGeneralOne = None
    ModelGeneralTwo = None
    
    
    @classmethod
    def setup_models(cls, aliased=False):
        cls.item_cls_manager.clear()
        
        dct_1 = {'model_cls': cls.ModelGeneralOne}
        dct_2 = {'model_cls': cls.ModelGeneralTwo}
        
        if aliased:
            dct_1.update({
                'aliases': {
                    'alias_1': 'two_1_1__f_integer',
                    'alias_2': 'two_x_x__one_1_1__f_integer',
                }
            })
            dct_2.update({
                'aliases': {
                    'alias_1__post': 'f_string',
                    'alias_2__post': 'one_x_1__alias_1',
                    'alias_3__post': 'one_x_x__two_1_x__alias_1__post',
                }
            })
        
        cls.ItemGeneralOne = type('ItemGeneralOne', (Item,), dct_1)
        cls.ItemGeneralTwo = type('ItemGeneralTwo', (Item,), dct_2)
        
        cls.ItemGeneralOne.complete_setup()
        cls.ItemGeneralTwo.complete_setup()
    
    
    def test_set_field(self):
        self.setup_models()

        #--- setting with correct keys ---
        item = self.ItemGeneralOne()
        item['f_integer'] = '10'
        item['two_1_1__f_string'] = 'one'
        item['two_1_1__one_1_x__f_string'] = 'two'
        item['two_1_1__one_x_x__two_x_1__f_string'] = 'three'
        bulk = item['two_1_1__one_x_x']
        bulk['f_integer'] = '20'
        bulk.gen(f_text='four')
        in_bulk_item = bulk.gen(f_text='five')
        # setting field by calling
        in_bulk_item(f_string='ITEM_CALL') 
        bulk(two_x_1__f_text='BULK_CALL')
        
        self.assertEqual(item['f_integer'], '10')
        self.assertEqual(item['two_1_1']['f_string'], 'one')
        self.assertEqual(item['two_1_1']['one_1_x']['f_string'], 'two')
        self.assertNotIn('two_x_1', item['two_1_1']['one_x_x'])
        self.assertEqual(item['two_1_1']['one_x_x']['two_x_1__f_string'],
                         'three')
        
        bulk = item['two_1_1__one_x_x']
        self.assertEqual(bulk['f_integer'], '20')
        self.assertEqual(bulk[0]['f_text'], 'four')
        
        self.assertEqual(bulk[1]['f_text'], 'five')
        
        self.assertEqual(bulk[1]['f_string'], 'ITEM_CALL')
        self.assertEqual(bulk['two_x_1__f_text'], 'BULK_CALL')
        
        #--- setting with incorrect keys ---
        item = self.ItemGeneralOne()
        with self.assertRaises(WrongAlias):
            item['wrong_key'] = 'value'
        
        bulk = self.ItemGeneralOne.Bulk()
        with self.assertRaises(WrongAlias):
            bulk['wrong_key'] = 'value'
            
        #--- setting one-to-x default value in bulk
        
        # not items temselves, can belong to different items
        bulk['two_1_1__f_integer'] = '10'
        bulk['two_1_x__f_integer'] = '10'
        bulk['two_x_x__one_1_x__f_integer'] = '10'
         
        # direct
        with self.assertRaises(BulkItemOneToXDefaultError):
            bulk['two_1_1'] = self.ItemGeneralTwo()
         
        with self.assertRaises(BulkItemOneToXDefaultError):
            bulk['two_1_x'] = self.ItemGeneralTwo()
         
        with self.assertRaises(BulkItemOneToXDefaultError):
            bulk['two_1_x'].gen()
         
        with self.assertRaises(BulkItemOneToXDefaultError):
            bulk['two_x_x__one_1_x'].gen()
        
        #--- aliases -----------------------------------------------------------
        self.setup_models(aliased=True)
        
        item = self.ItemGeneralOne()
        item['alias_1'] = '1'
        item['alias_2'] = '2'
        item['two_1_1__alias_1__post'] = 'str-1'
        item['two_1_1__alias_2__post'] = '3'
        item['two_1_1__alias_3__post'] = '4'
        bulk = item['two_1_x']
        bulk['alias_1__post'] = 'str-2'
        
        # aliased
        self.assertEqual(item['alias_1'], '1')
        self.assertEqual(item['alias_2'], '2')
        self.assertEqual(item['two_1_1__alias_1__post'], 'str-1')
        self.assertEqual(item['two_1_1__alias_2__post'], '3')
        self.assertEqual(item['two_1_1__alias_3__post'], '4')
        
        bulk = item['two_1_x']
        self.assertEqual(bulk['alias_1__post'], 'str-2')
        
        # direct
        self.assertEqual(item['two_1_1__f_integer'], '1')
        self.assertEqual(item['two_x_x__one_1_1__f_integer'], '2')
        self.assertEqual(item['two_1_1__f_string'], 'str-1')
        self.assertEqual(item['two_1_1__one_x_1__two_1_1__f_integer'], '3')
        self.assertEqual(item['two_1_1__one_x_x__two_1_x__f_string'], '4')
        
        bulk = item['two_1_x']
        self.assertEqual(bulk['f_string'], 'str-2')
    
    
    def test_aliases(self):
        self.setup_models(aliased=True)
        
        # set
        item = self.ItemGeneralOne()
        item['alias_1'] = '1'
        item['alias_2'] = '2'
        item['two_1_1__alias_1__post'] = 'str-1'
        item['two_1_1__alias_2__post'] = '3'
        item['two_1_1__alias_3__post'] = '4'
        bulk = item['two_1_x']
        bulk['alias_1__post'] = 'str-2'
        
        # get
        self.assertEqual(item['alias_1'], '1')
        self.assertEqual(item['alias_2'], '2')
        self.assertEqual(item['two_1_1__alias_1__post'], 'str-1')
        self.assertEqual(item['two_1_1__alias_2__post'], '3')
        self.assertEqual(item['two_1_1__alias_3__post'], '4')
        self.assertEqual(bulk['alias_1__post'], 'str-2')
        
        # delete
        self.assertIn('alias_1', item)
        del item['alias_1']
        self.assertNotIn('alias_1', item)
        self.assertIn('alias_2', item)
        
        self.assertIn('two_1_1__alias_1__post', item)
        del item['two_1_1__alias_1__post']
        self.assertNotIn('two_1_1__alias_1__post', item)
        
    
    def test_del_field(self):
        self.setup_models()
        
        item = self.ItemGeneralOne()
        item['f_string'] = 'str-10'
        item['two_1_1__f_string'] = 'str-20'
        item['two_x_x__one_1_1__f_string'] = 'str-30'
        bulk = item['two_1_x']
        bulk['f_string'] = 'str-2'
        
        self.assertEqual(item['f_string'], 'str-10')
        del item['f_string']
        self.assertNotIn('f_string', item)
        
        self.assertEqual(item['two_1_1']['f_string'], 'str-20')
        del item['two_1_1__f_string']
        self.assertNotIn('f_string', item['two_1_1'])
        
        
        self.assertEqual(item['two_x_x']['one_1_1__f_string'], 'str-30')
        self.assertNotIn('one_1_1', item['two_x_x'])

        #--- aliases -----------------------------------------------------------
        self.setup_models(aliased=True)
        
        item = self.ItemGeneralOne()
        item['alias_1'] = '1'
        item['alias_2'] = '2'
        item['two_1_1__alias_1__post'] = 'str-1'
        item['two_1_1__alias_2__post'] = '3'
        item['two_1_1__alias_3__post'] = '4'
        bulk = item['two_1_x']
        bulk['alias_1__post'] = 'str-2'
        
        self.assertEqual(item['alias_1'], '1')
        del item['alias_1']
        self.assertNotIn('alias_1', item)
        
        self.assertEqual(item['alias_2'], '2')
        del item['alias_2']
        self.assertNotIn('alias_2', item)

        self.assertEqual(item['two_1_1__alias_1__post'], 'str-1')
        del item['two_1_1__alias_1__post']
        self.assertNotIn('two_1_1__alias_1__post', item)
        
        self.assertEqual(item['two_1_1__alias_2__post'], '3')
        del item['two_1_1__alias_2__post']
        self.assertNotIn('two_1_1__alias_2__post', item)
        
        self.assertEqual(item['two_1_1__alias_3__post'], '4')
        del item['two_1_1__alias_3__post']
        self.assertNotIn('two_1_1__alias_3__post', item)
        
        bulk = item['two_1_x']
        
        self.assertEqual(bulk['alias_1__post'], 'str-2')
        del bulk['alias_1__post']
        self.assertNotIn('alias_1__post', bulk)
    
    
    def test_contains(self):
        self.setup_models()
        item = self.ItemGeneralOne()
        item['f_integer'] = '1'
        item['two_1_x__f_integer'] = '2'
        bulk = item['two_1_x']
        bulk['one_x_x__f_integer'] = '3'
        
        self.assertIn('f_integer', item)
        self.assertIn('two_1_x__f_integer', item)
        self.assertIn('two_1_x__one_x_x__f_integer', item)  # from bulk
        
        self.assertNotIn('wrong_key', item)
        self.assertNotIn('wrong_key__f_integer', item)
        self.assertNotIn('two_1_x__one_x_x__wrong_key', item)
        
        self.assertIn('f_integer', bulk)  # item
        self.assertIn('one_x_x__f_integer', bulk)
        
        self.assertNotIn('wrong_key', bulk)
        self.assertNotIn('wrong_key__f_integer', bulk)
        self.assertNotIn('two_1_x__one_x_x__wrong_key', bulk)
        
        #--- aliased -----------------------------------------------------------
        self.setup_models(aliased=True)
        
        item = self.ItemGeneralOne()
        item['alias_1'] = '1'
        item['alias_2'] = '2'
        item['two_1_1__alias_1__post'] = 'str-1'
        item['two_1_1__alias_2__post'] = '3'
        item['two_1_1__alias_3__post'] = '4'
        bulk = item['two_1_x']
        bulk['alias_1__post'] = 'str-2'
        
        self.assertIn('alias_1', item)
        self.assertIn('alias_2', item)
        self.assertIn('two_1_1__alias_1__post', item)
        self.assertIn('two_1_1__alias_2__post', item)
        self.assertIn('two_1_1__alias_3__post', item)
        
        self.assertNotIn('wrong_key', item)
        self.assertNotIn('wrong_key__f_integer', item)
        self.assertNotIn('two_1_x__one_x_x__wrong_key', item)
        
        self.assertIn('alias_1__post', bulk)
        
        self.assertNotIn('wrong_key', bulk)
        self.assertNotIn('wrong_key__f_integer', bulk)
        self.assertNotIn('two_1_x__one_x_x__wrong_key', bulk)
    
    
    def test_bulk_iter(self):
        self.setup_models()
        bulk = self.ItemGeneralOne.Bulk()
        items = [bulk.gen(f_integer=1),
                 bulk.gen(f_integer=2),
                 bulk.gen(f_integer=3),]
        items_in_bulk = list(bulk)
        self.assertEqual(items_in_bulk, items)
        
        for item_no, item_in_bulk in enumerate(bulk):
            self.assertIs(items[item_no], item_in_bulk)
            self.assertIs(items[item_no], bulk[item_no])
        
        self.assertEqual(item_no, len(items)-1)
        
        
    def test_bulk_item_slice(self):
        class ItemsGeneralOne(Item):
            model_cls = self.ModelGeneralOne
                
        class ItemsGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
                
        
        bulk = ItemsGeneralOne.Bulk()
        
        items = []
        for i in range(10):
            item = ItemsGeneralOne(f_integer=i)
            items.append(item)
            bulk.add(item)
        
        self.assertEqual(items[:5], bulk[:5])
        self.assertEqual(items[0::2], bulk[0::2])

