import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FaSearch, FaEye, FaPlus, FaEdit, FaArrowLeft } from 'react-icons/fa';

const Supplier = () => {
  const [suppliers, setSuppliers] = useState(null);
  const [filteredSuppliers, setFilteredSuppliers] = useState(suppliers);
  const [selectedSupplier, setSelectedSupplier] = useState(null);
  const [activeTab, setActiveTab] = useState('list');
  const [formData, setFormData] = useState({
    name: '',
    contactPerson: '',
    phoneNumber: '',
    businessType: '',
    taxID: '',
    address: '',
    parameters: [{ name: '', value: '' }],
  });
  const [newSupplierData, setNewSupplierData] = useState({
    name: '',
    contactPerson: '',
    phoneNumber: '',
    businessType: '',
    taxID: '',
    address: '',
    description: '', 
  });
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(()=>{
    console.log(formData?.parameters);
  })

  useEffect(() => {
    setFilteredSuppliers(suppliers);
  }, [suppliers]);

  useEffect(()=>{
     const fetchSupplierData=async()=>{
          try{
            const supplierData=await axios.get("http://localhost:5100/api/supplier/fetchsupplierdata");
            setSuppliers(supplierData.data.supplierData);
          }
          catch(err){
             console.log(err);
          }
     }
     fetchSupplierData();
  },[]);

  const handleView = (supplier) => {
    setSelectedSupplier(supplier);
    setActiveTab('view');
  };

  const handleBack = () => {
    setSelectedSupplier(null);
    setActiveTab('list');
  };

  const handleAdd = () => {
    setFormData({
      name: '',
      contactPerson: '',
      phoneNumber: '',
      businessType: '',
      taxID: '',
      address: '',
      parameters: [{ name: '', value: '' }],
    });
    setSelectedSupplier(null);
    setActiveTab('add');
  };

  const handleEdit = (supplier) => {
    setFormData({
      ...supplier,
      parameters: supplier.parameters || [{ name: '', value: '' }],
    });
    setSelectedSupplier(supplier);
    setActiveTab('edit');
  };

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleParameterChange = (index, e) => {
    const newParameters = [...formData.parameters];
    newParameters[index][e.target.name] = e.target.value;
    setFormData((prev) => ({
      ...prev,
      parameters: newParameters,
    }));
  };

  const handleAddParameter = () => {
    setFormData((prev) => ({
      ...prev,
      parameters: [...prev.parameters, { name: '', value: '' }],
    }));
  };

  const handleNewSupplierChange = (e) => {
    setNewSupplierData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (selectedSupplier) {
      try {
        console.log(formData);
        await axios.patch(`http://localhost:5100/api/supplier/updatesupplier?id=${selectedSupplier._id}`,formData);
      }
      catch(err){
        console.log(err);
      }
    } else {
      setSuppliers((prev) => [
        ...prev,
        { id: prev.length + 1, ...newSupplierData },
      ]);
      console.log(newSupplierData);
      try {
        const response = await axios.post("http://localhost:5100/api/supplier/addnewsupplier",newSupplierData);
        console.log(response);
      }
      catch(err){
        console.log(err);
      }

    }
    handleBack();
  };

  const handleSearchChange = (e) => {
    const query = e.target.value;
    setSearchQuery(query);
    setFilteredSuppliers(
      suppliers.filter((supplier) =>
        supplier.name.toLowerCase().includes(query.toLowerCase())
      )
    );
  };

  return (
    <div className="p-6">
      <div className="mb-4">
        {activeTab === 'list' && (
          <>
            <div className="mb-4 flex items-center border rounded">
              <FaSearch className="ml-2 text-gray-500" />
              <input
                type="text"
                placeholder="Search Suppliers"
                value={searchQuery}
                onChange={handleSearchChange}
                className="w-full px-3 py-2 border-0 outline-none"
              />
            </div>
            <button onClick={handleAdd} className="relative left-[1099px] p-2 cursor-pointer text-gray-500 hover:text-blue-500">
              <FaPlus />
            </button>
          </>
        )}
        {activeTab !== 'list' && (
          <button onClick={handleBack} className="p-2 cursor-pointer text-gray-500 hover:text-blue-500">
            <FaArrowLeft /> Back
          </button>
        )}
      </div>

      {activeTab === 'list' && (
        <div className="flex space-x-6">
          <div className="w-full border p-4">
            <ul className="space-y-2">
              {filteredSuppliers?.map((supplier) => (
                <li
                  key={supplier.id}
                  className="flex justify-between items-center mb-2 p-2 border rounded cursor-pointer"
                >
                  <span>{supplier.name}</span>
                  <div className="space-x-4">
                    <button
                      onClick={() => handleView(supplier)}
                      className="p-2 cursor-pointer text-gray-500 hover:text-blue-500"
                    >
                      <FaEye />
                    </button>
                    <button
                      onClick={() => handleEdit(supplier)}
                      className="p-2 cursor-pointer text-gray-500 hover:text-blue-500"
                    >
                      <FaEdit />
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {activeTab === 'view' && selectedSupplier && (
        <div className="border p-4">
          <h3 className="text-xl font-bold mb-2">{selectedSupplier.name} {selectedSupplier.contactPerson}</h3>
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
      )}

      {activeTab === 'add' && (
        <form onSubmit={handleSubmit} className="border p-4 rounded-md h-[600px] overflow-y-auto">
          <h2 className="text-2xl font-semibold mb-4">Add Supplier</h2>
          <div className="border p-4 rounded-md mt-4">
            <h3 className="text-xl font-semibold mb-2">Personal Details</h3>
            <div className="flex flex-col space-y-4">
              <input
                type="text"
                name="name"
                value={newSupplierData.name}
                onChange={handleNewSupplierChange}
                placeholder="Supplier Name"
                className="p-2 border border-gray-300 rounded-md"
              />
              <input
                type="text"
                name="contactPerson"
                value={newSupplierData.contactPerson}
                onChange={handleNewSupplierChange}
                placeholder="Contact Person"
                className="p-2 border border-gray-300 rounded-md"
              />
              <input
                type="text"
                name="phoneNumber"
                value={newSupplierData.phoneNumber}
                onChange={handleNewSupplierChange}
                placeholder="Phone Number"
                className="p-2 border border-gray-300 rounded-md"
              />
              <input
                type="text"
                name="businessType"
                value={newSupplierData.businessType}
                onChange={handleNewSupplierChange}
                placeholder="Business Type"
                className="p-2 border border-gray-300 rounded-md"
              />
              <input
                type="text"
                name="taxID"
                value={newSupplierData.taxID}
                onChange={handleNewSupplierChange}
                placeholder="Tax ID"
                className="p-2 border border-gray-300 rounded-md"
              />
              <input
                type="text"
                name="address"
                value={newSupplierData.address}
                onChange={handleNewSupplierChange}
                placeholder="Address"
                className="p-2 border border-gray-300 rounded-md"
              />
            </div>
          </div>
          <div className="border p-4 rounded-md mt-4">
            <h3 className="text-xl font-semibold mb-2">Description</h3>
            <textarea
              name="description"
              value={newSupplierData.description}
              onChange={handleNewSupplierChange}
              placeholder="Supplier Description"
              className="p-2 border border-gray-300 rounded-md w-full"
            />
          </div>
          <button
            type="submit"
            className="mt-4 p-2 bg-gray-800 text-white rounded-md hover:bg-gray-700"
          >
            Add Supplier
          </button>
        </form>
      )}


      {activeTab === 'edit' && selectedSupplier && (
        <form onSubmit={handleSubmit} className="border p-4 rounded-md h-[600px] overflow-y-auto">
          <h2 className="text-2xl font-semibold mb-4">Edit Supplier</h2>
          <div className="border p-4 rounded-md mt-4">
            <h3 className="text-xl font-semibold mb-2">Personal Details</h3>
            <div className="flex flex-col space-y-4">
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Supplier Name"
                className="p-2 border border-gray-300 rounded-md"
              />
              <input
                type="text"
                name="contactPerson"
                value={formData.contactPerson}
                onChange={handleChange}
                placeholder="Contact Person"
                className="p-2 border border-gray-300 rounded-md"
              />
              <input
                type="text"
                name="phoneNumber"
                value={formData.phoneNumber}
                onChange={handleChange}
                placeholder="Phone Number"
                className="p-2 border border-gray-300 rounded-md"
              />
              <input
                type="text"
                name="businessType"
                value={formData.businessType}
                onChange={handleChange}
                placeholder="Business Type"
                className="p-2 border border-gray-300 rounded-md"
              />
              <input
                type="text"
                name="taxID"
                value={formData.taxID}
                onChange={handleChange}
                placeholder="Tax ID"
                className="p-2 border border-gray-300 rounded-md"
              />
              <input
                type="text"
                name="address"
                value={formData.address}
                onChange={handleChange}
                placeholder="Address"
                className="p-2 border border-gray-300 rounded-md"
              />
            </div>
            <div className="border p-4 rounded-md mt-4">
              <h3 className="text-xl font-semibold mb-2">Parameters</h3>
              {formData.parameters?.map((param, index) => (
                <div key={index} className="border p-4 rounded-md mt-4">
                  <h3 className="text-xl font-semibold mb-2">Parameter {index + 1}</h3>
                  <div className="flex flex-col space-y-4">
                    <input
                      type="text"
                      name="name"
                      value={param.name}
                      onChange={(e) => handleParameterChange(index, e)}
                      placeholder="Parameter Name"
                      className="p-2 border border-gray-300 rounded-md"
                    />
                    <input
                      type="text"
                      name="value"
                      value={param.value}
                      onChange={(e) => handleParameterChange(index, e)}
                      placeholder="Parameter Value"
                      className="p-2 border border-gray-300 rounded-md"
                    />
                  </div>
                </div>
              ))}
              <button
                type="button"
                onClick={handleAddParameter}
                className="mt-4 p-2 bg-gray-800 text-white rounded-md hover:bg-gray-700"
              >
                Add Parameter
              </button>
            </div>
          </div>
          <button
            type="submit"
            className="mt-4 p-2 bg-gray-800 text-white rounded-md hover:bg-gray-700"
          >
            Save Changes
          </button>
        </form>
      )}
    </div>
  );
};

export default Supplier;
