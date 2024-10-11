import React from 'react'

const WinnerInfo = ({ hide, children }) => {
  return (
    <div className='overlay'>
      <div className='modal'>
        {children}
        <button onClick={hide}>Restartuj Gre</button>
      </div>
    </div>
  )
}

export default WinnerInfo