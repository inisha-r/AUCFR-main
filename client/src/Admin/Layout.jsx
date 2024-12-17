import React from 'react';
import { Outlet } from 'react-router-dom';
import AdminNavbar from './Navbar';
import AdminSidebar from './Sidebar';

const AdminLayout = () => {
  return (
    <div className="flex flex-col h-full">
      <AdminNavbar />
      <div className="flex flex-1">
        <AdminSidebar />
        <main className="flex-grow p-4 bg-gray-100">
          <Outlet /> {/* Renders the nested route */}
        </main>
      </div>
    </div>
  );
};

export default AdminLayout;
