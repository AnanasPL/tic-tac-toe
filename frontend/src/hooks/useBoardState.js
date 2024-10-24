import { useState, useEffect, useContext } from "react";
import { socketContext } from "../contexts/socketContext";
import { messageContext } from "../contexts/messageContext";

const useBoardState = () => {
  const [boardState, setBoardState] = useState(Array(9).fill(''));
  const { addMessageListener, removeMessageListener } =  useContext(socketContext);
  const setMessage = useContext(messageContext)

  useEffect(() => {
    const boardUpdateFn = (newState) => {
      setBoardState(newState);
      setMessage('')
    }

    const boardUpdateErrorFn = (message) => setMessage(message)
    
    addMessageListener('board-update', boardUpdateFn, true);
    addMessageListener('board-update-error', boardUpdateErrorFn, true);

    return () => {
      removeMessageListener('board-update', boardUpdateFn)
      removeMessageListener('board-update-error', boardUpdateErrorFn, true);
    }
  }, [boardState, setMessage]);

  return boardState;
};

export default useBoardState;