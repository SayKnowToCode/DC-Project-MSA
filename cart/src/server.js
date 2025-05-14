const express = require('express');
const connectDB = require('./config/db');
const cartRoutes = require('./routes/cart');

const app = express();
const PORT = 6000;

// Middleware
app.use(express.json());

// Connect DB
connectDB();

// Routes
app.use('/api/cart', cartRoutes);

app.listen(PORT, () => {
    console.log(`Cart Service running on port ${PORT}`);
});
