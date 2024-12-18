import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import { FaEye, FaArrowLeft } from 'react-icons/fa';
import { extractFeatures } from '../featureExtractor';

const TopSupplier = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const rankedData = location.state.response || {};
  const boq = location.state.boq || "";


  const handleBack = () => {
    navigate("/user/product-search");
  };

  const handleProceed = () => {
    const boqresult = extractFeatures(boq);

    if (boqresult != null) {
      navigate('/user/display', {
        state: {
          response: rankedData, boq: boqresult
        },
      });
    }
  };

  return (
    <div className="mt-[64px] ml-[270px]">
      <button
        onClick={handleBack}
        className="mb-4 bg-gray-800 text-white px-4 py-2 rounded flex items-center"
      >
        <FaArrowLeft className="mr-2" />
        Back
      </button>
      <div className="mt-[64px] ml-[10px] p-4">
        <h2 className="text-2xl font-bold">Top Suppliers</h2>
        <br />

        <div>
          <ul>
            {rankedData?.map((supplier, key) => (
              <li
                key={key}
                className="flex justify-between items-center mb-2 p-2 border rounded hover:bg-gray-100"
              >
                <div>
                  <p>
                    <strong>Supplier:</strong> {supplier['FACADE VENDOR']}
                  </p>
                  <p>
                    <strong>Rank:</strong> {supplier.Rank}
                  </p>
                  <p>
                    <strong>Predicted Ranking Score:</strong>{' '}
                    {supplier['Predicted Ranking Score']}
                  </p>
                </div>
                <FaEye
                  className="cursor-pointer text-gray-500 hover:text-blue-500"
                  onClick={() => console.log(supplier)}
                />
              </li>
            ))}
          </ul>
        </div>
      </div>
      <button
        type="button"
        onClick={handleProceed}
        className="bg-gray-700 text-white px-4 py-2 rounded"
      >
        Proceed
      </button>
    </div>
  );
};

export default TopSupplier;













// import React, { useEffect, useState } from 'react';
// import axios from 'axios';
// import { useLocation } from 'react-router-dom';
// import { FaEye,FaArrowLeft } from 'react-icons/fa';
// import { useNavigate } from 'react-router-dom';

// const TopSupplier = () => {

//     const location = useLocation();
//     const [selectedSupplier, setSelectedSupplier] = useState(null);
//     const [supplier, setSupplier] = useState(null);
//     const { selectedProduct } = location.state || {};
//     const navigate=useNavigate();
//     const { selectedProduct1, predictions, distance, rankedData } = location.state || {};
//   console.log(selectedProduct1,predictions,distance,rankedData)
//     const handleViewSupplier = (supplier) => {
//         setSelectedSupplier(supplier);
//     };

//     const handleBack = () => {
//         setSelectedSupplier(null);
//     };

//     const handleProceed = async () => {
//         // navigate('/user/results');
//         if (boqText && selectedCity) {
//             try {
//               const response = await fetch('http://localhost:5000/predict', {
//                 method: 'POST',
//                 headers: {
//                   'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({ city: selectedCity }),
//               });

//               if (!response.ok) {
//                 throw new Error('Failed to fetch predictions');
//               }

//               const result = await response.json();
//               console.log(result);

//               // Navigate to the top suppliers page with API results
//               navigate('/user/topsuppliers', {
//                 state: {
//                   selectedProduct,
//                   predictions: result.predictions,
//                   distance: result.distance,
//                   rankedData: result.ranked_data,
//                 },
//               });
//             } catch (error) {
//               console.error('Error fetching predictions:', error);
//               alert('Something went wrong while fetching predictions.');
//             }
//           } else {
//             alert('Please enter BOQ text and select a city.');
//           }
//     };

//     useEffect(() => {

//         const fetchTopSupplier = async () => {
//             try {
//                 const response = await axios.get(`http://localhost:5000/api/supplier/fetchsupplierdata?businessType=${selectedProduct.name}`);
//                 setSupplier(response.data);
//             }
//             catch (err) {
//                 console.log(err);
//             }
//         }
//         fetchTopSupplier();

//     }, [selectedProduct]);

//     return (
//         <div className='mt-[64px] ml-[270px]'>

//             <div className="mt-[64px] ml-[10px] p-4">
//             <h2 className="text-2xl font-bold">Top Suppliers</h2><br/>
//                 {selectedSupplier ?
//                     (
//                         <div>
//                             <button
//                                 onClick={handleBack}
//                                 className="mb-4 bg-gray-800 text-white px-4 py-2 rounded flex items-center"
//                             >
//                                 <FaArrowLeft className="mr-2" />
//                                 Back to List
//                             </button>
//                             <h3 className="text-xl font-bold mb-2">{selectedSupplier.name}</h3>
//                             <p className="mb-4">
//                                 <p><strong>Phone Number: </strong>{selectedSupplier.phoneNumber}</p>
//                                 <p><strong>Business Type: </strong>{selectedSupplier.businessType}</p>
//                                 <p><strong>Tax Id: </strong>{selectedSupplier.taxID}</p>
//                                 <p><strong>Address: </strong>{selectedSupplier.address}</p>
//                             </p>
//                             <div className="mt-4">
//                                 <h4 className="text-lg font-bold">Top Products</h4>
//                                 <p>Details about top products...</p>
//                             </div>
//                             <div className="mt-4">
//                                 <h4 className="text-lg font-bold">Performance Analysis</h4>
//                                 <p>Details about performance analysis...</p>
//                             </div>
//                         </div>
//                     ) : (
//                         <div>
//                             <>
//                                 <ul>
//                                     {supplier?.supplierData?.map((supplier, key) => (
//                                         <li
//                                             key={key}
//                                             className="flex justify-between items-center mb-2 p-2 border rounded hover:bg-gray-100"
//                                         >
//                                             {supplier.name}
//                                             <FaEye
//                                                 className="cursor-pointer text-gray-500 hover:text-blue-500"
//                                                 onClick={() => handleViewSupplier(supplier)}
//                                             />
//                                         </li>
//                                     ))}
//                                 </ul>
//                             </>
//                         </div>)
//                 }
//             </div>
//             <button
//               type="button"
//               onClick={handleProceed}
//               className="bg-gray-700 text-white px-4 py-2 rounded"
//             >
//               Proceed
//             </button>
//         </div>

//     );
// };

// export default TopSupplier;


