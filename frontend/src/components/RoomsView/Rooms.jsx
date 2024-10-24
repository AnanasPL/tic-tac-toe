import React, { useContext, useEffect, useState } from 'react';

import socketContext from '../../contexts/socketContext';

import Room from './RoomInfo';
import AddRoom from './AddRoom';

const Rooms = () => {
  const [rooms, setRooms] = useState([]);
  const { emit, addMessageListener, removeMessageListener } = useContext(socketContext);

  useEffect(() => {
    const roomsUpdateFn = ({ rooms }) => setRooms(rooms);
    
    addMessageListener('rooms-update', roomsUpdateFn);

    emit('get-rooms');

    return () => removeMessageListener('rooms-update', roomsUpdateFn);
  }, []);

  return (
    <div className='rooms-wrapper'>
      <AddRoom />
      {rooms.map(([code, size], id) => <Room code={code} size={size} key={id}/>)}
    </div>
  );
};

export default Rooms;