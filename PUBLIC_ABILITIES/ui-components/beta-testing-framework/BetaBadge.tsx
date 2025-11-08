'use client';

type BetaBadgeType = 'beta' | 'stable' | 'construction' | 'live' | 'caution' | 'core' | 'new';

interface BetaBadgeProps {
  type?: BetaBadgeType;
  text?: string;
  size?: 'small' | 'medium' | 'large';
}

export default function BetaBadge({ type = 'beta', text, size = 'small' }: BetaBadgeProps) {
  const configs = {
    beta: {
      icon: '🔧',
      label: 'BETA',
      bg: '#ff6b00',
      color: '#000'
    },
    stable: {
      icon: '✅',
      label: 'STABLE',
      bg: '#00ff88',
      color: '#000'
    },
    construction: {
      icon: '🚧',
      label: 'WIP',
      bg: '#ffaa00',
      color: '#000'
    },
    live: {
      icon: '⚡',
      label: 'LIVE',
      bg: '#00ccff',
      color: '#000'
    },
    caution: {
      icon: '⚠️',
      label: 'CAUTION',
      bg: '#ff4444',
      color: '#fff'
    },
    core: {
      icon: '🎯',
      label: 'CORE',
      bg: '#00ff88',
      color: '#000'
    },
    new: {
      icon: '💡',
      label: 'NEW',
      bg: '#ffdd00',
      color: '#000'
    }
  };

  const config = configs[type];
  const displayText = text || config.label;

  const sizes = {
    small: {
      fontSize: '10px',
      padding: '2px 6px',
      iconSize: '12px'
    },
    medium: {
      fontSize: '12px',
      padding: '4px 8px',
      iconSize: '14px'
    },
    large: {
      fontSize: '14px',
      padding: '6px 12px',
      iconSize: '16px'
    }
  };

  const sizeConfig = sizes[size];

  return (
    <span style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: '4px',
      backgroundColor: config.bg,
      color: config.color,
      padding: sizeConfig.padding,
      borderRadius: '4px',
      fontSize: sizeConfig.fontSize,
      fontWeight: 'bold',
      fontFamily: 'monospace',
      marginLeft: '6px',
      verticalAlign: 'middle',
      boxShadow: `0 2px 6px ${config.bg}66`,
      border: `1px solid ${config.color}33`,
      cursor: 'help',
      transition: 'all 0.2s ease'
    }}
    title={`This feature is ${type.toUpperCase()}`}
    onMouseOver={(e) => {
      e.currentTarget.style.transform = 'scale(1.05)';
      e.currentTarget.style.boxShadow = `0 3px 10px ${config.bg}99`;
    }}
    onMouseOut={(e) => {
      e.currentTarget.style.transform = 'scale(1)';
      e.currentTarget.style.boxShadow = `0 2px 6px ${config.bg}66`;
    }}>
      <span style={{ fontSize: sizeConfig.iconSize }}>{config.icon}</span>
      <span>{displayText}</span>
    </span>
  );
}
