import React from 'react';
import { FaHome, FaBell, FaSignOutAlt } from 'react-icons/fa';

const Navbar = () => {
  return (
    <nav className="flex items-center justify-between bg-gray-800 p-4">
      <div className="flex items-center">
        <FaHome className="text-white text-3xl mr-2" />
        <h1 className="text-white font-bold text-xl">Company Name</h1>
      </div>
      <div className="flex items-center">
        <FaBell className="text-white text-xl mr-2" />
        <a href="/logout" className="text-white text-xl">
            <FaSignOutAlt />
        </a>
      </div>
    </nav>
  );
};

export default Navbar;
