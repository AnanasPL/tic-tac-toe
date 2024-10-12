import React, { useContext, useEffect } from "react";
import { socketContext } from "../../contexts/socketContext";
import { useNavigate } from "react-router-dom";

const AddRoom = () => {
	const { emit, addMessageListener } = useContext(socketContext);
	const navigate = useNavigate()
	
	useEffect(() => {
		addMessageListener("room-created-successfully", ({ code }) => {
			navigate(`/room/${code}`)
		}, true);
	}, []); 

	return (
		<div className="addRoom">
			<button id="roomCreation" onClick={() => emit("create-room")}>
				Create New Room
			</button>
            <button onClick={() => emit('remove-empty-rooms')}
            >Clear rooms</button>
		</div>
	);
};

export default AddRoom;
