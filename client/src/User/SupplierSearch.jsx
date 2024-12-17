import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FaSearch, FaEye, FaArrowLeft } from 'react-icons/fa';



const SupplierSearch = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSupplier, setSelectedSupplier] = useState(null);
  const [suppliersData, setSuppliersData] = useState(null);

  useEffect(() => {
    const fetchSupplierData = async () => {
      try {
        const response = await axios.get("https://aucfr-main-server.vercel.app/api/supplier/fetchsupplierdata");

        const names = response.data.supplierData.map((data) => ({ name: data.name }));

        setSuppliersData(names);
        setSuppliersData(response.data.supplierData);
      } catch (err) {
        console.log(err);
      }
    };
    fetchSupplierData();
  }, []);

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const filteredSuppliers = suppliersData?.filter((supplier) =>
    supplier.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleViewSupplier = (supplier) => {
    setSelectedSupplier(supplier);
  };

  const handleBack = () => {
    setSelectedSupplier(null);
  };

  return (
    <div className="mt-[64px] ml-[270px] p-4">
      <h2 className="text-2xl font-bold mb-4">Supplier Search</h2>
      {selectedSupplier ? (
        <div>
          <button
            onClick={handleBack}
            className="mb-4 bg-gray-800 text-white px-4 py-2 rounded flex items-center"
          >
            <FaArrowLeft className="mr-2" />
            Back to List
          </button>
          <h3 className="text-xl font-bold mb-2">{selectedSupplier.name}</h3>
          <p className="mb-4">
            <p><strong>Phone Number: </strong>{selectedSupplier.phoneNumber}</p>
            <p><strong>Business Type: </strong>{selectedSupplier.businessType}</p>
            <p><strong>Tax Id: </strong>{selectedSupplier.taxID}</p>
            <p><strong>Address: </strong>{selectedSupplier.address}</p>
          </p>
          <div className="mt-4">
            <h4 className="text-lg font-bold">Top Products</h4>
            <p>Details about top products...</p>
          </div>
          <div className="mt-4">
            <h4 className="text-lg font-bold">Performance Analysis</h4>
            <p>Details about performance analysis...</p>
          </div>
        </div>
      ) : (
        <>
          <div className="mb-4 flex items-center border rounded">
            <FaSearch className="ml-2 text-gray-500" />
            <input
              type="text"
              placeholder="Search Suppliers"
              value={searchTerm}
              onChange={handleSearch}
              className="w-full px-3 py-2 border-0 outline-none"
            />
          </div>
          <ul>
            {filteredSuppliers?.map((supplier, key) => (
              <li
                key={key}
                className="flex justify-between items-center mb-2 p-2 border rounded hover:bg-gray-100"
              >
                {supplier.name}
                <FaEye
                  className="cursor-pointer text-gray-500 hover:text-blue-500"
                  onClick={() => handleViewSupplier(supplier)}
                />
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
};

export default SupplierSearch;
