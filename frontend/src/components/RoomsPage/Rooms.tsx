import React, { useEffect, useState } from 'react';

import { useSocketContext } from '../../contexts/socketContext';

import Room from './RoomInfo';
import AddRoom from './AddRoom';

const Rooms = () => {
  const [rooms, setRooms] = useState<[string, number][]>([]);
  const { emit, addMessageListener, removeMessageListener } = useSocketContext();

  useEffect(() => {
    const roomsUpdateFn = ({ rooms }: {rooms: [string, number][]}) => setRooms(rooms);
    
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
}

export default Rooms;