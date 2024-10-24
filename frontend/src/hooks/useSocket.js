import { useEffect, useRef } from 'react';

import io from 'socket.io-client';

const useSocket = () => {
  const socketRef = useRef(io('http://localhost:5000'));
  const listeners = useRef({});

  const emit = (message, data = null) => {
    if (data === null) {
      socketRef.current.emit(message);
      return;
    }

    socketRef.current.emit(message, data);
  };

  const addMessageListener = (message, listenerFn, oneTime = false) => {
    if (listeners.current[message] === undefined) listeners.current[message] = [];
    if (listeners.current[message].includes(listenerFn)) return;
    
    if (oneTime) {
      socketRef.current.once(message, listenerFn);
    } else {
      socketRef.current.on(message, listenerFn);
    }
    
    listeners.current[message].push(listenerFn);
  };

  const removeMessageListener = (message, listenerFn) => {
    if (listeners.current[message] === undefined) return;
    
    socketRef.current.off(message, listenerFn);

    const index = listeners.current[message].indexOf(listenerFn);
    if (index === -1) return;
    
    listeners.current[message].splice(index, 1);
  };

  useEffect(() => () => socketRef.current.disconnect(), []);

  return {emit, addMessageListener, removeMessageListener};
};

export default useSocket;