const express = require('express');
const connectDB = require('./config/db');
const cartRoutes = require('./routes/cart');

const app = express();
const PORT = 6000; //to be changed

// Middleware
app.use(express.json());

// Connect DB
connectDB();

// Routes
app.use('/cart', cartRoutes);

app.listen(PORT, () => {
    console.log(`Cart Service running on port ${PORT}`);
});
