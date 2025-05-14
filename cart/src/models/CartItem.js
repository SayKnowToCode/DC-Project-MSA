const mongoose = require('mongoose');

const CartItemSchema = new mongoose.Schema({
    name: String,
    imageUrl: String,
    description: String,
    price: Number,
    quantity: Number,
});

module.exports = mongoose.model('CartItem', CartItemSchema);
