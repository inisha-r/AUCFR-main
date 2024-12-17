const Supplier = require('../model/supplier');
const mongoose = require('mongoose');

const addSupplier = async (req, res) => {
    const { name, contactPerson, phoneNumber, businessType, taxID, address, description } = req.body;

    try {
        await Supplier.insertMany({ name, contactPerson, phoneNumber, businessType, taxID, address, description });
        res.status(200).json({ message: 'Supplier added successfully' });
    } catch (err) {
        console.log(err);
        res.status(500).json({ message: 'Server error' });
    }
}

const fetchSupplierData = async (req, res) => {
    const { businessType } = req.query || null;
    try {
        if (businessType) {
            const supplierData = await Supplier.find({ businessType });
            res.status(200).json({ message: 'Supplier Data fetched successfully', supplierData });
            return;
        }
        const supplierData = await Supplier.find();
        res.status(200).json({ message: 'Supplier Data fetched successfully', supplierData });
    } catch (err) {
        console.log(err);
        res.status(500).json({ message: 'Server error' });
    }
}


const updateSupplier = async (req, res) => {
    const { id } = req.query;
    const { name, contactPerson, phoneNumber, businessType, taxID, address, parameters } = req.body;
    try {
        const updatedSupplier = await Supplier.updateOne({ _id: new mongoose.Types.ObjectId(id) }, { $set: { name, contactPerson, phoneNumber, businessType, taxID, address, parameters, } });
        res.status(200).json({ message: 'Supplier updated successfully', updatedSupplier });
    } catch (err) {
        console.log(err);
        res.status(500).json({ message: 'Server error' });
    }
};



module.exports = { addSupplier, fetchSupplierData, updateSupplier };