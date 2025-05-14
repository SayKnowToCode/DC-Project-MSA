const mongoose = require('mongoose');

const CartItemSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
        unique: true,
    },
    cart: [{
        product_id: Number,
        description: String,
        price: Number,
        quantity: Number,
    }]

});

module.exports = mongoose.model('CartItem', CartItemSchema);
