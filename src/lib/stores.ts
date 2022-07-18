import { writable } from "svelte/store"

export const roomId = writable("")

export const name = writable("")

export const gameType = writable("")

export const joinedRoom = writable(false)

export const error = writable("")

export const playAudio = writable(false)