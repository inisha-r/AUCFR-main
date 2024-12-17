import React from 'react';
import { Link } from 'react-router-dom';

const UserSidebar = () => {
  return (
    <aside className="w-64 bg-gray-800 text-white fixed top-[60px] left-0 h-full">
      <div className="p-4">
        <ul>
          <li>
            <Link to="/user" className="block py-2 px-4 hover:bg-gray-700">Home</Link>
          </li>
          <li>
            <Link to="/user/settings" className="block py-2 px-4 hover:bg-gray-700">Settings</Link>
          </li>
          <li>
            <Link to="/user/supplier-search" className="block py-2 px-4 hover:bg-gray-700">Supplier Search</Link>
          </li>
          <li>
            <Link to="/user/product-search" className="block py-2 px-4 hover:bg-gray-700">Product Search</Link>
          </li>
        </ul>
      </div>
    </aside>
  );
};

export default UserSidebar;
