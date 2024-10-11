import { useContext, useEffect, useRef, useState } from 'react';

import { socketContext } from '../contexts/socketContext';
import { messageContext } from '../contexts/messageContext';
import { modalVisibleContext } from '../contexts/modalContext';

const useGameProgress = (setPlayAgain) => {
  const { addMessageListener, removeMessageListener } = useContext(socketContext);
  const setMessage = useContext(messageContext)

  const hasGameStarted = useRef(false);
  const hasGameEnded = useRef(false);

  const [winner, setWinner] = useState(null);

  const gameInProgress = () => {
    if (!hasGameStarted.current) {
      setMessage('Poczekaj na rozpoczęcie gry');
      return false;
    };

    return !hasGameEnded.current;
  };

  
  useEffect(() => {
    const gameStartedFn = () => hasGameStarted.current = true;
    
    const gameEndedFn = ({ winner }) => {
      hasGameEnded.current = true;
      setWinner(winner)
      setPlayAgain(0)
    }
    const restartGame = () => {
      hasGameStarted.current = true;
      hasGameEnded.current = false;
      setWinner(null)
    };

    addMessageListener('game-started', gameStartedFn);
    addMessageListener('game-ended', gameEndedFn);
    addMessageListener('game-restarted', restartGame)

    return () => {
      removeMessageListener('game-started', gameStartedFn);
      removeMessageListener('game-ended', gameEndedFn);
      removeMessageListener('game-restarted', restartGame);
    }
  }, []);
  
  return { gameInProgress, winner };
};

export default useGameProgress;