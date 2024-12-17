const express=require('express');
const cors=require('cors');
const connectDB=require("./config/db");
const supplierRoutes=require('./routes/supplierRoutes');
const userRoutes=require("./routes/userRoutes");

require('dotenv').config();

connectDB();

const app=express();
app.use(express.json());
app.use(cors());


app.get("/",async(req,res)=>{
    res.json("AUCFR Backend Server");
})

app.use("/api/supplier",supplierRoutes);
app.use("/api/user", userRoutes);


app.listen(process.env.PORT,()=>{
    console.log(`PORT is running on ${process.env.PORT}`);
})