/**
 * Podcast MVP - Minimal React Frontend Starter
 * =============================================
 *
 * This is a minimal working React app to get you started.
 *
 * To run:
 * 1. npm create vite@latest . -- --template react
 * 2. npm install axios react-router-dom
 * 3. Copy this file to src/App.jsx
 * 4. npm run dev
 * 5. Open http://localhost:5173
 *
 * Next steps: Add recorder component, dashboard, episode list from MVP_TECHNICAL_SPEC.md
 */

import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [view, setView] = useState('login'); // login, signup, dashboard
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);

  // ========== AUTH COMPONENTS ==========

  const LoginForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleLogin = async (e) => {
      e.preventDefault();
      setError('');

      try {
        const response = await axios.post(`${API_URL}/auth/login`, {
          email,
          password
        });

        const { access_token, user: userData } = response.data;
        localStorage.setItem('token', access_token);
        setToken(access_token);
        setUser(userData);
        setView('dashboard');
      } catch (err) {
        setError(err.response?.data?.error || 'Login failed');
      }
    };

    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow-md w-96">
          <h1 className="text-2xl font-bold mb-6">🎙️ Podcast MVP - Login</h1>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          <form onSubmit={handleLogin}>
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            <div className="mb-6">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            <button
              type="submit"
              className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
            >
              Login
            </button>
          </form>

          <p className="mt-4 text-center text-sm">
            Don't have an account?{' '}
            <button
              onClick={() => setView('signup')}
              className="text-blue-500 hover:underline"
            >
              Sign up
            </button>
          </p>
        </div>
      </div>
    );
  };

  const SignupForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [error, setError] = useState('');

    const handleSignup = async (e) => {
      e.preventDefault();
      setError('');

      try {
        const response = await axios.post(`${API_URL}/auth/signup`, {
          email,
          password,
          full_name: fullName
        });

        const { access_token, user: userData } = response.data;
        localStorage.setItem('token', access_token);
        setToken(access_token);
        setUser(userData);
        setView('dashboard');
      } catch (err) {
        setError(err.response?.data?.error || 'Signup failed');
      }
    };

    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow-md w-96">
          <h1 className="text-2xl font-bold mb-6">🎙️ Podcast MVP - Sign Up</h1>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          <form onSubmit={handleSignup}>
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Full Name
              </label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:border-blue-500"
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            <div className="mb-6">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            <button
              type="submit"
              className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
            >
              Sign Up
            </button>
          </form>

          <p className="mt-4 text-center text-sm">
            Already have an account?{' '}
            <button
              onClick={() => setView('login')}
              className="text-blue-500 hover:underline"
            >
              Login
            </button>
          </p>
        </div>
      </div>
    );
  };

  // ========== DASHBOARD COMPONENT ==========

  const Dashboard = () => {
    const [podcasts, setPodcasts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showNewPodcastForm, setShowNewPodcastForm] = useState(false);
    const [newPodcastTitle, setNewPodcastTitle] = useState('');
    const [newPodcastDescription, setNewPodcastDescription] = useState('');

    useEffect(() => {
      fetchPodcasts();
    }, []);

    const fetchPodcasts = async () => {
      try {
        const response = await axios.get(`${API_URL}/podcasts`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setPodcasts(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Failed to fetch podcasts:', err);
        setLoading(false);
      }
    };

    const createPodcast = async (e) => {
      e.preventDefault();

      try {
        await axios.post(`${API_URL}/podcasts`, {
          title: newPodcastTitle,
          description: newPodcastDescription
        }, {
          headers: { Authorization: `Bearer ${token}` }
        });

        setNewPodcastTitle('');
        setNewPodcastDescription('');
        setShowNewPodcastForm(false);
        fetchPodcasts();
      } catch (err) {
        alert('Failed to create podcast');
      }
    };

    const handleLogout = () => {
      localStorage.removeItem('token');
      setToken(null);
      setUser(null);
      setView('login');
    };

    return (
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow-sm">
          <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
            <h1 className="text-xl font-bold">🎙️ Podcast MVP</h1>
            <div className="flex items-center gap-4">
              <span className="text-gray-600">{user?.email}</span>
              <button
                onClick={handleLogout}
                className="bg-gray-200 px-4 py-2 rounded hover:bg-gray-300"
              >
                Logout
              </button>
            </div>
          </div>
        </nav>

        <div className="max-w-6xl mx-auto px-4 py-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">My Podcasts</h2>
            <button
              onClick={() => setShowNewPodcastForm(true)}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              + New Podcast
            </button>
          </div>

          {showNewPodcastForm && (
            <div className="bg-white p-6 rounded-lg shadow-md mb-6">
              <h3 className="text-lg font-bold mb-4">Create New Podcast</h3>
              <form onSubmit={createPodcast}>
                <div className="mb-4">
                  <label className="block text-gray-700 text-sm font-bold mb-2">
                    Title
                  </label>
                  <input
                    type="text"
                    value={newPodcastTitle}
                    onChange={(e) => setNewPodcastTitle(e.target.value)}
                    className="w-full px-3 py-2 border rounded"
                    required
                  />
                </div>
                <div className="mb-4">
                  <label className="block text-gray-700 text-sm font-bold mb-2">
                    Description
                  </label>
                  <textarea
                    value={newPodcastDescription}
                    onChange={(e) => setNewPodcastDescription(e.target.value)}
                    className="w-full px-3 py-2 border rounded h-24"
                  />
                </div>
                <div className="flex gap-2">
                  <button
                    type="submit"
                    className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                  >
                    Create
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowNewPodcastForm(false)}
                    className="bg-gray-200 px-4 py-2 rounded hover:bg-gray-300"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}

          {loading ? (
            <p>Loading podcasts...</p>
          ) : podcasts.length === 0 ? (
            <div className="bg-white p-12 rounded-lg shadow-md text-center">
              <p className="text-gray-600 mb-4">
                You don't have any podcasts yet.
              </p>
              <button
                onClick={() => setShowNewPodcastForm(true)}
                className="bg-blue-500 text-white px-6 py-3 rounded hover:bg-blue-600"
              >
                Create Your First Podcast
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {podcasts.map((podcast) => (
                <div
                  key={podcast.id}
                  className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition"
                >
                  <h3 className="font-bold text-lg mb-2">{podcast.title}</h3>
                  <p className="text-gray-600 text-sm mb-4">
                    {podcast.description || 'No description'}
                  </p>
                  <div className="text-xs text-gray-400">
                    Created {new Date(podcast.created_at).toLocaleDateString()}
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="mt-12 bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="font-bold text-lg mb-3">✅ What's Working:</h3>
            <ul className="list-disc list-inside space-y-2 text-sm mb-6">
              <li>User signup and login (JWT auth)</li>
              <li>Create and list podcasts</li>
              <li>Database connection (PostgreSQL)</li>
            </ul>

            <h3 className="font-bold text-lg mb-3">🚧 Next Steps:</h3>
            <ul className="list-disc list-inside space-y-2 text-sm">
              <li>Add WebRTC recording component (see MVP_TECHNICAL_SPEC.md lines 550-650)</li>
              <li>Add S3 upload for audio files (see lines 400-450)</li>
              <li>Add Celery for background processing (see lines 800-950)</li>
              <li>Add Whisper transcription (see lines 900-950)</li>
              <li>Add Claude show notes generation (see lines 950-1000)</li>
              <li>Add Stripe billing (see lines 450-500)</li>
            </ul>
          </div>
        </div>
      </div>
    );
  };

  // ========== MAIN RENDER ==========

  if (!token) {
    return view === 'signup' ? <SignupForm /> : <LoginForm />;
  }

  return <Dashboard />;
}

export default App;
