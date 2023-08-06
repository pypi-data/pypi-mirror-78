from save_to_db.core.item import Item
from save_to_db.core.utils.mapper import mapper 
from save_to_db.utils.test_base import TestBase


class TestMapper(TestBase):
    
    ModelGeneralOne = None
    ModelGeneralTwo = None
    
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        class ItemGeneralOne(Item):
            model_cls = cls.ModelGeneralOne
                
        class ItemGeneralTwo(Item):
            model_cls = cls.ModelGeneralTwo
        
        cls.ItemGeneralOne = ItemGeneralOne
        cls.ItemGeneralTwo = ItemGeneralTwo
    
    
    def test_item_added_on_creation(self):
        single_item = self.ItemGeneralOne()
        self.assertIn(single_item, mapper)
        
        bulk_item = self.ItemGeneralOne.Bulk()
        self.assertIn(bulk_item, mapper)
    
    
    def test_reverse_key_one_to_one(self):
        #--- setting ---
        # direct set ...
        item_one = self.ItemGeneralOne()
        first_item_two = self.ItemGeneralTwo()
        item_one['two_1_1'] = first_item_two
         
        self.assertIn('one_1_1', first_item_two)
        self.assertIs(first_item_two['one_1_1'], item_one)
        
        # ... direct overwrite
        second_item_two = self.ItemGeneralTwo()
        item_one['two_1_1'] = second_item_two
        
        self.assertIn('one_1_1', second_item_two)
        self.assertIs(second_item_two['one_1_1'], item_one)
        
        self.assertNotIn('one_1_1', first_item_two)
        
        # set on creation
        item_two = self.ItemGeneralTwo()
        item_one = self.ItemGeneralOne(two_1_1=item_two)
        
        self.assertIn('one_1_1', item_two)
        self.assertIs(item_two['one_1_1'], item_one)
        
        # set on getting
        item_one = self.ItemGeneralOne()
        item_two = item_one['two_1_1']
        
        self.assertIn('one_1_1', item_two)
        self.assertIs(item_two['one_1_1'], item_one)

        # set by call ...
        first_item_two = self.ItemGeneralTwo()
        item_one = self.ItemGeneralOne()
        item_one(two_1_1=first_item_two)
        
        self.assertIn('one_1_1', first_item_two)
        self.assertIs(first_item_two['one_1_1'], item_one)
        
        # ... overwrite by call
        second_item_two = self.ItemGeneralTwo()
        item_one(two_1_1=second_item_two)
        
        self.assertIn('one_1_1', second_item_two)
        self.assertIs(second_item_two['one_1_1'], item_one)
        
        self.assertNotIn('one_1_1', first_item_two)
        
        #--- overwrite by `None` ---
        item_one = self.ItemGeneralOne()
        item_two = self.ItemGeneralTwo()
        item_one['two_1_1'] = item_two
         
        item_one['two_1_1'] = None

        self.assertNotIn('one_1_1', item_two)
        
        #--- deleting item value ---
        item_one = self.ItemGeneralOne()
        item_two = self.ItemGeneralTwo()
        item_one['two_1_1'] = item_two
         
        del item_one['two_1_1']
        
        self.assertNotIn('two_1_1', item_one)
        self.assertNotIn('one_1_1', item_two)
                
        #--- deleting item itsef ---
        item_one = self.ItemGeneralOne()
        item_two = self.ItemGeneralTwo(f_integer=1)
        item_one['two_1_1'] = item_two
        
        self.assertIn('one_1_1', item_two)
        item_two.delete()
        
        self.assertNotIn('one_1_1', item_two)
        self.assertNotIn('f_integer', item_two)
         
        self.assertNotIn('two_1_1', item_one)

    
    def test_reverse_key_one_to_many(self):
        #--- setting ---
         
        # set and add ...
        item_one = self.ItemGeneralOne()
        first_bulk_two = self.ItemGeneralTwo.Bulk()
        item_one['two_1_x'] = first_bulk_two
          
        first_item_two = self.ItemGeneralTwo()
        first_bulk_two.add(first_item_two)
         
        self.assertIn('one_x_1', first_item_two)
        self.assertIs(first_item_two['one_x_1'], item_one)
         
        # ... direct overwrite
        second_bulk_two = self.ItemGeneralTwo.Bulk()
        second_item_two = self.ItemGeneralTwo()
        second_bulk_two.add(second_item_two)
        item_one['two_1_x'] = second_bulk_two
         
        self.assertNotIn('one_x_1', first_item_two)  # not in first bulk
        self.assertIn('one_x_1', second_item_two)    # in second bulk
        self.assertIs(second_item_two['one_x_1'], item_one)
        
        # gen
        item_one = self.ItemGeneralOne()
        bulk_two = self.ItemGeneralTwo.Bulk()
        item_one['two_1_x'] = bulk_two
          
        item_two = bulk_two.gen()
         
        self.assertIn('one_x_1', item_two)
        self.assertIs(item_two['one_x_1'], item_one)
         
        #--- removing ---
        item_one = self.ItemGeneralOne()
        bulk_two = self.ItemGeneralTwo.Bulk()
        item_one['two_1_x'] = bulk_two
          
        first_item_two = bulk_two.gen()
        second_item_two = bulk_two.gen()
         
        self.assertIs(first_item_two['one_x_1'], item_one)
        self.assertIs(second_item_two['one_x_1'], item_one)
         
        bulk_two.remove(first_item_two)
         
        self.assertNotIn('one_x_1', first_item_two)
        self.assertIs(second_item_two['one_x_1'], item_one)
         
        #--- deleting ---
         
        # bulk reference
        item_one = self.ItemGeneralOne()
        bulk_two = self.ItemGeneralTwo.Bulk()
        item_one['two_1_x'] = bulk_two
          
        first_item_two = bulk_two.gen()
        second_item_two = bulk_two.gen()
         
        self.assertIn(first_item_two, bulk_two)
        self.assertIn(second_item_two, bulk_two)
         
        del item_one['two_1_x']
         
        self.assertIn(first_item_two, bulk_two)
        self.assertIn(second_item_two, bulk_two)
         
        self.assertNotIn('one_x_1', first_item_two)
        self.assertNotIn('one_x_1', second_item_two)
        
        # parent item
        item_one = self.ItemGeneralOne()
        bulk_two = self.ItemGeneralTwo.Bulk()
        item_one['two_1_x'] = bulk_two
          
        first_item_two = bulk_two.gen()
        second_item_two = bulk_two.gen()
        
        item_one.delete()
        
        self.assertNotIn('two_1_x', item_one)
        
        self.assertIn(first_item_two, bulk_two)
        self.assertIn(second_item_two, bulk_two)
        
        self.assertNotIn('one_x_1', first_item_two)
        self.assertNotIn('one_x_1', second_item_two)
        
        
        # bulk itself
        item_one = self.ItemGeneralOne()
        bulk_two = self.ItemGeneralTwo.Bulk()
        item_one['two_1_x'] = bulk_two
          
        first_item_two = bulk_two.gen()
        second_item_two = bulk_two.gen()
         
        self.assertIn(first_item_two, bulk_two)
        self.assertIn(second_item_two, bulk_two)
         
        self.assertIs(first_item_two['one_x_1'], item_one)
        self.assertIs(second_item_two['one_x_1'], item_one)
         
        bulk_two.delete()

        self.assertNotIn('two_1_x', item_one)
        self.assertEqual(len(bulk_two), 0)
          
        self.assertNotIn('one_x_1', first_item_two)
        self.assertNotIn('one_x_1', second_item_two)
        
        # item in bulk
        item_one = self.ItemGeneralOne()
        bulk_two = self.ItemGeneralTwo.Bulk()
        item_one['two_1_x'] = bulk_two
          
        first_item_two = bulk_two.gen()
        second_item_two = bulk_two.gen()
         
        self.assertIn(first_item_two, bulk_two)
        self.assertIn(second_item_two, bulk_two)
         
        first_item_two.delete()
         
        self.assertNotIn(first_item_two, bulk_two)
        self.assertIn(second_item_two, bulk_two)
    
    
    def test_reverse_key_many_to_many(self):
        #--- setting ---
        
        # direct set
        item_one = self.ItemGeneralOne()
        bulk_two = self.ItemGeneralTwo.Bulk()
        item_one['two_x_x'] = bulk_two
         
        # gen item on that side
        genned_item_two = bulk_two.gen()
        self.assertIn('one_x_x', genned_item_two)
        self.assertIn(item_one, genned_item_two['one_x_x'])
        self.assertIn(genned_item_two, item_one['two_x_x'])
         
        # gen item on this side
        genned_item_one = genned_item_two['one_x_x'].gen()
         
        self.assertIn('two_x_x', genned_item_one)
        self.assertIn(genned_item_two, genned_item_one['two_x_x'])
        self.assertIn(genned_item_one, genned_item_two['one_x_x'])
         
        # --- overwriting with non-empty bulk-items ---
        bulk_one = self.ItemGeneralOne.Bulk()
          
        bulk_two = self.ItemGeneralTwo.Bulk()
        item_two = bulk_two.gen(f_integer=200)
          
        item_one = bulk_one.gen(f_integer=100)
        item_one['two_x_x'] = bulk_two
        
        # reverse was set
        self.assertIn(item_one, item_two['one_x_x'])
        
        second_bulk_two = self.ItemGeneralTwo.Bulk()
        item_one['two_x_x'] = second_bulk_two
        
        # reverse cleared
        self.assertNotIn(item_one, item_two['one_x_x'])
         
        #--- separate many-to-many ---
        # [REF: 1]
        # Items:
        #    one: 11, 12
        #    two: 21, 22
        #
        #    11 has:         21, 22
        #    21 has: 11, 12
        #    (reverse)
        #    12 has:             21
        #    22 has: 11
        item_11 = self.ItemGeneralOne(f_integer=11)
        item_12 = self.ItemGeneralOne(f_integer=12)
        item_21 = self.ItemGeneralTwo(f_integer=21)
        item_22 = self.ItemGeneralTwo(f_integer=22)
         
        item_11['two_x_x'].add(item_21, item_22)
        item_21['one_x_x'].add(item_11, item_12)
         
        self.assertEqual(len(item_11['two_x_x']), 2)
        self.assertIn(item_21, item_11['two_x_x'])
        self.assertIn(item_22, item_11['two_x_x'])
         
        self.assertEqual(len(item_21['one_x_x']), 2)
        self.assertIn(item_11, item_21['one_x_x'])
        self.assertIn(item_12, item_21['one_x_x'])
         
        # (reverse)
        self.assertEqual(len(item_12['two_x_x']), 1)
        self.assertIn(item_21, item_12['two_x_x'])
         
        self.assertEqual(len(item_22['one_x_x']), 1)
        self.assertIn(item_11, item_22['one_x_x'])
         
        #--- removing items ---
        # [REF: 2]
        #    removing from 11: 21
        #
        #    (removed items in brackets)
        #    11 has:            [21], 22
        #    21 has: [11],  12
        #    (reverse)
        #    12 has:                  21
        #    22 has:  11
        item_11['two_x_x'].remove(item_21)
         
        self.assertEqual(len(item_11['two_x_x']), 1)
        self.assertIn(item_22, item_11['two_x_x'])
         
        self.assertEqual(len(item_21['one_x_x']), 1)
        self.assertIn(item_12, item_21['one_x_x'])
          
        self.assertEqual(len(item_12['two_x_x']), 1)
        self.assertIn(item_21, item_12['two_x_x'])
          
        self.assertEqual(len(item_22['one_x_x']), 1)
        self.assertIn(item_11, item_22['one_x_x'])
        
        #--- deleting ---
        
        # creates structure as on [REF: 1]
        item_11, item_12, item_21, item_22 = None, None, None, None
        def make_structure():
            nonlocal item_11, item_12, item_21, item_22
            item_11 = self.ItemGeneralOne(f_integer=11)
            item_12 = self.ItemGeneralOne(f_integer=12)
            item_21 = self.ItemGeneralTwo(f_integer=21)
            item_22 = self.ItemGeneralTwo(f_integer=22)
        
            item_11['two_x_x'].add(item_21, item_22)
            item_21['one_x_x'].add(item_11, item_12)
        
        # deleting bulk in 11: (removed items in brackets)
        # 
        #    11 has:            [21], [22] - deleted (reset)
        #    21 has: [11],  12
        #    (reverse)
        #    12 has:             21
        #    22 has: [11]

        # deleting bulk item
        make_structure()
        item_11['two_x_x'].delete()
         
        self.assertNotIn('two_x_x', item_11)
         
        self.assertEqual(len(item_21['one_x_x']), 1)
        self.assertIn(item_12, item_21['one_x_x'])
 
        self.assertEqual(len(item_12['two_x_x']), 1)
        self.assertIn(item_21, item_12['two_x_x'])
           
        self.assertIn('one_x_x', item_22)
        self.assertEqual(len(item_22['one_x_x']), 0)
        
        # deleting reference to bulk
        make_structure()
        del item_11['two_x_x']
        
        self.assertNotIn('two_x_x', item_11)
         
        self.assertEqual(len(item_21['one_x_x']), 1)
        self.assertIn(item_12, item_21['one_x_x'])
 
        self.assertEqual(len(item_12['two_x_x']), 1)
        self.assertIn(item_21, item_12['two_x_x'])
           
        self.assertIn('one_x_x', item_22)
        self.assertEqual(len(item_22['one_x_x']), 0)
        
        
        # deleting single item
        make_structure()
        item_11.delete()
        
        # all many-to-many must stay in play, but item deleted from them
        self.assertNotIn('two_x_x', item_11)  # reset
         
        self.assertEqual(len(item_21['one_x_x']), 1)
        self.assertIn(item_12, item_21['one_x_x'])
         
        # (reverse)
        self.assertEqual(len(item_12['two_x_x']), 1)
        self.assertIn(item_21, item_12['two_x_x'])
         
        self.assertIn('one_x_x', item_22)
        self.assertEqual(len(item_22['one_x_x']), 0)
        
    
    def test_reverse_key_many_to_one(self):
        # --- set direct ---
        
        # item two without reverse
        item_one = self.ItemGeneralOne()
        item_two = self.ItemGeneralTwo()
        item_one['two_x_1'] = item_two
        self.assertEqual(len(item_two['one_1_x']), 1)
        self.assertIn(item_one, item_two['one_1_x'])
         
        # overwriting
        second_item_two = self.ItemGeneralTwo()
        item_one['two_x_1'] = second_item_two
        self.assertEqual(len(second_item_two['one_1_x']), 1)
        self.assertIn(item_one, second_item_two['one_1_x'])
        self.assertEqual(len(item_two['one_1_x']), 0)
        self.assertNotIn(item_one, item_two['one_1_x'])

        # item two with reverse
        item_one = self.ItemGeneralOne()
        item_two = self.ItemGeneralTwo(one_1_x=[])
        item_one['two_x_1'] = item_two
        self.assertEqual(len(item_two['one_1_x']), 1)
        self.assertIn(item_one, item_two['one_1_x'])

        # --- deleting ---
        
        # deleting item that item
        item_one = self.ItemGeneralOne()
        item_two = self.ItemGeneralTwo(one_1_x=[])
        item_one['two_x_1'] = item_two
        
        item_two.delete()
        
        self.assertNotIn('one_1_x', item_two)
        self.assertNotIn('two_x_1', item_one)
        
        # deleting this that item
        item_one = self.ItemGeneralOne()
        item_two = self.ItemGeneralTwo()
        item_one['two_x_1'] = item_two
        
        item_one.delete()
        
        self.assertIn('one_1_x', item_two)
        self.assertNotIn(item_one, item_two['one_1_x'])
        
        # deleting reference        
        item_one = self.ItemGeneralOne()
        item_two = self.ItemGeneralTwo()
        item_one['two_x_1'] = item_two
        
        del item_one['two_x_1']
        
        self.assertIn('one_1_x', item_two)
        self.assertNotIn(item_one, item_two['one_1_x'])
        
        # deleting bulk
        item_one = self.ItemGeneralOne()
        item_two = self.ItemGeneralTwo()
        item_one['two_x_1'] = item_two
        
        item_two['one_1_x'].delete()
        
        self.assertEqual(len(item_two['one_1_x']), 0)
        self.assertNotIn('two_x_1', item_one)
    
    
    def test_item_delete(self):
        # --- single item ---
        two_1_x = self.ItemGeneralTwo.Bulk()
        two_1_x.gen()
        two_1_x.gen()
        
        two_x_x = self.ItemGeneralTwo.Bulk()
        two_x_x.gen()
        two_x_x.gen()
        
        item_one_fields = {
            'f_integer': 10,
            'f_string': 'str-1',
            'two_1_1': self.ItemGeneralTwo(),
            'two_x_1': self.ItemGeneralTwo(),
            'two_1_x': two_1_x,
            'two_x_x': two_x_x,
        }
        item_one = self.ItemGeneralOne(**item_one_fields)
        
        for key in item_one_fields:
            self.assertIn(key, item_one)
        
        item_one.delete()
        
        for key in item_one_fields:
            self.assertNotIn(key, item_one)
        
        # --- bulk item container ---
        bulk_one = self.ItemGeneralOne.Bulk()
        bulk_one.gen()
        bulk_one.gen()
        
        self.assertEqual(len(bulk_one), 2)
        
        bulk_one.delete()
        
        self.assertEqual(len(bulk_one), 0)
        
        # --- bulk defaults must be cleared ---
        item_one_1 = self.ItemGeneralOne()
        bulk_one_1 = self.ItemGeneralOne.Bulk()
        
        bulk_two = self.ItemGeneralTwo.Bulk(
            one_x_1=item_one_1, one_x_x =bulk_one_1,
            f_integer=10, one_x_1__f_integer=20
        )
        
        self.assertIn('one_x_1', bulk_two)
        self.assertIn('one_x_x', bulk_two)
        self.assertIn('f_integer', bulk_two)
        self.assertIn('one_x_1__f_integer', bulk_two)
        
        bulk_two.delete()
        
        self.assertNotIn('one_x_1', bulk_two)
        self.assertNotIn('one_x_x', bulk_two)
        self.assertNotIn('f_integer', bulk_two)
        self.assertNotIn('one_x_1__f_integer', bulk_two)
        
        # --- deleted items must not be referenced ---
        # x-to-1
        item_one_1 = self.ItemGeneralOne()
        bulk_one_1 = self.ItemGeneralOne.Bulk()
        
        bulk_two = self.ItemGeneralTwo.Bulk(
            one_x_1=item_one_1, one_x_x =bulk_one_1,
            f_integer=10, one_x_1__f_integer=20
        )
        
        item_one_1.delete()
        
        self.assertNotIn('one_x_1', bulk_two)
        self.assertIs(bulk_two['one_x_x'], bulk_one_1)
        self.assertEqual(bulk_two['f_integer'], 10)
        self.assertEqual(bulk_two['one_x_1__f_integer'], 20)
        
        # x-to-x
        item_one_1 = self.ItemGeneralOne()
        bulk_one_1 = self.ItemGeneralOne.Bulk()
        
        bulk_two = self.ItemGeneralTwo.Bulk(
            one_x_1=item_one_1, one_x_x =bulk_one_1,
            f_integer=10, one_x_1__f_integer=20
        )
        
        bulk_one_1.delete()
        
        self.assertNotIn('one_x_x', bulk_two)
        self.assertIs(bulk_two['one_x_1'], item_one_1)
        self.assertEqual(bulk_two['f_integer'], 10)
        self.assertEqual(bulk_two['one_x_1__f_integer'], 20)
        
        