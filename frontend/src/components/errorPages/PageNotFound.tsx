import React from 'react';

import { Link } from 'react-router-dom';

const PageNotFound = () => {
  return (
    <>
      <div className='go-back-button'>
        <Link to='/'>
          <button>
            Go back to the main page
          </button>
        </Link>
      </div>
      <div className='error-message'>
        Page was not found
      </div>
    </>
  );
}

export default PageNotFound;