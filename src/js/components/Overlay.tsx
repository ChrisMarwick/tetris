import React from 'react';
import { Layer, Rect } from "react-konva";
import { GRID_HEIGHT, GRID_WIDTH } from "../config";


export const SIZE_X = 250;
export const SIZE_Y = 125;


interface OverlayProps {
    isVisible?: boolean;
    children?: React.ReactNode;
}


export const Overlay = ({isVisible = true, children}: OverlayProps) => {
    return <Layer 
        x={(GRID_WIDTH / 2) - (SIZE_X / 2)} 
        y={(GRID_HEIGHT / 2) - (SIZE_Y / 2)}
        visible={isVisible}
    >
        <Rect
            width={SIZE_X}
            height={SIZE_Y}
            fill="white"
            strokeWidth={0}
            cornerRadius={5}
            opacity={0.9}
        />
        {children}
    </Layer>
}
