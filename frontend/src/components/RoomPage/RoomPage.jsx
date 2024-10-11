import React, { useContext, useState, useEffect } from 'react';
import Board from './Board';
import Message from './Message';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { socketContext } from '../../contexts/socketContext';
import { messageContext } from '../../contexts/messageContext'
import { modalContext } from '../../contexts/modalContext';
import WinnerInfo from './WinnerInfo';

const RoomPage = () => {
  const {emit, addMessageListener, removeMessageListener} = useContext(socketContext)

  const [message, setMessage] = useState('');
  const [roomExists, setRoomExists] = useState(false)

  const { roomCode } = useParams()
  const navigate = useNavigate()


  useEffect(() => {
    const checkForRoomFn = ({ exists }) => {
      if (exists) {
        setRoomExists(true)
      } else {
        navigate('/room-not-found', { state: { code: roomCode }})
      }
    }

    addMessageListener('check-if-room-exists-response', checkForRoomFn)

    emit('check-if-room-exists', {code: roomCode})

    return () => removeMessageListener('check-if-room-exists-response', checkForRoomFn)
  }, [])

  return (
    <messageContext.Provider value={setMessage}>
     <modalContext.Provider>
        {roomExists && (<>
            <Link to={'/'}>Go back to the main page</Link>
            <Board />
            <Message message={message}/>
          </>)}
      </modalContext.Provider> 
    </messageContext.Provider>
  );
};

export default RoomPage;