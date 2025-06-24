import { useEffect, useRef, useState } from "react";
import { Layer, Rect, Text } from "react-konva";
import { GRID_HEIGHT, GRID_WIDTH } from "../config";


const SIZE_X = 250;
const SIZE_Y = 125;
const FONT_SIZE = 20;


interface AnnouncementProps {
    message: string;
    setMessage: (string) => null;
}


export const Announcement = ({message, setMessage}: AnnouncementProps) => {
    const textRef = useRef(null);
    const [settings, setSettings] = useState({
        'isVisible': false,
        'textX': 0
    });
    useEffect(() => {
        if (message !== '') {
            setTimeout(() => {
                setMessage('');
                setSettings({
                    'isVisible': false,
                    'textX': 0
                });
            }, 2000);
        }
    }, [message, setMessage, setSettings]);
    useEffect(() => {
        if (textRef.current && message !== '') {
            const textX = (SIZE_X / 2) - (textRef.current.getWidth() / 2);
            setSettings({
                'isVisible': true,
                'textX': textX
            })
        }
    }, [textRef, message, setSettings]);

    return <Layer 
        x={(GRID_WIDTH / 2) - (SIZE_X / 2)} 
        y={(GRID_HEIGHT / 2) - (SIZE_Y / 2)}
        visible={settings.isVisible}
    >
        <Rect
            width={SIZE_X}
            height={SIZE_Y}
            fill="white"
            strokeWidth={0}
            cornerRadius={5}
            opacity={0.9}
        />
        <Text
            x={settings.textX}
            y={(SIZE_Y / 2) - (FONT_SIZE / 2)}
            fontSize={FONT_SIZE}
            text={message}
            ref={textRef}
        />
    </Layer>
    // return message ? <Konva.Text align="center" verticalAlign="middle">{message}</Konva.Text> : <></>
}

// Support series of messages? 