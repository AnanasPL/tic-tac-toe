import { createContext, useContext } from 'react';

type setMessageType = (a: string) => void;

export const messageContext = createContext<setMessageType | undefined>(undefined);

export const useMessageContext = () => {
  const setMessage = useContext(messageContext);

  if (setMessage === undefined) throw new Error("Must be used in a context provider");

  return setMessage;
}
