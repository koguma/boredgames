import { writable } from "svelte/store"

export const roomId = writable("")

export const name = writable("")

export const joinedRoom = writable(false)