import React from 'react';

import { useLocation } from 'react-router-dom';

import BasicErrorPage from './BasicErrorPage';

const RoomNotFound = () => {
  let message = 'There is no room with the code: ';

  try {
    const { state: { code }} = useLocation();
    message += code;
  } catch (e) {}

  return <BasicErrorPage message={message} />;
}

export default RoomNotFound;