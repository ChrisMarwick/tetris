import { useState, useEffect, useCallback } from 'react';
import { Grid } from './Grid';
import { io } from 'socket.io-client'
import throttle from 'lodash.throttle';


const MAX_KEY_INTERVAL = 200;
const keyEventsMap = {
    'q': 'ROTATE_ANTICLOCKWISE',
    'e': 'ROTATE_CLOCKWISE',
    'a': 'MOVE_LEFT',
    'd': 'MOVE_RIGHT',
    's': 'DROP',
    'p': 'TOGGLE_PAUSE'
}

const sendKeyEvent = (socket, action) => {
    console.log(`Send key event ${action}`);
    socket.emit('action', {
        'event': action
    })
}
const throttledSendKeyEvent = throttle(sendKeyEvent, MAX_KEY_INTERVAL, {trailing: false});


export const Game = () => {
    const [gameId, setGameId] = useState(null);
    const [grid, setGrid] = useState(null);
    
    useEffect(() => {
        const socket = io('http://localhost:5000/', {
            transports: ["polling", "websocket"]
            // tryAllTransports: true
        });
        socket.on('connect', () => {
            console.log('Connection made successfully');
            socket.emit('new_game');
        });
        socket.on('new_game', (data) => {
            console.log('New game with id ' + data.game_id);
            setGameId(data.game_id);
        })
        socket.on('redraw', (data) => {
            console.log('Received redraw event');
            setGrid(data.grid);
        })
        addEventListener('keydown', (e) => {
            if (e.key in keyEventsMap) {
                const event = keyEventsMap[e.key];
                throttledSendKeyEvent(socket, event);
            }
        })
    }, [setGameId, setGrid]);
    return grid ? <Grid grid={grid}/> : <></>
}
