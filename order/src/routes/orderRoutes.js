const express = require('express');
const router = express.Router();
const { createOrder } = require('../controllers/orderController');

// Place Order Route
router.post('/', createOrder);

module.exports = router;
