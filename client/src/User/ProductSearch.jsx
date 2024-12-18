// import React, { useState } from 'react';
// import { FaSearch, FaArrowLeft } from 'react-icons/fa';
// import { useNavigate } from 'react-router-dom';

// const productsData = [
//   { id: 1, name: 'Facade' },
//   // Add more products if needed
// ];

// const ProductSearch = () => {
//   const [searchTerm, setSearchTerm] = useState('');
//   const [selectedProduct, setSelectedProduct] = useState(null);
//   const [boqText, setBoqText] = useState('');
//   const navigate = useNavigate();

//   const handleSearch = (event) => {
//     setSearchTerm(event.target.value);
//   };

//   const handleViewProduct = (product) => {
//     setSelectedProduct(product);
//   };

//   const handleProceed = () => {
//     // Navigate to Results page and pass boqText as state
//     navigate('/user/results', { state: { boqText } });
//   };

//   const filteredProducts = productsData.filter((product) =>
//     product.name.toLowerCase().includes(searchTerm.toLowerCase())
//   );

//   return (
//     <div className="mt-[64px] ml-[260px] p-4">
//       {selectedProduct ? (
//         <div>
//           <button
//             onClick={() => setSelectedProduct(null)}
//             className="mb-4 bg-gray-800 text-white px-4 py-2 rounded flex items-center"
//           >
//             <FaArrowLeft className="mr-2" />
//             Back to Products
//           </button>
//           <h2 className="text-2xl font-bold mb-4">{selectedProduct.name}</h2>
//           <div className="overflow-auto max-h-[650px] bg-gray-100 p-4 rounded">
//             <h2 className="text-xl font-bold mb-4">Enter the BOQ of the Product</h2>
//             <textarea
//               className="w-full p-3 border rounded mb-4"
//               rows="10"
//               placeholder="Enter the BOQ of the product here..."
//               value={boqText}
//               onChange={(e) => setBoqText(e.target.value)}
//             />
//             <button
//               type="button"
//               onClick={handleProceed}
//               className="bg-gray-700 text-white px-4 py-2 rounded"
//             >
//               Proceed
//             </button>
//           </div>
//         </div>
//       ) : (
//         <div>
//           <h2 className="text-2xl font-bold mb-4">Product Search</h2>
//           <div className="mb-4 flex items-center border rounded">
//             <FaSearch className="ml-2 text-gray-500" />
//             <input
//               type="text"
//               placeholder="Search Products"
//               value={searchTerm}
//               onChange={handleSearch}
//               className="w-full px-3 py-2 border-0 outline-none"
//             />
//           </div>
//           <h3 className="text-xl font-bold mb-4">Our Products</h3>
//           <ul>
//             {filteredProducts.map((product) => (
//               <li key={product.id} className="mb-2 flex justify-between items-center p-2 border rounded hover:bg-gray-100">
//                 <span>{product.name}</span>
//                 <button
//                   onClick={() => handleViewProduct(product)}
//                   className="bg-gray-700 text-white px-3 py-1 rounded"
//                 >
//                   View
//                 </button>
//               </li>
//             ))}
//           </ul>
//         </div>
//       )}
//     </div>
//   );
// };

// export default ProductSearch;


import React, { useState } from 'react';
import { FaSearch, FaArrowLeft } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

const productsData = [
  { id: 1, name: 'Facade' },
  // Add more products if needed
];

const cityOptions = [
  'Ahmedabad', 'Agra', 'Alappuzha', 'Ariyalur', 'Aurangabad', 'Bangalore', 'Bhopal', 'Bilaspur',
  'Bhubaneswar', 'Chandigarh', 'Chennai', 'Coimbatore', 'Cuddalore', 'Dindigul', 'Dehradun',
  'Durgapur', 'Faridabad', 'Ghaziabad', 'Guwahati', 'Gurgaon', 'Hyderabad', 'Indore',
  'Jaipur', 'Jabalpur', 'Jammu', 'Jodhpur', 'Kallakurichi', 'Kanpur', 'Kanyakumari',
  'Kochi', 'Kolkata', 'Lucknow', 'Madurai', 'Meerut', 'Mysore', 'Nagapattinam', 'Nagpur',
  'Navi Mumbai', 'Noida', 'Patna', 'Perambalur', 'Pune', 'Rajkot', 'Ranchi', 'Raipur',
  'Rourkela', 'Salem', 'Shimla', 'Silchar', 'Thanjavur', 'Tenkasi', 'Thiruvananthapuram',
  'Tiruchirappalli', 'Tirunelveli', 'Tiruppur', 'Tiruvannamalai', 'Thrissur', 'Vadodara',
  'Vijayawada', 'Virudhunagar', 'Visakhapatnam', 'Vellore', 'Villupuram'
];

