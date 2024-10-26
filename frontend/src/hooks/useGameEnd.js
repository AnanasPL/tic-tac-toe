import { useContext, useEffect, useState, useRef } from 'react';

import socketContext from '../contexts/socketContext';

const useGameEnd = (setVisible) => {
  const { addMessageListener, removeMessageListener } = useContext(socketContext);

  const [playAgainState, setPlayAgainState] = useState({ O: null, X: null });
  const winnerRef = useRef({ text: '', symbol: '' });

  useEffect(() => {   
    const playAgainStateUpdateFn = (newState) => {     
      newState = Object.fromEntries(Object.entries(newState).map(([sym, v]) => 
        [sym, v === null ? null : v ? `\u2714` : `\u2717`]
      ))
      
      console.log(newState)

      setPlayAgainState(newState);
    };

    addMessageListener('play-again-state-update', playAgainStateUpdateFn, true);
    
    return () => removeMessageListener('play-again-state-update', playAgainStateUpdateFn);
  }, [playAgainState]);
  
	useEffect(() => {
    const gameEndedFn = ({ winner, symbol }) => {
      winnerRef.current = { 
        text: symbol ? (winner ? 'YOU WON!' : 'YOU LOST!') : 'TIE!',
			  symbol: symbol ? symbol : 'O / X' //placeholder
      };
			setVisible(true);
		};

    const restartGameFn = () => {
      setPlayAgainState({ O: null, X: null });
      setVisible(false);
    };
    
		addMessageListener('game-ended', gameEndedFn);
    addMessageListener('game-restarted', restartGameFn);

		return () => {
      removeMessageListener('game-ended', gameEndedFn);
		  removeMessageListener('game-restarted', restartGameFn);
    };
  }, [setVisible]);

  return [winnerRef.current, playAgainState];
};

export default useGameEnd;