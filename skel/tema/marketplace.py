"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock, currentThread
from .cart import Cart

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer # Maximum queue size per producer

        self.producers = [] # List of producer IDs
        self.products = [] # List of products in the marketplace

        self.producer_num_products = {} # {producer_id: num_products}
        self.product_to_producer = {} # {product: producer_id} (inverse mapping)

        self.carts = {} # {cart_id: [product1, product2, ...]}
        self.num_carts = 0 # Number of carts in the marketplace

        self.register_producer_lock = Lock() # Lock for `register_producer()` method
        self.new_cart_lock = Lock() # Lock for `new_cart()` method
        self.add_to_cart_lock = Lock() # Lock for `add_to_cart()` method
        self.place_order_lock = Lock() # Lock for `place_order()` method

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.register_producer_lock:
            _ = [self.producers.append(0) if not self.producers else \
                    self.producers.append(self.producers[-1] + 1)]
        return self.producers[-1]

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # Check if the producer has reached the maximum number of products
        producer_id = int(producer_id)
        producer_curr_products = self.producer_num_products.get(producer_id, 0)
        if producer_curr_products >= self.queue_size_per_producer:
            return False

        # Increment the number of products for the producer
        self.producer_num_products[producer_id] = producer_curr_products + 1

        # Add the product to the marketplace `products` list
        self.products.append(product)

        # Also perform the inverse mapping from product -> producer_id
        self.product_to_producer[product] = producer_id

        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.new_cart_lock:
            # Increase the number of carts
            self.num_carts += 1

            # Create a new cart
            self.carts[self.num_carts] = Cart()

        # Return the cart id
        return self.num_carts

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        with self.add_to_cart_lock:
            # Check if the product is in the marketplace
            if product not in self.products:
                return False

            # Get the producer id for the product
            producer_id = self.product_to_producer[product]

            # Decrease the number of products for the producer
            self.producer_num_products[producer_id] -= 1

            # Add the product to the cart
            self.carts[cart_id].add_product(product, producer_id)

            # Remove the product from the marketplace
            self.products.remove(product)

        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        # Remove from `cart_id`
        self.carts[cart_id].remove_product(product)

        # Make the product available again in the marketplace
        self.products.append(product)

        # Increase the number of products for the producer
        self.producer_num_products[self.product_to_producer[product]] += 1

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        # Get the products from the cart
        products = self.carts[cart_id].get_products()

        # Print the order
        for product in products:
            with self.place_order_lock:
                name = str(currentThread().getName())
                print(f"{name} bought {product}")

        return products
