const express = require('express');
const router = express.Router();
const {
    addToCart,
    getCartItems,
    removeFromCart,
} = require('../controllers/cartController');
const { createCart } = require('../controllers/cartInit');

router.post('/add', addToCart);
router.get('/:username', getCartItems);
router.delete('/remove', removeFromCart);


router.post('/init', createCart);

module.exports = router;
