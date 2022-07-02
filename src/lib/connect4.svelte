<script lang="ts">
    import { onMount } from 'svelte';
    import {name, joinedRoom} from '$lib/stores.js'

    export let socket : WebSocket

    let board : number[][]

    let selectedColumn = -1
    let positions : number[][] = []
    let player : number
    let opponent : string
    let gameOver = false
    let winner: number
    let rematching = false

    function createBoard() {
        board = new Array(7).fill(new Array(6).fill(0))
    }

    onMount(async() => {
        createBoard()
        socket.addEventListener("message", (event) => {
            let received = JSON.parse(event.data)
            if (received.event == "move") {
                board[received.x][received.y] = received.player
            }
            else if (received.event == "error") {
                console.log(received.message)
            }
            else if (received.event == "end") {
                gameOver = true
                winner = received.winner
            }
            else if (received.event == "disconnected") {
                console.log(received.event.message)
                leaveRoom()
            }
            else if (received.event == "connected") {
                player = received["you"]
                console.log(received["you"])
            }
            else if (received.event == "started") {
                opponent = received["opponent"]
                $joinedRoom = true
            }
            else if (received.event == "rematch") {
                createBoard()
                gameOver = false
                rematching = false
            }
        } )
    })

    function handleClick() {
        if (selectedColumn != -1 && socket.readyState == 1) {
            socket.send(JSON.stringify({
                "event": "move",
                "column": selectedColumn
            }))
        }
    }

    function handleMouseMove(event : MouseEvent) {
        if (positions.length == 0) updateCollection()
        let mouse_x = event.clientX
        for (let i = 0; i < positions.length; i++) {
            if (mouse_x > positions[i][0] && mouse_x <= positions[i][1]) {
                selectedColumn = i
                return
            }
        }
        selectedColumn = -1
    }

    function updateCollection() {
        if ($joinedRoom) {
            positions = []
            Array.from(document.getElementsByClassName("columnIdentifier")).forEach((elem) => {
                positions.push([elem.getBoundingClientRect().x,elem.getBoundingClientRect().x+ elem.getBoundingClientRect().width])
            })   
        }
    }

    function displayResult() {
        let result = ""
        if (gameOver) {
            if (winner == 3) {
                result = "Draw!"
            }
            else if (winner == player) {
                result = `You won!`
            }
            else {
                result = `You lost!`
            }
        }
        return result
    }

    function leaveRoom() {
        socket.close(1000)
    }

    function voteRematch() {
        socket.send(JSON.stringify({
            "event": "rematch",
        }))
        rematching = true
    }
</script>

<svelte:window on:resize={updateCollection}/>

{#if $joinedRoom}
    {#if gameOver}
    <div class="card bg-neutral text-neutral-content">
        <div class="card-body items-center text-center">
            <h2 class="card-title">{displayResult}</h2>
            <p>Request rematch?</p>
            <div class="card-actions justify-end">
                <button class="btn btn-primary w-1/5" on:click={voteRematch}>
                    {#if rematching}
                        Waiting...
                    {:else}
                        Yes
                    {/if}
                </button>
                <button class="btn btn-ghost w-1/5" on:click={leaveRoom}>No</button>
            </div>
        </div>
    </div>
    {:else}
    <div class="game flex items-center justify-center h-screen" on:mousemove={handleMouseMove} on:click={handleClick}>
        <span class="test">{opponent}</span>
        <div class="relative board grid grid-cols-7 bg-primary bg-primary py-3">
            {#each board as column, i}
                <div class="grid grid-rows-6">
                    {#each column as square, j}
                        <div class="square w-10 h-10 sm:h-12 sm:w-12 md:h-20 md:w-20 relative" class:columnIdentifier={j == 0} class:columnIdentifierSelected={j == 0 && i == selectedColumn} class:redBefore={player == 1} class:yellowBefore={player == 2}>
                            <div class="rounded-full bg-primary-content circle" class:red={square == 1} class:yellow={square == 2}></div>
                        </div>
                    {/each}
                </div>
            {/each}
        </div>
    </div>
    {/if}
{/if}

<style>
    .test {
        position: absolute;
        top: 0;
        left: 0;
    }

    .red {
        background-color: red;
    }

    .yellow {
        background-color: yellow;
    }

    .redBefore.columnIdentifierSelected::before {
        border-top: 0.5rem solid red !important;
    }
    .yellowBefore.columnIdentifierSelected::before {
        border-top: 0.5rem solid yellow !important;
    }

    .columnIdentifierSelected::before {
        position: absolute;
        content: "";
        width: 0; 
        height: 0; 
        border-left: 0.5rem solid transparent;
        border-right: 0.5rem solid transparent;
        
        border-top: 0.5rem solid transparent;
        top: -2.25rem;
        left: 40%;
    }

    .circle {
        width: 80%;
        height: 80%;
        margin: 10%;
    }

    .board::before {
        content: '';
        height: 110%;
        width: 20px;
        margin-left: -20px;
        background-color: hsl(var(--p) / var(--tw-bg-opacity));;
        position: absolute;
        top: 0;
        left: 0;
        display: block;
    }
    .board::after {
        content: '';
        height: 110%;
        width: 20px;
        margin-right: -20px;
        background-color: hsl(var(--p) / var(--tw-bg-opacity));;
        position: absolute;
        top: 0;
        right: 0;
        display: block;
    }
</style>