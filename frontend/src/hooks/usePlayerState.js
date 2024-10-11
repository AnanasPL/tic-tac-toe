import { useContext, useEffect, useRef, useState } from "react";
import { socketContext } from "../contexts/socketContext";

const usePlayerState = () => {
  const playerSymbol = useRef('');
  const [currentPlayer, setCurrentPlayer] = useState(false);
  const { addMessageListener, removeMessageListener } = useContext(socketContext);

  useEffect(() => {
    const assignPlayerInfoFn = ({ symbol, isCurrentPlayer }) => {
      playerSymbol.current = symbol;
      setCurrentPlayer(isCurrentPlayer);
    };

    addMessageListener('player-info', assignPlayerInfoFn);

    // Just in case, we don't want any listeners left in case message is not received
    return () => removeMessageListener('player-info', assignPlayerInfoFn);
  }, []);

  return { playerSymbol, currentPlayer, setCurrentPlayer };
};

export default usePlayerState;