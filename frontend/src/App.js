import React, { useState } from 'react';
import './App.css';
import { FaSearch } from 'react-icons/fa';

function App() {
  const [keywords, setKeywords] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [apiKey, setApiKey] = useState('my-very-secret-api-key'); // Domyślnie ustawiony API key
  const [result, setResult] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    let timeframe = '';
    if (startDate && endDate) {
      timeframe = `${startDate} ${endDate}`;
    }
    const response = await fetch(`http://127.0.0.1:8000/trend?keywords=${keywords}&timeframe=${timeframe}`, {
      headers: {
        'Authorization': `Bearer ${apiKey}`
      }
    });
    const data = await response.json();
    setResult(data);
  };

  return (
    <div className="App">
      <h1>Google Trends Search</h1>
      <form onSubmit={handleSubmit} className="search-form">
        <div className="search-input-container">
          <FaSearch className="search-icon" />
          <input
            type="text"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            placeholder="Enter keywords..."
            required
          />
        </div>
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          required
          style={{ marginTop: '10px', padding: '10px', width: '300px' }}
        />
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          required
          style={{ marginTop: '10px', padding: '10px', width: '300px' }}
        />
        <button type="submit" style={{ marginTop: '10px' }}>Search</button>
      </form>
      {result && (
        <div className="result">
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;