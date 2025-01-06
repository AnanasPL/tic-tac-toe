import { useCallback, useEffect, useRef } from 'react';

import io, { Socket } from 'socket.io-client';

export interface socketFunctions {
  emit: (message: string, data?: unknown) => void,
  addMessageListener: (message: string, listenerFn: (...args: any[]) => void, oneTime?: boolean) => void,
  removeMessageListener: (message: string, listenerFn: (...args: any[]) => void) => void,
}

const useSocket: () => socketFunctions = () => {
  const socketRef = useRef<Socket>(io('https://tic-tac-toe-c7wa.onrender.com'));

  const emit = useCallback((message: string, data?: unknown) => {
    if (data === undefined) {
      socketRef.current.emit(message);
      return;
    }

    socketRef.current.emit(message, data);
  }, []);

  const addMessageListener = useCallback((message: string, listenerFn: (...args: any[]) => void, oneTime: boolean = false) => {
    if (oneTime) socketRef.current.once(message, listenerFn);
    else socketRef.current.on(message, listenerFn);
  }, []);

  const removeMessageListener = useCallback((message: string, listenerFn: (...args: any[]) => void) => {
    socketRef.current.off(message, listenerFn);
  }, []);

  useEffect(() => () => {
      socketRef.current.disconnect();
    }, []);

  return { emit, addMessageListener, removeMessageListener } as const;
}

export default useSocket;