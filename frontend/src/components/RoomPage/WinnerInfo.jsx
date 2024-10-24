import React, { useContext, useState } from 'react';

import { Link } from 'react-router-dom';

import socketContext from '../../contexts/socketContext';

import useGameEnd from '../../hooks/useGameEnd';

import PlayAgainStatus from './PlayAgainStatus';

const WinnerInfo = () => {
	const { emit } = useContext(socketContext);
	
  const [visible, setVisible] = useState(false);
	const [winner, playAgainState] = useGameEnd(setVisible);

	if (!visible) return;

	return (
		<div className='overlay'>
			<div className='modal'>
        <div>
          <p>{winner.text}</p>
          <p style={{ fontSize: 60 }}>{winner.symbol}</p>
        </div>
        
        <PlayAgainStatus status={playAgainState}/>

				<button onClick={() => emit('restart-request')}>
					Play again?
				</button>

				<Link to='/'>
					<button>Main Page</button>
				</Link>
			</div>
		</div>
	);
};

export default WinnerInfo;