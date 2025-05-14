const mongoose = require('mongoose');


const MONGO_URI = process.env.MONGO_URI;
console.log("Mongo URI:", MONGO_URI);

const connectDB = async () => {
    try {
        await mongoose.connect(MONGO_URI);
        console.log('MongoDB connected');
    } catch (err) {
        console.log('eror here')
        console.error(err.message);
        process.exit(1);
    }
};

module.exports = connectDB;
