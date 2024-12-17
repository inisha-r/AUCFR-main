const express=require('express');
const cors=require('cors');
const connectDB=require("./config/db");
const supplierRoutes=require('./routes/supplierRoutes');
const userRoutes=require("./routes/userRoutes");

require('dotenv').config();

connectDB();

const app=express();
app.use(express.json());
app.use(cors({
    origin: "https://aucfr-main-client.vercel.app", 
    methods: ["POST", "GET","PATCH","DELETE"],
    credentials: true
  }));
app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "https://aucfr-main-client.vercel.app"); 
    res.header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS,DELETE");
    res.header("Access-Control-Allow-Headers", "Content-Type, Authorization");
    res.header("Access-Control-Allow-Credentials", "true");
    next();
  });
app.use(cors());


app.get("/",async(req,res)=>{
    res.json("AUCFR Backend Server");
})

app.use("/api/supplier",supplierRoutes);
app.use("/api/user", userRoutes);


app.listen(process.env.PORT,()=>{
    console.log(`PORT is running on ${process.env.PORT}`);
})
