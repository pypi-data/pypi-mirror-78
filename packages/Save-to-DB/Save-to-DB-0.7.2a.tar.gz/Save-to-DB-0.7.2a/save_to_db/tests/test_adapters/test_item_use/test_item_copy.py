import copy
from save_to_db.core.item import Item
from save_to_db.utils.test_base import TestBase



class TestItemCopy(TestBase):
    
    ModelGeneralOne = None
    ModelGeneralTwo = None
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        class ItemGeneralOne(Item):
            model_cls = cls.ModelGeneralOne
        cls.ItemGeneralOne = ItemGeneralOne
        
        class ItemGeneralTwo(Item):
            model_cls = cls.ModelGeneralTwo
        cls.ItemGeneralTwo = ItemGeneralTwo
    
    
    def test_copy(self):
        # --- single item ---
        item_one = self.ItemGeneralOne(f_integer=10)
        item_two = self.ItemGeneralTwo(f_integer=20)
        item_one['two_x_1'] = item_two
        item_one['two_1_x'].add(item_two)
        item_one['two_1_x__f_integer'] = 30
        
        item_one_copy = copy.copy(item_one)
        self.assertIsNot(item_one_copy, item_one)
        
        # related items must be the same
        self.assertIs(item_one_copy['two_x_1'], item_two)
        self.assertIs(item_one_copy['two_1_x'][0], item_two)
        
        self.assertEqual(item_one_copy['f_integer'], 10)
        self.assertEqual(item_one_copy['two_x_1']['f_integer'], 20)
        self.assertEqual(item_one_copy['two_1_x'][0]['f_integer'], 20)
        self.assertEqual(item_one_copy['two_1_x']['f_integer'], 30)
        
        # reverse relationships must keep updating
        second_item_two = self.ItemGeneralTwo(f_integer=200)
        item_one_copy['two_1_1'] = second_item_two
        self.assertIs(second_item_two['one_1_1'], item_one_copy)
        
        # --- bulk item ---
        bulk_one = self.ItemGeneralOne.Bulk(f_integer=10)
        item_one_in_bulk = self.ItemGeneralTwo()
        item_two_in_bulk_defaults = self.ItemGeneralTwo()
        
        bulk_one.add(item_one_in_bulk)
        bulk_one['two_x_1'] = item_two_in_bulk_defaults
        
        bulk_one_copy = copy.copy(bulk_one)
        self.assertIsNot(bulk_one_copy, bulk_one)
        self.assertEqual(bulk_one_copy['f_integer'], 10)
        
        # bulk attribute must be new but contain the same items
        self.assertIsNot(bulk_one_copy.bulk, bulk_one.bulk)
        self.assertEqual(bulk_one_copy.bulk, bulk_one.bulk)
        
        # related items must be the same ...
        
        # ... in bulk
        self.assertIs(bulk_one_copy[0], item_one_in_bulk)
        
        # ... in defaults
        self.assertIs(bulk_one['two_x_1'], item_two_in_bulk_defaults)
        
        # reverse relationships must keep updating
        item_two_container = self.ItemGeneralTwo(
            one_1_x=bulk_one_copy
        )
        second_item_one_in_bulk = self.ItemGeneralOne()
        bulk_one_copy.add(second_item_one_in_bulk)
        self.assertIs(second_item_one_in_bulk['two_x_1'], item_two_container)
    
    
    def test_deepcopy(self):
        # --- single item ---
        item_one = self.ItemGeneralOne(f_integer=10)
        item_two = self.ItemGeneralTwo(f_integer=20)
        item_one['two_x_1'] = item_two
        item_one['two_1_x'].add(item_two)
        item_one['two_1_x__f_integer'] = 30
        
        item_one_copy = copy.deepcopy(item_one)
        self.assertIsNot(item_one_copy, item_one)
        
        # related items must be new
        self.assertIsNot(item_one_copy['two_x_1'], item_two)
        self.assertIsNot(item_one_copy['two_1_x'][0], item_two)
        
        # reverse relationships mut be updated
        two_x_1 = item_one_copy['two_x_1']
        self.assertIs(two_x_1['one_1_x'], item_one_copy)
        
        self.assertEqual(item_one_copy['f_integer'], 10)
        self.assertEqual(item_one_copy['two_x_1']['f_integer'], 20)
        self.assertEqual(item_one_copy['two_1_x'][0]['f_integer'], 20)
        self.assertEqual(item_one_copy['two_1_x']['f_integer'], 30)
        
        return
        
        # reverse relationships must keep updating
        item_two = self.ItemGeneralTwo()
        item_one_copy['two_1_1'] = item_two
        self.assertIs(item_two['one_1_1'], item_one_copy)
        
        item_two = self.ItemGeneralTwo()
        item_one_copy['two_x_1'] = item_two
        self.assertEqual(len(item_two['one_1_x']), 1)
        self.assertIs(item_two['one_1_x'][0], item_one_copy)
        
        item_two = self.ItemGeneralTwo()
        item_one_copy['two_1_x'].add(item_two)
        self.assertIs(item_two['one_x_1'], item_one_copy)
        
        # --- bulk item ---
        bulk_one = self.ItemGeneralOne.Bulk(f_integer=10)
        item_one_in_bulk = self.ItemGeneralTwo()
        item_two_in_bulk_defaults = self.ItemGeneralTwo()
        
        bulk_one.add(item_one_in_bulk)
        bulk_one['two_x_1'] = item_two_in_bulk_defaults
        
        print()
        print('!!!')
        bulk_one_copy = copy.deepcopy(bulk_one)
        self.assertIsNot(bulk_one_copy, bulk_one)
        self.assertEqual(bulk_one_copy['f_integer'], 10)
        
        # copied items must be new ...
        
        # ... in bulk
        self.assertIsNot(bulk_one_copy[0], item_one_in_bulk)
        
        # ... in defaults
        self.assertIsNot(bulk_one['two_x_1'], item_two_in_bulk_defaults)
        
        pass