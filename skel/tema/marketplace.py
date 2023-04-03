"""
This module represents the Marketplace.
"""

from threading import Lock
from .logger import Logger
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

        self.carts = {} # {cart_id: Cart()}
        self.num_carts = 0 # Number of carts in the marketplace

        self.register_producer_lock = Lock() # Lock for `register_producer()` method
        self.new_cart_lock = Lock() # Lock for `new_cart()` method
        self.add_to_cart_lock = Lock() # Lock for `add_to_cart()` method

        self.logger = Logger(__name__) # Logger
        # Logger.disable()
        self.logger.log('Marketplace created')

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.register_producer_lock:
            self.logger.log('[?] Registering producer')
            _ = [self.producers.append(0) if not self.producers else \
                    self.producers.append(self.producers[-1] + 1)]
            producer_id = self.producers[-1]
            self.logger.log(f'[W] Producer {producer_id} registered')

        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # Log the input parameters
        self.logger.log(f'[?] Producer {producer_id} is trying to publish {product}...')

        # Check if the producer has reached the maximum number of products
        producer_id = int(producer_id)
        producer_curr_products = self.producer_num_products.get(producer_id, 0)
        if producer_curr_products >= self.queue_size_per_producer:
            self.logger.log(f'[X] Producer {producer_id} reached '
                f'the maximum number of products {self.queue_size_per_producer}')
            return False

        # Increment the number of products for the producer
        self.producer_num_products[producer_id] = producer_curr_products + 1

        # Add the product to the marketplace `products` list
        self.products.append(product)

        # Also perform the inverse mapping from product -> producer_id
        self.product_to_producer[product] = producer_id

        self.logger.log(f'[W] Producer {producer_id} successfully published {product}')

        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.new_cart_lock:
            self.logger.log('[?] Creating a new cart')
            # Increase the number of carts
            self.num_carts += 1

            # Create a new cart
            self.carts[self.num_carts] = Cart()

            self.logger.log(f'[W] Cart {self.num_carts} created')

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
            # Log the input parameters
            self.logger.log(f'[?] Adding {product} to cart {cart_id}')

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

            # Log the results
            self.logger.log(f'[W] Added {product} to cart {cart_id}')

        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        # Log the input parameters
        self.logger.log(f'[?] Removing {product} from cart {cart_id}')

        # Remove from `cart_id`
        self.carts[cart_id].remove_product(product)

        # Make the product available again in the marketplace
        self.products.append(product)

        # Increase the number of products for the producer
        self.producer_num_products[self.product_to_producer[product]] += 1

        # Log the results
        self.logger.log(f'[W] Removed {product} from cart {cart_id}')

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        # Log the input parameters
        self.logger.log(f'[?] Placing order for cart {cart_id}')

        # Get the products from the cart
        products = self.carts[cart_id].get_products()

        # Log the results
        self.logger.log(f'[W] Placed order for cart {cart_id}')

        return products
        