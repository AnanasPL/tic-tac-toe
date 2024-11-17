import React from 'react';

import { Link } from 'react-router-dom';

interface BasicErrorPageProps {
    message: string
}

const BasicErrorPage = ({ message }: BasicErrorPageProps) => {
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
        {message}
      </div>
    </>
  );
}

export default BasicErrorPage;