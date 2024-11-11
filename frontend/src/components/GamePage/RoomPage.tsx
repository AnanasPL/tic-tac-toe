import React, { useState, useEffect } from 'react';

import { Link, useNavigate, useParams } from 'react-router-dom';

import { useSocketContext } from '../../contexts/socketContext';
import { messageContext } from '../../contexts/messageContext';

import Board from './Board';
import Message from './Message';

const RoomPage = () => {
  const {emit, addMessageListener, removeMessageListener} = useSocketContext();

  const [message, setMessage] = useState('');
  const [roomExists, setRoomExists] = useState(false);

  const { roomCode } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const checkForRoomFn = (exists: boolean) => 
      exists ? 
      setRoomExists(true) : 
      navigate('/room-not-found', { state: { code: roomCode }});

    addMessageListener('check-if-room-exists-response', checkForRoomFn, true);

    emit('check-if-room-exists', roomCode);

    return () => removeMessageListener('check-if-room-exists-response', checkForRoomFn);
  }, []);

  return (roomExists && (<>
    <Link to='/'>
      Go back to the main page
    </Link>

    <messageContext.Provider value={setMessage}>
      <Board />
    </messageContext.Provider>

    <Message message={message}/>
    </>)
  );
}

export default RoomPage;