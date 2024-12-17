import React, { useState } from 'react';
import axios from 'axios';

const Settings = () => {
  const [userData, setUserData] = useState({
    profile: '',
    Name: '',
    Email: '',
    Phone: '',
    Gender: '',
    DOB: '',
    Username: '',
    Password: '',
  });

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  const handleUserData = (e) => {
    const { name, value, files } = e.target;
    setUserData((prevData) => ({
      ...prevData,
      [name]: files ? files[0] : value,
    }));

  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    const maxSizeBytes = 20 * 1024 * 1024; 

    if (file) {
      if (file.size > maxSizeBytes) {
        alert('File size exceeds the 20MB limit. Please upload a smaller file.');
        return;
      }
      try {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = () => {
          setUserData((prevData) => ({
            ...prevData,
            profile: reader.result, 
          }));
        };
      } catch (err) {
        console.error('Image processing failed:', err);
      }
    }
  };

  const handleUserFormSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    console.log(userData);
    try {
      const response = await axios.post('https://aucfr-main-server.vercel.app/api/user/storeuserdetail', userData);
      setSuccess(true);
      console.log('Response:', response.data);
    } catch (err) {
      setError(err.response?.data?.message || 'An error occurred.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mt-[64px] ml-[350px] mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Settings</h2>
      <div className="max-h-[650px] overflow-y-auto p-4 border rounded bg-white shadow-md">
        {success && <p className="text-green-600">Profile updated successfully!</p>}
        {error && <p className="text-red-600">{error}</p>}
        <form onSubmit={handleUserFormSubmit}>
          <div className="mb-4">
            <label className="block font-semibold text-gray-700">Profile Picture</label>
            <input
              type="file"
              id="profile-image-upload"
              accept="image/*"
              onChange={handleImageUpload}
            />
          </div>
          <div className="mb-4">
            <label className="block font-semibold text-gray-700">Name</label>
            <input
              type="text"
              className="w-full px-3 py-2 border rounded"
              name="Name"
              value={userData.Name}
              onChange={handleUserData}
            />
          </div>
          <div className="mb-4">
            <label className="block font-semibold text-gray-700">Email</label>
            <input
              type="email"
              className="w-full px-3 py-2 border rounded"
              name="Email"
              value={userData.Email}
              onChange={handleUserData}
            />
          </div>
          <div className="mb-4">
            <label className="block font-semibold text-gray-700">Phone</label>
            <input
              type="tel"
              className="w-full px-3 py-2 border rounded"
              name="Phone"
              value={userData.Phone}
              onChange={handleUserData}
            />
          </div>
          <div className="mb-4">
            <label className="block font-semibold text-gray-700">Gender</label>
            <select
              className="w-full px-3 py-2 border rounded"
              name="Gender"
              value={userData.Gender}
              onChange={handleUserData}
            >
              <option value="">Select Gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div className="mb-4">
            <label className="block font-semibold text-gray-700">Date of Birth</label>
            <input
              type="date"
              className="w-full px-3 py-2 border rounded"
              name="DOB"
              value={userData.DOB}
              onChange={handleUserData}
            />
          </div>
          <div className="mb-4">
            <label className="block font-semibold text-gray-700">Username</label>
            <input
              type="text"
              className="w-full px-3 py-2 border rounded"
              name="Username"
              value={userData.Username}
              onChange={handleUserData}
            />
          </div>
          <div className="mb-4">
            <label className="block font-semibold text-gray-700">Password</label>
            <input
              type="password"
              className="w-full px-3 py-2 border rounded"
              name="Password"
              value={userData.Password}
              onChange={handleUserData}
            />
          </div>
          <button
            type="submit"
            className="bg-gray-700 text-white px-4 py-2 rounded hover:bg-gray-800"
            disabled={loading}
          >
            {loading ? 'Updating...' : 'Update'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Settings;
