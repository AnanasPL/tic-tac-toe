import React, { useEffect, useContext, useMemo } from "react"

import { useParams } from "react-router-dom"

import useGameProgress from "../../hooks/useGameProgress";
import usePlayerState from "../../hooks/usePlayerState";
import useBoardState from "../../hooks/useBoardState";

import { socketContext } from "../../contexts/socketContext"
import { messageContext } from "../../contexts/messageContext";

import Cell from "./Cell"
import WinnerInfo from "./WinnerInfo";

const Board = () => {
    const { emit } = useContext(socketContext)
    const setMessage = useContext(messageContext)

    const { playerSymbol, setCurrentPlayer } = usePlayerState()
    const boardState = useBoardState(playerSymbol, setCurrentPlayer);

    const { gameStarted, winner, playAgainState } = useGameProgress()
    const { roomCode } = useParams()

    const handleClick = useMemo(() => (id) => {
        if (!gameStarted()) {
            setMessage('Oczekiwanie na drugiego gracza')
            return
        }
        
        emit('board-update', {changedCell: {index: id, symbol: playerSymbol.current}})
    }, [gameStarted, setMessage, emit, playerSymbol])
    //TODO: consider cell state management, consider further decentralization
    
    useEffect(() => {
        emit('join-room', {code: roomCode})

        return () => {
            emit('leave-room', {code: roomCode})
        }
    }, [])
    
    const getWinnerInfo = () => {
        if (!winner) return

        if (winner === playerSymbol.current) {
            return (
                <div>
                    <p>Wygrywasz!</p>
                    <p style={{fontSize: 60}}>{playerSymbol.current}</p>
                </div>
            )
        } else if (winner === 'tie') {
            return (
                <div>
                    <p>Remis!</p>
                    <p style={{fontSize: 60}}>{playerSymbol.current}</p>
                </div>
            )
        } else {
            return (
                <div>
                    <p>Przegrywasz!</p>
                    <p style={{fontSize: 60}}>{playerSymbol.current === 'X' ? 'X' : 'O'}</p>
                </div>
            )
        }
    } 

    return (
        <div className="board">
            {boardState.map((val, id) => <Cell value={val} onClick={() => handleClick(id)} key={id}/>)}
            {winner && <button onClick={() => emit('game-restart')}>RESTART</button>}
            {winner && (
                <WinnerInfo hide={() => {emit('restart-request')}}>
                    <div>
                        {getWinnerInfo()}
                        <div className="players-play-again-status-wrapper">
                            <div className="player-status-wrapper">
                                <div className="player-symbol">
                                    O
                                </div>
                                <div className="play-again-status">
                                    {playAgainState.O}
                                </div>
                            </div>
                            <div className="player-status-wrapper">
                                <div className="play-again-status">
                                    {playAgainState.X}
                                </div>
                                <div className="player-symbol">
                                    X
                                </div>
                            </div>
                        </div>
                    </div>
                </WinnerInfo>
            )}
        </div>
    )
}

export default Board