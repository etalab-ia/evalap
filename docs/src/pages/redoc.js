import React, { useEffect } from 'react';

export default function RedocRedirect() {
  useEffect(() => {
    const isDev = window.location.port === '3000';
    if (isDev) {
      window.location.href = 'http://localhost:8000/redoc';
    } else {
      // In production, this route should normally be intercepted by a reverse proxy.
      // If it reaches here, we try to go to the server-side /redoc.
      window.location.href = '/redoc';
    }
  }, []);

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <p>Redirecting to API Reference...</p>
      <p>If you are not redirected, <a href="http://localhost:8000/redoc">click here (Local)</a> or <a href="/redoc">click here (Production)</a>.</p>
    </div>
  );
}
