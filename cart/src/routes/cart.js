const express = require('express');
const router = express.Router();
const {
    addToCart,
    getCartItems,
    removeFromCart,
    createCart
} = require('../controllers/cartController');

router.post('/', addToCart);
router.get('/', getCartItems);
router.delete('/:id', removeFromCart);

router.post('/init', createCart);

module.exports = router;
