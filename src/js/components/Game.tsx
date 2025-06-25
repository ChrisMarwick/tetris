import { useState, useEffect, useCallback } from 'react';
import { Stage } from 'react-konva';
import { Grid } from './Grid';
import { InfoBar } from './InfoBar';
import { Announcement } from './Announcement';
import { io, Socket } from 'socket.io-client';
import throttle from 'lodash.throttle';
import { CANVAS_HEIGHT, CANVAS_WIDTH } from '../config';
import { useGameStore } from '../store';
import { Menu } from './Menu';
import { HighScore } from './HighScore';


const MAX_KEY_INTERVAL = 200;
const keyEventsMap: Record<string, string> = {
    'q': 'ROTATE_ANTICLOCKWISE',
    'e': 'ROTATE_CLOCKWISE',
    'a': 'MOVE_LEFT',
    'd': 'MOVE_RIGHT',
    's': 'DROP',
    'p': 'TOGGLE_PAUSE'
}


const startNewGame = (socket: Socket) => {
    socket.emit('new_game');
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
    const updateGameData = useGameStore(({update}) => update);
    const gameState = useGameStore(({game_state}) => game_state);
    const [announcement, setAnnouncement] = useState('');
    const [isHighScoreVisible, setIsHighScoreVisible] = useState(false);
    const [socket, setSocket] = useState(null);
    const [showMenu, setShowMenu] = useState(true);

    const handleClickNewGame = useCallback(() => {
        if (socket) {
            startNewGame(socket);
            setShowMenu(false);
        }
    }, [socket, setShowMenu]);
    const handleClickHighScore = useCallback(() => {
        setIsHighScoreVisible(true);
    }, [setIsHighScoreVisible]);
    
    useEffect(() => {
        const socket = io('http://localhost:5000/', {
            transports: ["polling", "websocket"]
            // tryAllTransports: true
        });
        socket.on('connect', () => {
            setSocket(socket);
            console.log('Connection made successfully');
        });
        socket.on('new_game', (data) => {
            console.log('New game with id ' + data.game_id);
            setGameId(data.game_id);
        })
        socket.on('event', ({event, data}) => {
            if (['MOVE_LEFT', 'MOVE_RIGHT', 'ROTATE_CLOCKWISE', 'ROTATE_ANTICLOCKWISE', 'DROP', 'GRAVITY_TICK', 'TOGGLE_PAUSE'].includes(event)) {
                updateGameData(data);
            } else if (event === 'SCORE') {
                if (data.number_rows === 1) {
                    setAnnouncement('Row cleared!')
                } else {
                    setAnnouncement(`Row cleared x${data.number_rows}!`);
                }
            } else if (event === 'LEVEL_ADVANCE') {
                setAnnouncement(`Level ${data.level}`);
            } else if (event === 'GAME_ENDED') {
                updateGameData(data);
                setAnnouncement('Game over!');
                setTimeout(() => {
                    console.log(gameState);
                    setShowMenu(true);
                }, 2000);
            }
        })
        addEventListener('keydown', (e) => {
            if (e.key in keyEventsMap) {
                const event = keyEventsMap[e.key];
                throttledSendKeyEvent(socket, event);
            }
        })
    }, [setGameId, updateGameData, setSocket]);
    return <Stage 
        width={CANVAS_WIDTH} 
        height={CANVAS_HEIGHT} 
    >
        <Grid opacity={gameState === 'IN_PROGRESS' ? 1 : 0.7}/>
        <InfoBar/>
        <Announcement message={announcement} setMessage={setAnnouncement}/>
        {showMenu && <Menu onClickNewGame={handleClickNewGame} onClickHighScore={handleClickHighScore}/>}
        {isHighScoreVisible && <HighScore onClose={() => {
            setIsHighScoreVisible(false);
        }}/>}
    </Stage>
}
