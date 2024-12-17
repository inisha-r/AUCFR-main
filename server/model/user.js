const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
    profile: { type: String },
    Name: { type: String, required: true },
    Email: { type: String, required: true },
    Phone: { type: String },
    Gender: { type: String },
    DOB: { type: Date },
    Username: { type: String },
    Password: { type: String, required: true },
});

const User = mongoose.model('User', UserSchema);

module.exports = User;