const ProductSearch = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [boqText, setBoqText] = useState('');
  const [selectedCity, setSelectedCity] = useState('');
  const [selectedOption, setSelectedOption] = useState('');

  const navigate = useNavigate();

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleViewProduct = (product) => {
    setSelectedProduct(product);
  };

  // const handleProceed = () => {
  //   if (boqText && selectedCity) { // Ensure both fields have values
  //     navigate('/user/topsuppliers',{state:{selectedProduct}});
  //     // navigate('/user/results', { state: { boqText, selectedCity } });
  //   } else {
  //     alert("Please enter BOQ text and select a city."); // Optional alert for user feedback
  //   }
  // };

  const handleProceed = async () => {
   // console.log("data123", boqText, selectedCity,selectedOption);
    if (boqText && selectedCity && selectedOption) {
      try {
        const response = await fetch('https://aucfr-main-backend.onrender.com/predict', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ city: selectedCity }),
        });

        if (!response.ok) {
          throw new Error('Failed to fetch predictions');
        }

        const result = await response.json();
        //console.log(result);

        navigate('/user/topsuppliers', {
          state: {
            response: result,boq:boqText
          },
        });
      } catch (error) {
        console.error('Error fetching predictions:', error);
        alert('Something went wrong while fetching predictions.');
      }
    } else {
      alert('Please enter BOQ text and select a city.');
    }
  };


  const filteredProducts = productsData.filter((product) =>
    product.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="mt-[64px] ml-[260px] p-4">
      {selectedProduct ? (
        <div>
          <button
            onClick={() => setSelectedProduct(null)}
            className="mb-4 bg-gray-800 text-white px-4 py-2 rounded flex items-center"
          >
            <FaArrowLeft className="mr-2" />
            Back to Products
          </button>
          <h2 className="text-2xl font-bold mb-4">{selectedProduct.name}</h2>
          <div className="overflow-auto max-h-[650px] bg-gray-100 p-4 rounded">
            <select
              className="w-full p-2 border rounded"
              value={selectedOption}
              onChange={(e) => setSelectedOption(e.target.value)}
            >
              <option value="">Select an option</option>
              <option value="Vision Panel">Vision Panel</option>
              <option value="Spandrel Panel">Spandrel Panel</option>
              <option value="ACP">ACP</option>
              <option value="Glass Canopy">Glass Canopy</option>
              <option value="Spider Glazing">Spider Glazing</option>
              <option value="ACP for Canopy">ACP for Canopy</option>
              <option value="Acoustic Enclosure Louver Cladding">Acoustic Enclosure Louver Cladding</option>
              <option value="Aluminium Louvers">Aluminium Louvers</option>
              <option value="Signage External Facade DataCenter Logo">Signage External Facade DataCenter Logo</option>
            </select>

            <h2 className="text-xl font-bold mb-4 mt-4">Enter the BOQ of the Product</h2>
            <textarea
              className="w-full p-3 border rounded mb-4"
              rows="10"
              placeholder="Enter the BOQ of the product here..."
              value={boqText}
              onChange={(e) => setBoqText(e.target.value)}
            />
            <div className="mb-4">
              <label className="block mb-2 font-bold">Select a City</label>
              <select
                className="w-full p-2 border rounded"
                value={selectedCity}
                onChange={(e) => setSelectedCity(e.target.value)}
              >
                <option value="">Select a city</option>
                {cityOptions.map((city, index) => (
                  <option key={index} value={city}>{city}</option>
                ))}
              </select>
            </div>
            <button
              type="button"
              onClick={handleProceed}
              className="bg-gray-700 text-white px-4 py-2 rounded"
              disabled={!boqText || !selectedCity ||!selectedOption} 
            >
              Proceed
            </button>
          </div>
        </div>
      ) : (
        <div>
          <h2 className="text-2xl font-bold mb-4">Product Search</h2>
          <div className="mb-4 flex items-center border rounded">
            <FaSearch className="ml-2 text-gray-500" />
            <input
              type="text"
              placeholder="Search Products"
              value={searchTerm}
              onChange={handleSearch}
              className="w-full px-3 py-2 border-0 outline-none"
            />
          </div>
          <h3 className="text-xl font-bold mb-4">Our Products</h3>
          <ul>
            {filteredProducts.map((product) => (
              <li key={product.id} className="mb-2 flex justify-between items-center p-2 border rounded hover:bg-gray-100">
                <span>{product.name}</span>
                <button
                  onClick={() => handleViewProduct(product)}
                  className="bg-gray-700 text-white px-3 py-1 rounded"
                >
                  View
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ProductSearch;
