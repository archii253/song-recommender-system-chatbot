import { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [recommendations, setRecommendations] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || `Server error: ${res.status}`);
      }

      const data = await res.json();
      setResponse(data.response_text);
      setRecommendations(data.recommendations);

    } catch (err) {
      setResponse("Error: "+ err.message);
      setRecommendations([]); // Clear previous recommendations
    console.error("API Error:", err);
  }
};

  return (
    <div className="app-container"> {/* ← Main container div */}
      <h1>Song Recommender Chatbot</h1>
      <form onSubmit={handleSubmit}>
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask for song recommendations..."
        />
        <button type="submit">Send</button>
      </form>

      {response && <p>{response}</p>}
      {response && (
      response.startsWith("Error:") ? (
        <p className="error-message">{response}</p>
      ) : (
        <p className="success-message">{response}</p>
      )
    )}

      <div className="recommendations-container"> {/* ← Recommendations wrapper */}
        {recommendations.map((song, index) => (
          <div key={index} className="song-item"> {/* ← Individual song div */}
            <p><strong>{song.track}</strong> by {song.artist}</p>
            <a 
              href={song.youtube_link} 
              target="_blank" 
              rel="noopener noreferrer"
              className="youtube-link"
            >
              Watch on YouTube
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;