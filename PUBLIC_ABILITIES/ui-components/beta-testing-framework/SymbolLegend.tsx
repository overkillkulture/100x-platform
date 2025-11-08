'use client';

import { useState } from 'react';

export default function SymbolLegend() {
  const [isOpen, setIsOpen] = useState(false);

  const symbols = [
    {
      icon: '🔧',
      label: 'BETA',
      description: 'Rough draft / Work in progress - expect bugs and changes',
      color: '#ff6b00'
    },
    {
      icon: '✅',
      label: 'STABLE',
      description: 'Feature is tested and working reliably',
      color: '#00ff88'
    },
    {
      icon: '🚧',
      label: 'CONSTRUCTION',
      description: 'Actively being built - may not work at all',
      color: '#ffaa00'
    },
    {
      icon: '⚡',
      label: 'LIVE',
      description: 'Real-time data / Active system',
      color: '#00ccff'
    },
    {
      icon: '⚠️',
      label: 'CAUTION',
      description: 'Known issues or experimental feature',
      color: '#ff4444'
    },
    {
      icon: '🎯',
      label: 'CORE',
      description: 'Essential system component',
      color: '#00ff88'
    },
    {
      icon: '💡',
      label: 'NEW',
      description: 'Recently added feature',
      color: '#ffdd00'
    },
  ];

  return (
    <>
      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          backgroundColor: '#00ff88',
          color: '#000',
          border: '2px solid #00ccff',
          borderRadius: '50%',
          width: '60px',
          height: '60px',
          fontSize: '24px',
          cursor: 'pointer',
          boxShadow: '0 4px 15px rgba(0, 255, 136, 0.5)',
          zIndex: 9998,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontWeight: 'bold',
          transition: 'all 0.3s ease'
        }}
        onMouseOver={(e) => {
          e.currentTarget.style.transform = 'scale(1.1)';
          e.currentTarget.style.backgroundColor = '#00ccff';
        }}
        onMouseOut={(e) => {
          e.currentTarget.style.transform = 'scale(1)';
          e.currentTarget.style.backgroundColor = '#00ff88';
        }}
        title="Open Symbol Legend"
      >
        ?
      </button>

      {/* Legend Modal */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          bottom: '90px',
          right: '20px',
          backgroundColor: '#0a0e27',
          border: '2px solid #00ff88',
          borderRadius: '10px',
          padding: '20px',
          boxShadow: '0 8px 30px rgba(0, 255, 136, 0.3)',
          zIndex: 9998,
          minWidth: '350px',
          maxWidth: '450px',
          fontFamily: 'monospace',
          color: '#00ff88'
        }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '15px',
            borderBottom: '2px solid #00ff88',
            paddingBottom: '10px'
          }}>
            <h3 style={{ margin: 0, fontSize: '18px', color: '#00ccff' }}>
              📋 Symbol Legend
            </h3>
            <button
              onClick={() => setIsOpen(false)}
              style={{
                background: 'none',
                border: 'none',
                color: '#ff4444',
                fontSize: '20px',
                cursor: 'pointer',
                padding: '0',
                lineHeight: '1'
              }}
            >
              ✕
            </button>
          </div>

          <div style={{ fontSize: '12px', marginBottom: '15px', color: '#00ccff', opacity: 0.8 }}>
            These symbols help you understand the status of features throughout the system.
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {symbols.map((symbol, index) => (
              <div
                key={index}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '10px',
                  padding: '10px',
                  backgroundColor: 'rgba(0, 255, 136, 0.05)',
                  borderLeft: `4px solid ${symbol.color}`,
                  borderRadius: '5px'
                }}
              >
                <span style={{ fontSize: '20px', flexShrink: 0 }}>{symbol.icon}</span>
                <div style={{ flex: 1 }}>
                  <div style={{
                    fontWeight: 'bold',
                    color: symbol.color,
                    marginBottom: '3px',
                    fontSize: '13px'
                  }}>
                    {symbol.label}
                  </div>
                  <div style={{ fontSize: '11px', color: '#00ff88', opacity: 0.8, lineHeight: '1.4' }}>
                    {symbol.description}
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div style={{
            marginTop: '15px',
            padding: '10px',
            backgroundColor: 'rgba(255, 107, 0, 0.1)',
            borderRadius: '5px',
            fontSize: '11px',
            color: '#ffaa00',
            borderLeft: '3px solid #ff6b00'
          }}>
            <strong>Remember:</strong> This entire system is in active development.
            Report any issues you encounter - no bug is too small!
          </div>
        </div>
      )}
    </>
  );
}
