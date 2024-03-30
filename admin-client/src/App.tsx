import { useState } from 'react'
import './App.css'
import { Routes, Route, Link } from 'react-router-dom'
import TestEmailForm from './components/TestEmailForm.js';
import EmailForm from './components/EmailForm.js';
import ViewForms from './components/ViewForms.js';
import ServerMonitor from './components/ServerMonitor.js';
const host = "http://0.0.0.0";
const port = 8080;
// const scriptSecret = "abc123";

export const local_endpoints = {
  test_email: `${host}:${port}/test-email`,
  send_email: `${host}:${port}/email`,
  forms: `${host}:${port}/forms`,
  unpaired: `${host}:${port}/unpaired`,
  paired: `${host}:${port}/pairs`,
  status: `${host}:${port}/status`,
}

const SendEmails = () => {
  const [testMode, setTestMode] = useState(false);
  return (
    <div>
      <button onClick={() => setTestMode(!testMode)}>
        {testMode ? 'Switch to Real Mode' : 'Switch to Test Mode'}
      </button>
      {testMode ? (
        <TestEmailForm endpoint={local_endpoints.test_email} />
      ) : (
        <EmailForm endpoint={local_endpoints.send_email} />
      )}
    </div>
  )
}

const Forms = () => {
  return <ViewForms />
}

const Monitor = () => {
  return <ServerMonitor endpoint={local_endpoints.status} />
}

const Navbar = () => {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Status</Link>
        </li>
        <li>
          <Link to="/emails">Send Emails</Link>
        </li>
        <li>
          <Link to="/forms">Forms</Link>
        </li>
      </ul>
    </nav>
  )
}

function App() {


  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route path="/emails" element={<SendEmails/>} />
        <Route path="/forms" element={<Forms/>} />
        <Route path="/" element={<Monitor/>} />
      </Routes>
    </div>
  )
}

export default App
