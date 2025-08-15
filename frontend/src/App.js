import React from 'react';

function App() {
  return (
    <div style={{
      backgroundColor: '#1a1a1a',
      color: 'white',
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'Arial, sans-serif'
    }}>
      <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>
        🎬 RENDEREEL STUDIO
      </h1>
      <p style={{ fontSize: '1.5rem', marginBottom: '2rem' }}>
        Professional AI Creative Platform
      </p>
      <div style={{ 
        padding: '1rem 2rem', 
        backgroundColor: '#8B5CF6', 
        borderRadius: '8px',
        fontSize: '1.2rem'
      }}>
        🚀 Platform Loading Successfully!
      </div>
      <p style={{ marginTop: '2rem', opacity: 0.7 }}>
        Full features coming soon...
      </p>
    </div>
  );
}

export default App;
