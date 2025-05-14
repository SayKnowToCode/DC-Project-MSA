const CartItem = require('../models/CartItem');

// Add item to cart
exports.addToCart = async (req, res) => {
    try {
        const newItem = new CartItem(req.body);
        const savedItem = await newItem.save();
        res.status(201).json(savedItem);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};

// Get all items
exports.getCartItems = async (req, res) => {
    try {
        const items = await CartItem.find();
        res.status(200).json(items);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};

// Remove item from cart
exports.removeFromCart = async (req, res) => {
    try {
        await CartItem.findByIdAndDelete(req.params.id);
        res.status(200).json({ message: 'Item removed' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};
