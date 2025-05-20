const jwt = require('jsonwebtoken');
const dotenv = require('dotenv');
dotenv.config();
const JWT_SECRET = process.env.JWT_SECRET;

// JWT verification middleware
const verifyJWT = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({ error: 'Authorization header missing' });
    }

    // Expecting header format: 'Bearer <token>'
    const token = authHeader.split(' ')[1];
    console.log(token);
    console.log(jwt.decode(token));

    if (!token) {
        return res.status(401).json({ error: 'Token missing' });
    }

    jwt.verify(token, JWT_SECRET, { algorithms: ['HS256'] }, (err, decoded) => {
        if (err) {
            console.error('JWT verification error:', err);
            return res.status(403).json({ error: 'Invalid or expired token' });
        }
        req.user = decoded;
        next();
    });

};

module.exports = verifyJWT;
