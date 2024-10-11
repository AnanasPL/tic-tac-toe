import React from 'react'
import { Link } from 'react-router-dom'

export const ErrorPage = () => {
  return (
    <div className='error'>
      Error Page
      <Link to='/' >Go back to the main page </Link>
    </div>
  )
}
