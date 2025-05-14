const amqplib = require('amqplib');

const RABBITMQ_URL = 'amqp://rabbitmq:5672'; // RabbitMQ Service URL inside the cluster
const QUEUE_NAME = 'orderQueue';

// Function to send order data to RabbitMQ
async function sendOrderToQueue(order) {
    try {
        // Connect to RabbitMQ
        const connection = await amqplib.connect(RABBITMQ_URL);
        const channel = await connection.createChannel();

        // Assert the queue exists
        await channel.assertQueue(QUEUE_NAME, {
            durable: true
        });

        // Send the order to the queue
        channel.sendToQueue(QUEUE_NAME, Buffer.from(JSON.stringify(order)), {
            persistent: true
        });

        console.log('Order sent to queue:', order);

        // Close the connection
        await channel.close();
        await connection.close();
    } catch (err) {
        console.error('Error sending order to RabbitMQ:', err);
        throw err;
    }
}

module.exports = { sendOrderToQueue };
