import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const RoomNotFound = () => {
  const {state: { code }} = useLocation();

  return (
    <div>
      There is no room with the code: {code}
      <Link to='/'>
        Back to the Main Page
      </Link>
    </div>
  );
};

export default RoomNotFound;