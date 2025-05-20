const express = require('express');
const router = express.Router();
const {
    addToCart,
    getCartItems,
    removeFromCart,
} = require('../controllers/cartController');
const { createCart } = require('../controllers/cartInit');
const verifyJWT = require('../middlewares/verifyJWT');

router.delete('/remove', verifyJWT, removeFromCart);
router.post('/add', verifyJWT, addToCart);

router.get('/:username', verifyJWT, getCartItems);
router.post('/init', createCart);

module.exports = router;
