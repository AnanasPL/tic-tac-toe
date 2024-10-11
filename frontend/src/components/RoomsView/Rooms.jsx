import React, { useContext, useEffect, useState } from "react";
import Room from "./RoomInfo";
import AddRoom from "./AddRoom";
import { roomContext } from "../../contexts/roomContext";
import { socketContext } from "../../contexts/socketContext";

const Rooms = () => {
    const [rooms, setRooms] = useState([])
    const { emit, addMessageListener, removeMessageListener } = useContext(socketContext);

    useEffect(() => {
        const roomsUpdateFn = ({ rooms }) => setRooms(rooms)
        
        addMessageListener('rooms-update', roomsUpdateFn)

        emit('get-rooms')

        return () => removeMessageListener('rooms-update', roomsUpdateFn)
    }, [])

    return (
        <div className="rooms-wrapper">
            <roomContext.Provider value={[rooms, setRooms]}>
                <AddRoom />
                {rooms.map((info, id) => <Room code={info[0]} size={info[1]} key={id}/>)}
            </roomContext.Provider>
        </div>
    )
}

export default Rooms