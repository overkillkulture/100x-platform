'use client';

import { useState } from 'react';

export default function BetaNotice() {
  const [isMinimized, setIsMinimized] = useState(false);

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      backgroundColor: '#ff6b00',
      color: '#000',
      padding: isMinimized ? '8px 20px' : '15px 20px',
      zIndex: 9999,
      borderBottom: '3px solid #ff8800',
      boxShadow: '0 4px 10px rgba(255, 107, 0, 0.5)',
      fontFamily: 'monospace',
      fontSize: isMinimized ? '12px' : '14px',
      fontWeight: 'bold',
      cursor: 'pointer',
      transition: 'all 0.3s ease'
    }}
    onClick={() => setIsMinimized(!isMinimized)}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', maxWidth: '1400px', margin: '0 auto' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{ fontSize: isMinimized ? '16px' : '24px' }}>⚠️</span>
          {!isMinimized && (
            <>
              <span style={{ fontSize: '18px' }}>BETA TEST MODE - WE NEED YOUR HELP!</span>
              <span style={{ marginLeft: '10px', fontSize: '14px', opacity: 0.9 }}>
                Please click around, test everything, and report ANY bugs you find!
              </span>
            </>
          )}
          {isMinimized && (
            <span>BETA - Click to expand</span>
          )}
        </div>
        <span style={{ fontSize: '12px', opacity: 0.8 }}>
          {isMinimized ? '▼' : '▲'}
        </span>
      </div>
      {!isMinimized && (
        <div style={{
          marginTop: '10px',
          padding: '10px',
          backgroundColor: 'rgba(0, 0, 0, 0.2)',
          borderRadius: '5px',
          fontSize: '12px'
        }}>
          <strong>How to help:</strong> Try every feature, click every button, fill out forms, navigate between pages.
          If something breaks, looks weird, or doesn't make sense - that's exactly what we need to know!
          Look for the <span style={{backgroundColor: '#000', color: '#ff6b00', padding: '2px 6px', borderRadius: '3px'}}>🔧 BETA</span> symbol
          to identify rough draft features.
        </div>
      )}
    </div>
  );
}
