import React from 'react'
import { Link } from 'react-router-dom'

const WinnerInfo = ({ hide, children }) => {
  return (
    <div className='overlay'>
      <div className='modal'>
        {children}
        <button onClick={hide}>Zagrać ponownie?</button>
        <Link to={'/'}>
          <button>
            Strona Główna
          </button>
        </Link>
      </div>
    </div>
  )
}

export default WinnerInfo