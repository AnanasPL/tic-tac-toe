import { useState, useEffect } from 'react';

import { useSocketContext } from '@/contexts/socketContext';
import { useMessageContext } from '@/contexts/messageContext';

const useBoardState = () => {
  const [boardState, setBoardState] = useState<string[]>(Array(9).fill(''));

  const { addMessageListener, removeMessageListener } = useSocketContext();
  const setMessage = useMessageContext();

  useEffect(() => {
    const boardUpdateFn = (newState: string[]) => {
      setBoardState(newState);
      setMessage('');
    }

    const boardUpdateErrorFn = (message: string) => setMessage(message);
    
    addMessageListener('board-update', boardUpdateFn, true);
    addMessageListener('board-update-error', boardUpdateErrorFn, true);

    return () => {
      removeMessageListener('board-update', boardUpdateFn);
      removeMessageListener('board-update-error', boardUpdateErrorFn);
    }
  }, [boardState, setMessage]);

  return boardState;
}

export default useBoardState;