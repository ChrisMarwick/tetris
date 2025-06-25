import { useMemo, useState, useEffect } from "react";
import { Layer, Rect, Text } from 'react-konva';
import { INFO_BAR_HEIGHT, INFO_BAR_WIDTH, INFO_BAR_X } from "../config";
import { useGameStore } from "../store";


const PADDING = 20;
const KEY_BINDING_TEXTS = [
    'Controls',
    'A: Move Left',
    'D: Move Right',
    'S: Drop',
    'Q: Rotate Left',
    'E: Rotate Right',
    'P: Pause Game',
]


export const InfoBar = () => {
    const score = useGameStore(({score}) => score);
    const level = useGameStore(({level}) => level);
    const scoreText = useMemo(() => `Score: ${score}`, [score]);
    const levelText = useMemo(() => `Level: ${level}`, [level]);

    return <Layer>
        <Rect
            x={INFO_BAR_X}
            width={INFO_BAR_WIDTH}
            height={INFO_BAR_HEIGHT}
            fill='black'
        />
        <Rect
            x={INFO_BAR_X + PADDING}
            y={PADDING}
            width={INFO_BAR_WIDTH - (2 * PADDING)}
            height={75}
            fill='lightskyblue'
        />
        <Text
            x={INFO_BAR_X + (2 * PADDING)}
            y={2 * PADDING}
            fontSize={16}
            text={scoreText}
        />
        <Text
            x={INFO_BAR_X + (2 * PADDING)}
            y={(2 * PADDING) + 20}
            fontSize={16}
            text={levelText}
        />
        <Rect
            x={INFO_BAR_X + PADDING}
            y={2 * PADDING + 75}
            width={INFO_BAR_WIDTH - (2 * PADDING)}
            height={300}
            fill='lightskyblue'
        />
        {KEY_BINDING_TEXTS.map((text, i) => <Text
            key={`KeyBinding${i}`}
            x={INFO_BAR_X + (2 * PADDING)}
            y={(3 * PADDING) + 75 + (30 * i)}
            fontSize={16}
            text={text}
        />)}
    </Layer>
}
