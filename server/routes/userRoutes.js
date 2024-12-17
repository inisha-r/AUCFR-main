const express=require('express');
const {storeUserDetail}=require("../controller/userController");
const router=express.Router();

router.post("/storeuserdetail",storeUserDetail);

module.exports=router;