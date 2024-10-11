import { useState, useEffect, useContext } from "react";
import { socketContext } from "../../contexts/socketContext";
import { messageContext } from "../../contexts/messageContext";

const useBoardState = (playerSymbol, setCurrentPlayer) => {
  const [boardState, setBoardState] = useState(Array(9).fill(''));
  const { addMessageListener, removeMessageListener } =  useContext(socketContext);
  const setMessage = useContext(messageContext)

  useEffect(() => {
    const boardUpdateFn = ({ changedCell: { index, symbol }}) => {
      const newBoardState = [...boardState];
      newBoardState[index] = symbol;
      setBoardState(newBoardState);
      setCurrentPlayer(symbol !== playerSymbol.current);
      setMessage('')
    }
    
    addMessageListener('board-update', boardUpdateFn, true);
    return () => removeMessageListener('board-update', boardUpdateFn)
  }, [boardState]);

  useEffect(() => {
    const clearBoardFn = () => {
      setBoardState(Array(9).fill(''))
    }

    addMessageListener('board-clear', clearBoardFn)
    
    return () => removeMessageListener('board-clear', clearBoardFn)
  }, [])

  return boardState;
};

export default useBoardState;