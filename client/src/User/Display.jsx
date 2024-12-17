import React, { useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { FaArrowLeft } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

const Display = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const printRef = useRef();

    const rankedData = location.state.response || {};
    const boq = location.state.boq || "";

    const handleBack = () => {
        navigate("/user/product-search");
    };

    const handlePrint = () => {
        const content = printRef.current;
        const printWindow = window.open('', '', 'height=800,width=800');
        
        printWindow.document.write('<html><head><title>AUCFR</title>');
        printWindow.document.write('<style>body{font-family: Arial, sans-serif;}</style>');
        printWindow.document.write('<style>@media print { body { background-color: white; } }</style>');
        printWindow.document.write('</head><body>');
        printWindow.document.write(content.innerHTML);
        printWindow.document.write('</body></html>');
        
        printWindow.document.close();
        printWindow.print();
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
            
            <div className="mt-[24px] ml-[10px] p-4" ref={printRef}>
                <div className="border p-4 mb-4 shadow-md">
                    <h2 className="text-2xl font-bold">BOQ</h2>
                    <br />
                    <p>{boq}</p>
                </div>

                <div>
                    <h2 className="text-2xl font-bold">Top Suppliers</h2>
                    <br />

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
                            </li>
                        ))}
                    </ul>
                </div>
            </div>

            <button
                type="button"
                onClick={handlePrint}
                className="bg-gray-700 text-white px-4 py-2 rounded"
            >
                Print
            </button>
        </div>
    );
};

export default Display;
