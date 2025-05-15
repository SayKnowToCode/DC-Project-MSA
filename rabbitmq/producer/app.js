const express = require('express');
const mongoose = require('mongoose');
const amqp = require('amqplib');

const app = express();
const PORT = 3500;

const MONGO_URI = "mongodb+srv://Ninad:NinadDGR8@cluster0.izi96ja.mongodb.net/DC-Project?retryWrites=true&w=majority&appName=Cluster0";
const RABBITMQ_URL = "amqp://rabbitmq";


// Connect to MongoDB
mongoose.connect(MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log("MongoDB connected"))
    .catch(err => console.error("MongoDB connection error:", err));

app.get('/send/:username', async (req, res) => {
    const { username } = req.params;

    try {
        // Get direct access to collection without schema
        const collection = mongoose.connection.db.collection('cartitems');
        const userCart = await collection.findOne({ name: username });

        if (!userCart || !userCart.cart) {
            return res.status(404).json({ error: 'Cart not found for this user' });
        }

        // Connect to RabbitMQ and send message
        const connection = await amqp.connect(RABBITMQ_URL);
        const channel = await connection.createChannel();

        const queue = 'order_queue';
        await channel.assertQueue(queue, { durable: true });

        const messageBuffer = Buffer.from(JSON.stringify(userCart.cart));
        channel.sendToQueue(queue, messageBuffer, { persistent: true });

        console.log("Sent to RabbitMQ:", userCart.cart);

        await channel.close();
        await connection.close();

        res.status(200).json({ status: 'Message sent to RabbitMQ', cart: userCart.cart });

    } catch (err) {
        console.error("Error Here:", err);
        res.status(500).json({ error: err.message });
    }
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});