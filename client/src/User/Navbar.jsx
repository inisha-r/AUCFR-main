import React from 'react';
import { FaSignOutAlt, FaUser } from 'react-icons/fa'; // Importing profile and logout icons

const UserNavbar = () => {
  return (
    <nav className="bg-blue-800 p-4 fixed top-0 left-0 w-full z-10">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-left space-x-4">
          {/* Profile Icon */}
          <a href="/profile" className="text-white text-xl">
            <FaUser />
          </a>
          {/* Welcome User Text */}
          <div className="text-white text-xl">
            <h3>Welcome, User</h3>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          {/* Logout Icon */}
          <a href="/logout" className="text-white text-xl">
            <FaSignOutAlt />
          </a>
        </div>
      </div>
    </nav>
  );
};

export default UserNavbar;
