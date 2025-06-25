import { create } from "zustand";
import { IGrid } from "./interfaces/grid";


interface GameStoreData {
    grid: IGrid | null;
    score: number;
    level: number;
    game_state: 'IN_PROGRESS' | 'PAUSED' | 'ENDED';
    is_high_score: boolean;
}

interface IGameStore extends GameStoreData {
    update: (data: GameStoreData) => void;
}


export const useGameStore = create<IGameStore>((set) => ({
    grid: null,
    score: 0,
    level: 1,
    game_state: 'PAUSED',
    is_high_score: false,
    update: (data) => set(data)
}))
