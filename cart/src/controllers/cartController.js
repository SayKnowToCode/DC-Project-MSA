const CartItem = require('../models/CartItem');

// Add an item to a specific user's cart
exports.addToCart = async (req, res) => {
    try {
        const { item } = req.body;

        const username = req.user.username;
        if (!item) {
            return res.status(400).json({ error: 'Username and item are required' });
        }
        console.log(username)
        const userCart = await CartItem.findOne({ name: username });
        if (!userCart) {
            return res.status(404).json({ error: 'Cart not found for this user' });
        }

        userCart.cart.push(item);
        const updatedCart = await userCart.save();

        res.status(200).json({ message: 'Item added to cart', cart: updatedCart });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};

// Get all items in a specific user's cart  
exports.getCartItems = async (req, res) => {
    try {
        const { username } = req.user.username;

        const userCart = await CartItem.findOne({ name: username });

        if (!userCart) {
            return res.status(404).json({ error: 'Cart not found for this user' });
        }

        res.status(200).json(userCart.cart);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};

// Remove an item from a user's cart by product_id
exports.removeFromCart = async (req, res) => {
    try {
        const { product_id } = req.body;
        const { username } = req.user.username;
        const userCart = await CartItem.findOne({ name: username });

        if (!userCart) {
            return res.status(404).json({ error: 'Cart not found for this user' });
        }
        const initialLength = userCart.cart.length;

        userCart.cart = userCart.cart.filter(item => item.product_id != product_id);

        if (userCart.cart.length == initialLength) {
            return res.status(404).json({ error: 'Item not found in cart' });
        }

        const updatedCart = await userCart.save();

        res.status(200).json({ message: 'Item removed', cart: updatedCart });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};



