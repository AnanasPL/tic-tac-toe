import React from 'react';

interface PlayAgainStatusProps {
  status: {
    O: string | null,
    X: string | null
  }
}

const PlayAgainStatus = ({ status }: PlayAgainStatusProps) => {
  return (
    <div className="players-play-again-status-wrapper">
      <div className="player-status-wrapper">
        <div className="player-symbol">O</div>
        <div className="play-again-status">{status.O}</div>
      </div>
      <div className="player-status-wrapper">
        <div className="play-again-status">{status.X}</div>
        <div className="player-symbol">X</div>
      </div>
    </div>
  );
}

export default React.memo(PlayAgainStatus);