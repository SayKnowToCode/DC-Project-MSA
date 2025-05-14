const express = require('express');
const connectDB = require('./config/db');
const cors = require('cors');
const cartRoutes = require('./routes/cart');


const app = express();
app.use(cors());
const PORT = 6000; //to be changed

app.use(express.json());

connectDB();

app.use('/cart', cartRoutes);

app.listen(PORT, () => {
    console.log(`Cart Service running on port ${PORT}`);
});
