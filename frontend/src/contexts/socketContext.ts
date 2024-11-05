import { createContext, useContext } from 'react';

import { socketFunctions } from '@/hooks/useSocket';

export const socketContext = createContext<socketFunctions | undefined>(undefined);

export const useSocketContext = () => {
  const socket = useContext(socketContext);

  if (socket === undefined) throw new Error("Must be used in a context provider");

  return socket;
}