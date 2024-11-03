import React from 'react';

interface MessageProps {
  message: string
}

const Message = ({ message }: MessageProps) => {
  return (
    <div className='message'>
      {message}
    </div>
  );
}

export default Message;