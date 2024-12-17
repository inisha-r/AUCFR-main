// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import Results from './User/Results';


// Admin components
import AdminNavbar from './Admin/Navbar';
import AdminSidebar from './Admin/Sidebar';
import AdminDashboard from './Admin/Dashboard';
import AdminSupplier from './Admin/Supplier';
import AdminCustomer from './Admin/Customer';
import AdminOrder from './Admin/Order';
import AdminFeedback from './Admin/Feedback';
import AdminReport from './Admin/Report';
import AdminContact from './Admin/Contact';

// User components
import UserNavbar from './User/Navbar';
import UserSidebar from './User/Sidebar';
import Settings from './User/Settings';
import SupplierSearch from './User/SupplierSearch';
import ProductSearch from './User/ProductSearch';
import Dashboard from './User/Dashboard';

// Login component
import Login from './Login';
import TopSupplier from './User/TopSupplier';
import Display from './User/Display';

// Admin Layout Component
const AdminLayout = () => {
  return (
    <div className="flex flex-col h-full">
      <AdminNavbar />
      <div className="flex flex-1">
        <AdminSidebar />
        <main className="flex-grow p-4 bg-white">
          <Routes>
            <Route path="/" element={<AdminDashboard />} />
            <Route path="supplier" element={<AdminSupplier />} />
            <Route path="customer" element={<AdminCustomer />} />
            <Route path="order" element={<AdminOrder />} />
            <Route path="feedback" element={<AdminFeedback />} />
            <Route path="report" element={<AdminReport />} />
            <Route path="contact" element={<AdminContact />} />
          </Routes>
        </main>
      </div>
    </div>
  );
};

// User Layout Component
const UserLayout = () => {
  return (
    <div className="flex flex-col h-full">
      <UserNavbar />
      <div className="flex flex-1">
        <UserSidebar />
        <main className="flex-grow p-4 bg-white">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="settings" element={<Settings />} />
            <Route path="supplier-search" element={<SupplierSearch />} />
            <Route path="product-search" element={<ProductSearch />} />
            <Route path="results" element={<Results />} />
            <Route path="topsuppliers" element={<TopSupplier/>}/>
            <Route path="display" element={<Display/>}/>
          </Routes>
        </main>
      </div>
    </div>
  );
};

const App = () => {
  const { user } = useAuth();

  return (
    <Router>
      <Routes>
        {/* Login Page */}
        <Route path="/login" element={<Login />} />

        {/* Admin Panel */}
        <Route path="/admin/*" element={user?.role === 'admin' ? <AdminLayout /> : <Navigate to="/login" replace />} />

        {/* User Panel */}
        <Route path="/user/*" element={user?.role === 'user' ? <UserLayout /> : <Navigate to="/login" replace />} />
        
        {/* Redirect to login if none of the routes match */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
};

export default App;
