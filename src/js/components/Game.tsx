import { useState, useEffect, useCallback } from 'react';
import { Stage } from 'react-konva';
import { Grid } from './Grid';
import { InfoBar } from './InfoBar';
import { Announcement } from './Announcement';
import { io, Socket } from 'socket.io-client';
import throttle from 'lodash.throttle';
import { CANVAS_HEIGHT, CANVAS_WIDTH } from '../config';


const MAX_KEY_INTERVAL = 200;
const keyEventsMap: Record<string, string> = {
    'q': 'ROTATE_ANTICLOCKWISE',
    'e': 'ROTATE_CLOCKWISE',
    'a': 'MOVE_LEFT',
    'd': 'MOVE_RIGHT',
    's': 'DROP',
    'p': 'TOGGLE_PAUSE'
}

const sendKeyEvent = (socket: Socket, action: string) => {
    console.log(`Send key event ${action}`);
    socket.emit('action', {
        'event': action
    })
}
const throttledSendKeyEvent = throttle(sendKeyEvent, MAX_KEY_INTERVAL, {trailing: false});


export const Game = () => {
    const [gameId, setGameId] = useState<string | null>(null);
    const [gameData, setGameData] = useState({
        grid: null,
        score: 0,
        level: 1,
        game_state: null
    });
    const [announcement, setAnnouncement] = useState('');
    
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
        socket.on('event', ({event, data}) => {
            if (['MOVE_LEFT', 'MOVE_RIGHT', 'ROTATE_CLOCKWISE', 'ROTATE_ANTICLOCKWISE', 'DROP', 'GRAVITY_TICK'].includes(event)) {
                setGameData(data);
            } else if (event === 'ROW_CLEARED') {
                console.log(`GOT ROW_CLEARED ${data}`);
            } else if (event === 'SCORE') {
                console.log(`GOT SCORE ${data}`);
                if (data.number_rows === 1) {
                    setAnnouncement('Row cleared!')
                } else {
                    setAnnouncement(`Row cleared x${data.number_rows}!`);
                }
            } else if (event === 'LEVEL_ADVANCE') {
                setAnnouncement(`Level ${data.level}`);
            } else if (event === 'GAME_ENDED') {
                setAnnouncement('Game over!');
            }
        })
        addEventListener('keydown', (e) => {
            if (e.key in keyEventsMap) {
                const event = keyEventsMap[e.key];
                throttledSendKeyEvent(socket, event);
            }
        })
    }, [setGameId, setGameData]);
    return <Stage width={CANVAS_WIDTH} height={CANVAS_HEIGHT}>
        <Grid grid={gameData.grid}/>
        <InfoBar score={gameData.score} level={gameData.level}/>
        <Announcement message={announcement} setMessage={setAnnouncement}/>
    </Stage>
}
