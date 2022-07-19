<script lang="ts">
    import { onDestroy, onMount } from 'svelte';
    import {name, joinedRoom, error, playAudio} from '$lib/stores.js'

    export let socket : WebSocket

    let board : number[][]

    let selectedColumn = -1
    let positions : number[][] = []
    let player : number
    let opponent : string
    let gameOver = false
    let rematching = false
    let nextPlayer = 1
    let moveSound = new Audio('/move.wav')
    let errorSound = new Audio('/error.wav')
    let winSound = new Audio('/win.wav')
    let loseSound = new Audio('/lose.wav')
    let successSound = new Audio('/success.wav')
    let count = 0

    moveSound.volume = 0.5
    errorSound.volume = 0.5
    winSound.volume = 0.5
    loseSound.volume = 0.5
    successSound.volume = 0.5

    function createBoard() {
        board = new Array(7)
        for (let i = 0; i < board.length; i++) {
            board[i] = (new Array(6).fill(0))
        }
    }

    onMount(async() => {
        socket.addEventListener("message", (event) => {
            let received = JSON.parse(event.data)
            if (received.event == "move") {
                board[received.x][received.y] = received.player
                nextPlayer = received.next
                if ($playAudio) {
                    moveSound.play()
                }
                count = 1
            }
            else if (received.event == "error") {
                if ($playAudio) {
                    errorSound.play()
                }
                $error = received.message
                setTimeout(() => {
                    $error = ""
                }, 1000)
            }
            else if (received.event == "end") {
                nextPlayer = received.player
                gameOver = true
            }
            else if (received.event == "disconnected") {
                if ($playAudio) {
                    errorSound.play()
                }
                $error = received.message
                setTimeout(() => {
                    $error = ""
                    leaveRoom()
                }, 2000)
            }
            else if (received.event == "connected") {
                player = received["you"]
                createBoard()
                setTimeout(() => {
                    socket.send(JSON.stringify({
                        "event": "force-start"
                    }))
                }, 2500)
            }
            else if (received.event == "started") {
                if ($playAudio) {
                    successSound.play()
                }
                let otherPlayer = player == 1 ? 2 : 1
                opponent = received[otherPlayer]
                $joinedRoom = true
            }
            else if (received.event == "rematch") {
                if ($playAudio) {
                    successSound.play()
                }
                createBoard()
                gameOver = false
                rematching = false
                nextPlayer = received.player
                count = 1
            }
        } )
        await checkAFK()
    })

    async function checkAFK() {
        count = 0
        setTimeout(() => {
            if (count == 0) leaveRoom()
            else checkAFK()
        }, 45000)
    }

    onDestroy(async() => {
        leaveRoom()
    })

    function handleClick() {
        if (selectedColumn != -1 && socket.readyState == 1) {
            if (nextPlayer != player) {
                if ($playAudio) {
                    errorSound.play()
                }
                $error = "It is not your turn yet"
                setTimeout(() => {
                    $error = ""
                }, 1000)
            }
            else {
                socket.send(JSON.stringify({
                "event": "move",
                "column": selectedColumn
            }))
            }
        }
        selectedColumn = -1
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
            if (nextPlayer == 3) {
                result = "Draw!"
                if ($playAudio) {
                    loseSound.play()
                }
            }
            else if (nextPlayer == player) {
                result = "You won!"
                if ($playAudio) {
                    winSound.play()
                }
            }
            else {
                result = "You lost!"
                if ($playAudio) {
                    loseSound.play()
                }
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
    <div class="flex flex-col items-center justify-center absolute h-screen w-full bg-base-200 top-0 left-0 bg-opacity-50 z-40">
        <div class="card bg-base-100 w-72 opacity-90">
            <div class="card-body items-center text-center">
                <h2 class="card-title">{displayResult()}</h2>
                <p>Request rematch?</p>
                <div class="card-actions justify-center">
                    <button class="btn btn-primary w-30" on:click={voteRematch}>
                        {#if rematching}
                            Waiting...
                        {:else}
                            Yes
                        {/if}
                    </button>
                    <button class="btn btn-ghost w-30" on:click={leaveRoom}>No</button>
                </div>
            </div>
        </div>
    </div>
    {/if}
    <div class="flex flex-col items-center justify-center h-screen w-full" on:mousemove={handleMouseMove} on:click={handleClick}>

        <div class="mb-10 text-2xl mt-5">
            {#if player == nextPlayer}
            Your turn
            {:else}
            Opponent's turn
            {/if}
        </div>
        <div class="relative board grid grid-cols-7 bg-primary py-3">
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
        <div class="w-full mt-6 flex justify-center items-center flex-col">
                <div class="badge badge-primary py-3 px-3">{$name} (you): <span class="font-bold ml-1" class:red-text={player == 1} class:yellow-text={player != 1}>{player == 1 ? 'red' : 'yellow'}</span></div>
                vs
                <div class="badge badge-primary py-3 px-3">{opponent} (opponent): <span class="font-bold ml-1" class:red-text={player != 1} class:yellow-text={player == 1}>{player == 1 ? 'yellow' : 'red'}</span></div>
        </div>
    </div>
{/if}

<style>

    .red {
        background-color: red;
    }

    .yellow {
        background-color: yellow;
    }

    .red-text {
        color: red;
    }

    .yellow-text {
        color: yellow;
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