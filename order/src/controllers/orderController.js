const { sendOrderToQueue } = require('../services/orderService');

// Controller to place the order
exports.createOrder = async (req, res) => {
    try {
        const order = req.body;  // Example order body: { userId, productId, quantity }

        // Send order data to RabbitMQ queue
        await sendOrderToQueue(order);

        // Respond with success
        res.status(201).json({
            message: "Order created successfully",
            order
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: "Failed to create order" });
    }
};
