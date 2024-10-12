import { useCallback, useContext, useEffect, useRef, useState } from 'react';

import { socketContext } from '../contexts/socketContext';
import { modalVisibleContext } from '../contexts/modalContext';

const useGameProgress = () => {
  const { addMessageListener, removeMessageListener } = useContext(socketContext);

  const hasGameStarted = useRef(false);
  const hasGameEnded = useRef(false);

  const [winner, setWinner] = useState(null);
  const [playAgainState, setPlayAgainState] = useState({ O: null, X: null })

  const gameStarted = () => hasGameStarted.current

  const restartRequestFn = useCallback(({ symbol }) => {
      setPlayAgainState({...playAgainState, [symbol]: `\u2714`})
  }, [playAgainState])

  useEffect(() => {   
    addMessageListener('restart-request', restartRequestFn, true)
    
    return () => removeMessageListener('restart-request', restartRequestFn)
  }, [restartRequestFn])


  useEffect(() => {
    const startGame = () => hasGameStarted.current = true;
    
    const endGame = ({ winner }) => {
      hasGameEnded.current = true;
      setWinner(winner)
    }
    const restartGame = () => {
      hasGameStarted.current = true;
      hasGameEnded.current = false;
      setWinner(null)
      setPlayAgainState({ O: null, X: null})
    };

    addMessageListener('game-started', startGame);
    addMessageListener('game-ended', endGame);
    addMessageListener('game-restarted', restartGame)

    return () => {
      removeMessageListener('game-started', startGame);
      removeMessageListener('game-ended', endGame);
      removeMessageListener('game-restarted', restartGame);
    }
  }, []);
  
  return { gameStarted, winner, playAgainState };
};

export default useGameProgress;