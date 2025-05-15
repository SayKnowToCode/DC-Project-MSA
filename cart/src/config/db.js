const mongoose = require('mongoose');

// const MONGO_URI = process.env.MONGO_URI;
const MONGO_URI = "mongodb+srv://Ninad:NinadDGR8@cluster0.izi96ja.mongodb.net/DC-Project?retryWrites=true&w=majority&appName=Cluster0"


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
