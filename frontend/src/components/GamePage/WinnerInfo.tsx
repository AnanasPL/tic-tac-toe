import React, { useState } from 'react';

import { Link } from 'react-router-dom';

import { useSocketContext } from '../../contexts/socketContext';

import useGameEnd from '../../hooks/useGameEnd';

import PlayAgainStatus from './PlayAgainStatus';

const WinnerInfo = () => {
	const { emit } = useSocketContext();
	
  const [visible, setVisible] = useState(false);
	const [winner, playAgainState] = useGameEnd(setVisible);

	if (!visible) return;

	return (
		<div className='overlay'>
			<div className='modal'>
        <div>
          <div className='result-info'>{winner.text}</div>
          <div className='winner-symbol'>{winner.symbol}</div>
        </div>
        
        <PlayAgainStatus status={playAgainState}/>

        <div className='buttons'>
          <button onClick={() => emit('restart-request')}>
            Play again?
          </button>

          <Link to='/'>
            <button>Main Page</button>
          </Link>
        </div>
			</div>
		</div>
	);
}

export default WinnerInfo;