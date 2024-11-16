import React from 'react';

import { Link, useLocation } from 'react-router-dom';

const RoomNotFound = () => {
  const { state: { code } } = useLocation();

  return (
    <>
      <div className='go-back-button'>
        <Link to='/'>
          <button>
            Back to the Main Page
          </button>
        </Link>
      </div>
      <div className='error-message'>
        There is no room with the code: {code}
      </div>
    </>
  );
}

export default RoomNotFound;