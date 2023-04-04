"""
This module represents the Unittesting component of the Marketplace module.
"""

import unittest
import random
from marketplace import Marketplace
from product import Coffee, Tea

NUM_PRODUCERS = 10
NUM_CARTS = 10

class MarketplaceTestCase(unittest.TestCase):
    """
    Class that represents a Unittester. It's used for testing purposes.
    """

    def setUp(self):
        """
        Sets up the test.
        """
        self.marketplace = Marketplace(8)
        # Create a list of products and populate the marketplace with them
        prod1 = Coffee(name='Indonezia', price=1, acidity=5.05, roast_level='MEDIUM')
        prod2 = Tea(name='Wild Cherry', price=5, type='Black')
        prod3 = Coffee(name='Brazil', price=2, acidity=4.05, roast_level='LIGHT')
        prod4 = Coffee(name='Colombia', price=3, acidity=3.05, roast_level='MEDIUM')
        prod5 = Tea(name='Linden', price=9, type='Herbal')
        prods = [prod1, prod2, prod3, prod4, prod5]

        # Create a producer
        id_ = self.marketplace.register_producer()

        # Publish the list of products
        _ = [self.marketplace.publish(id_, prod) for prod in prods]

        # Also, create other producers
        _ = [self.marketplace.register_producer() for _ in range(NUM_PRODUCERS - 1)]

    def test_register_producer(self):
        """
        Tests the `register_producer()` method.
        """
        id_ = self.marketplace.register_producer()
        for _ in range(NUM_PRODUCERS - 1):
            self.assertEqual(id_ + 1, self.marketplace.register_producer())
            id_ += 1

    def test_publish(self):
        """
        Tests the `publish()` method.
        """
        # Create a list of products
        prod1 = Coffee(name='Indonezia4', price=1, acidity=5.05, roast_level='MEDIUM')
        prod2 = Tea(name='Linden', price=9, type='Herbal')
        prod3 = Coffee(name='Indonezia2', price=1, acidity=5.05, roast_level='MEDIUM')
        prod4 = Tea(name='English Breakfast', price=2, type='Black')
        prod5 = Tea(name='Vietnam Oolong', price=10, type='Oolong')
        prods = [prod1, prod2, prod3, prod4, prod5]

        # Get a random producer ID
        producer_id = random.randint(0, NUM_PRODUCERS - 1)

        # Publish the list of products
        _ = [self.marketplace.publish(producer_id, prod) for prod in prods]

        # Check if the products were published
        _ = [self.assertIn(prod, self.marketplace.products) for prod in prods]


    def test_new_cart(self):
        """
        Tests the `new_cart()` method.
        """
        # Create a list of carts
        carts = [self.marketplace.new_cart() for _ in range(NUM_CARTS)]

        # Check if the carts were created
        _ = [self.assertIn(cart, self.marketplace.carts) for cart in carts]

    def test_add_to_cart(self):
        """
        Tests the `add_to_cart()` method.
        """
        prod1 = Coffee(name='Indonezia', price=1, acidity=5.05, roast_level='MEDIUM')

        # No cart created yet
        self.assertFalse(self.marketplace.add_to_cart(1, prod1))

        # Create a cart
        cart_id = self.marketplace.new_cart()

        # Add a product to the cart
        self.assertTrue(self.marketplace.add_to_cart(cart_id, prod1))

        # Add an inexistent product to the cart
        prod2 = Coffee(name='Indonezia2', price=1, acidity=5.05, roast_level='MEDIUM')
        self.assertFalse(self.marketplace.add_to_cart(cart_id, prod2))

    def test_remove_from_cart(self):
        """
        Tests the `remove_from_cart()` method.
        """
        # Remove from an inexistent cart
        prod1 = Coffee(name='Indonezia', price=1, acidity=5.05, roast_level='MEDIUM')
        self.assertFalse(self.marketplace.remove_from_cart(1, prod1))

        # Create a cart
        cart_id = self.marketplace.new_cart()

        # Remove an inexistent product from the cart
        prod2 = Coffee(name='Indonezia2', price=1, acidity=5.05, roast_level='MEDIUM')
        self.assertFalse(self.marketplace.remove_from_cart(cart_id, prod2))

        # Add a product to the cart
        self.assertTrue(self.marketplace.add_to_cart(cart_id, prod1))

        # Check if the product was added
        products = [item['product'] for item in self.marketplace.carts[cart_id].products]
        self.assertIn(prod1, products)

        # Remove the product from the cart
        self.marketplace.remove_from_cart(cart_id, prod1)
        products = [item['product'] for item in self.marketplace.carts[cart_id].products]

        # Check if the product was removed
        self.assertNotIn(prod1, products)

    def test_place_order(self):
        """
        Tests the `place_order()` method.
        """
        # Place an order from an inexistent cart
        self.assertFalse(self.marketplace.place_order(1))

        # Create a cart
        cart_id = self.marketplace.new_cart()

        # Add a product to the marketplace
        prod1 = Coffee(name='Indonezia3', price=1, acidity=5.05, roast_level='MEDIUM')
        self.marketplace.publish(0, prod1)

        # Add a product to the cart
        self.assertTrue(self.marketplace.add_to_cart(cart_id, prod1))
        
        # Get the products before placing an order
        order_products_before = [item['product'] for item in \
                                    self.marketplace.carts[cart_id].products]

        # Place an order
        order_products_after = self.marketplace.place_order(cart_id)

        # Check if the order was placed
        self.assertEqual(order_products_before, order_products_after)
