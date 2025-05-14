const express = require('express');
const router = express.Router();
const {
    addToCart,
    getCartItems,
    removeFromCart
} = require('../controllers/cartController');
const { createCart } = require('../controllers/cartInit');

router.post('/', addToCart);
router.get('/', getCartItems);
router.delete('/:id', removeFromCart);

router.post('/init', createCart);

module.exports = router;
