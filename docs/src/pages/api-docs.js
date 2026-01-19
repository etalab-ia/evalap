import React, { useEffect } from 'react';

export default function ApiDocsRedirect() {
  useEffect(() => {
    const isDev = window.location.port === '3000';
    if (isDev) {
      window.location.href = 'http://localhost:8000/api-docs';
    } else {
      window.location.href = '/api-docs';
    }
  }, []);

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <p>Redirecting to API Reference (Swagger)...</p>
      <p>If you are not redirected, <a href="http://localhost:8000/api-docs">click here (Local)</a> or <a href="/api-docs">click here (Production)</a>.</p>
    </div>
  );
}
