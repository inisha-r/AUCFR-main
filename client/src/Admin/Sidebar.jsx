import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = () => {
  return (
    <div className="w-64 h-screen bg-gray-800 text-white flex flex-col">
      <ul className="space-y-4 p-4">
        <li>
          <Link to="/admin" className="block text-center  hover:text-gray-300">Home</Link>
        </li>
        <li>
          <Link to="/admin/supplier" className="block text-center hover:text-gray-300">Supplier</Link>
        </li>
        <li>
          <Link to="/admin/customer" className="block text-center hover:text-gray-300">Customer</Link>
        </li>
        <li>
          <Link to="/admin/order" className="block text-center hover:text-gray-300">Order</Link>
        </li>
        <li>
          <Link to="/admin/feedback" className="block text-center hover:text-gray-300">Feedback</Link>
        </li>
        <li>
          <Link to="/admin/report" className="block text-center hover:text-gray-300">Report</Link>
        </li>
        <li>
          <Link to="/admin/contact" className="block text-center hover:text-gray-300">Contact</Link>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
