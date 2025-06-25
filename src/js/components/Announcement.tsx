import { useEffect, useRef, useState } from "react";
import { Layer, Rect, Text } from "react-konva";
import { GRID_HEIGHT, GRID_WIDTH } from "../config";
import { Overlay, SIZE_X, SIZE_Y } from "./Overlay";


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

    return <Overlay 
        isVisible={settings.isVisible}
    >
        <Text
            x={settings.textX}
            y={(SIZE_Y / 2) - (FONT_SIZE / 2)}
            fontSize={FONT_SIZE}
            text={message}
            ref={textRef}
        />
    </Overlay>
}
