// Button within a canvas, because it's inside a canvas we can't use the usual <button>/<input type='button'>
import { useState, useRef, useEffect } from 'react';
import { Rect, Text } from "react-konva"


const FONT_SIZE = 16;


interface CanvasButtonProps {
    text: string;
    x: number;
    y: number;
    width: number;
    height: number;
    onClick: () => void;
    invertedColors?: boolean;
}


export const CanvasButton = ({text, x, y, width, height, onClick, invertedColors=false}: CanvasButtonProps) => {
    const buttonRef = useRef(null);
    const [isHovering, setIsHovering] = useState(false);

    useEffect(() => {
        if (buttonRef.current !== null) {
            buttonRef.current.on('mouseenter', () => {
                setIsHovering(true);
            })
            buttonRef.current.on('mouseleave', () => {
                setIsHovering(false);
            })
            buttonRef.current.on('click', () => {
                onClick();
            })
        }
    }, [buttonRef, setIsHovering, onClick]);

    return <>
        <Rect
            x={x}
            y={y}
            width={width}
            height={height}
            fill={invertedColors ? 'white': 'black'}
            stroke={isHovering ? 'yellow' : 'black'}
            strokeWidth={5}
            cornerRadius={5}
            opacity={0.9}
        />
        <Text
            x={x + 12}
            y={y + (height / 2) - (FONT_SIZE / 2)}
            text={text}
            fontSize={FONT_SIZE}
            fill={invertedColors ? 'black' : 'white'}
        />
        {/* Invisible rectangle to catch events, if we try to do it on the other rectangle it won't register mouse events over the text element as it's drawn on top */}
        <Rect
            ref={buttonRef}
            x={x}
            y={y}
            width={width}
            height={height}
            opacity={0}
        />
    </>
}
