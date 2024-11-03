import { createContext, useContext } from 'react';

import { socketFunctions } from '@/hooks/useSocket';

export const socketContext = createContext<socketFunctions | undefined>(undefined);

export const useSocketContext = () => {
  const socketFunctions = useContext(socketContext);

  if (socketFunctions === undefined) throw new Error("Must be used in a context provider");

  return socketFunctions;
}