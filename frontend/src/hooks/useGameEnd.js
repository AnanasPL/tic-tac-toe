import { useCallback, useContext, useEffect, useState, useRef } from 'react';

import socketContext from '../contexts/socketContext';

const useGameEnd = (setVisible) => {
  const { addMessageListener, removeMessageListener } = useContext(socketContext);

  const [playAgainState, setPlayAgainState] = useState({ O: null, X: null });
  const winnerRef = useRef({ text: '', symbol: '' });

  const restartRequestFn = useCallback(({ symbol }) => {
    setPlayAgainState({...playAgainState, [symbol]: `\u2714`});
  }, [playAgainState]);

  useEffect(() => {   
    addMessageListener('restart-request', restartRequestFn, true);
    
    return () => removeMessageListener('restart-request', restartRequestFn);
  }, [restartRequestFn]);
  
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