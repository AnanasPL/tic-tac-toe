import React from 'react';

import { useLocation } from 'react-router-dom';

import BasicErrorPage from './BasicErrorPage';

const RoomNotFound = () => {
  const location = useLocation();
  
  let message = 'There is no room with the code: ';
  
  if (location.state) {
    message += location.state.code;
  }
  
  return <BasicErrorPage message={message} />;
}

export default RoomNotFound;