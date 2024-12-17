const User = require('../model/user');

const storeUserDetail = async (req, res) => {
    const {
        profile,
        Name,
        Email,
        Phone,
        Gender,
        DOB,
        Username,
        Password,
    } = req.body;

    try {
        await User.insertMany([{ profile, Name, Email, Phone, Gender, DOB, Username, Password }]);
        res.status(200).json({ message: 'User added successfully' });
    } catch (err) {
        console.error('Error saving user:', err.message);
        res.status(500).json({ message: 'Server error', error: err.message });
    }
};

module.exports = { storeUserDetail };
