const CartItem = require('../models/CartItem');

const createCart = async (req, res) => {
    try {
        const { jsonrpc, method, params, id } = req.body;

        if (method !== 'init') {
            return res.status(400).json({
                jsonrpc: '2.0',
                error: { code: -32601, message: 'Method not found' },
                id
            });
        }

        const { username } = params;
        if (!username) {
            return res.status(400).json({
                jsonrpc: '2.0',
                error: { code: -32602, message: 'Missing username parameter' },
                id
            });
        }

        // Check if cart already exists
        const existingCart = await CartItem.findOne({ name: username });
        if (existingCart) {
            return res.json({
                jsonrpc: '2.0',
                result: { message: 'Cart already exists', cart: existingCart },
                id
            });
        }

        // Create a new cart
        const newCart = new CartItem({
            name: username,
            cart: [] // Empty cart initially
        });

        await newCart.save();

        return res.json({
            jsonrpc: '2.0',
            result: { message: 'Cart created successfully', cart: newCart },
            id
        });

    } catch (error) {
        console.error('Error creating cart:', error);
        return res.status(500).json({
            jsonrpc: '2.0',
            error: { code: -32603, message: 'Internal error' },
            id: req.body.id || null
        });
    }
};

module.exports = { createCart };
