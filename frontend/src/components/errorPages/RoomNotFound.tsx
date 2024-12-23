import React from 'react';

import { useLocation } from 'react-router-dom';

import BasicErrorPage from './BasicErrorPage';

const RoomNotFound = () => {
  const { state: { code }} = useLocation();

  return <BasicErrorPage message={'There is no room with the code: ' + code} />;
}

export default RoomNotFound;