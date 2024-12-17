const express=require('express');
const {addSupplier,fetchSupplierData,updateSupplier}=require('../controller/supplierController');
const router=express.Router();

router.post("/addnewsupplier",addSupplier);
router.get("/fetchsupplierdata",fetchSupplierData);
router.patch("/updatesupplier",updateSupplier);

module.exports=router;