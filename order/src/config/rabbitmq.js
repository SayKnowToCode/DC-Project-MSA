const amqplib = require('amqplib');

const RABBITMQ_URL = process.env.RABBITMQ_URL || 'amqp://order_service_user:12345@rabbitmq:5672';


// Function to establish RabbitMQ connection
async function createRabbitMQConnection() {
    try {
        const connection = await amqplib.connect(RABBITMQ_URL);
        console.log('Connected to RabbitMQ');
        return connection;
    } catch (err) {
        console.error('Error connecting to RabbitMQ:', err);
        throw err;
    }
}

module.exports = { createRabbitMQConnection };
