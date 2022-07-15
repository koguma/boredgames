<script lang="ts">
    import { onDestroy, onMount } from 'svelte';
    import {name, joinedRoom, error} from '$lib/stores.js'
    import {Piece} from '$lib/checkersPiece'

    export let socket : WebSocket

    let board : Piece[][]
    let player : number
    let opponent : string
    let gameOver = false
    let rematching = false
    let nextPlayer = 1
    let selectedPiece : number[] = []
    let destination : number[] = []
    let waiting : boolean


    function createBoard() {
        board = new Array(8)
        let flag = 1
        let isPlayer1 = player == 1
        for (let i = 0; i < board.length; i++) {
            board[i] = new Array(8)
            for (let j = 0; j < board.length; j++) {
                board[i][j] = new Piece(0)
            }
            if (flag) {
                board[i][6].setOwner(2)
                board[i][0].setOwner(1)
                board[i][2].setOwner(1)
            }
            else {
                board[i][1].setOwner(1)
                board[i][5].setOwner(2)
                board[i][7].setOwner(2)
            }
            if (isPlayer1) {
                board[i].reverse()
            }
            flag ^= 1
        }
        if (isPlayer1) {
            board.reverse()
        }
    }

    onMount(async() => {
        socket.addEventListener("message", (event) => {
            let received = JSON.parse(event.data)
            if (received.event == "move") {
                let previous_position = received.previous_position
                let current_position = received.current_position
                if (player == 1) {
                    previous_position = [Math.abs(received.previous_position[0]-7),Math.abs(received.previous_position[1]-7)]
                    current_position = [Math.abs(received.current_position[0]-7),Math.abs(received.current_position[1]-7)]
                }
                
                board[previous_position[0]][previous_position[1]].setOwner(0)
                board[current_position[0]][current_position[1]].setOwner(received.player)
                

                /*                 board[current_position[0]][current_position[1]] = new Piece(received.player)
                if (board[previous_position[0]][previous_position[1]].isKing()) {
                    board[current_position[0]][current_position[1]].setKing(true)
                }
                board[current_position[0]][current_position[1]] = new Piece(received.player)*/
                
                if (received["eaten"]) {
                    let eaten = received.eaten
                    
                    if (player == 1) {
                        eaten = [Math.abs(received.eaten[0]-7),Math.abs(received.eaten[1]-7)]
                    }
                    
                    board[eaten[0]][eaten[1]].setOwner(0)
                }

                if (received["king"] == true && !board[current_position[0]][current_position[1]].isKing()) {
                    board[current_position[0]][current_position[1]].setKing(true)
                }

                board = board
                    
                nextPlayer = received.next
            }

            else if (received.event == "error") {
                $error = received.message
                setTimeout(() => {
                    $error = ""
                }, 2000)
            }
            else if (received.event == "end") {
                nextPlayer = received.player
                gameOver = true
            }
            else if (received.event == "disconnected") {
                $error = received.message
                setTimeout(() => {
                    $error = ""
                    leaveRoom()
                }, 2000)
            }
            else if (received.event == "connected") {
                player = received["you"]
                createBoard()
            }
            else if (received.event == "started") {
                let otherPlayer = player == 1 ? 2 : 1
                opponent = received[otherPlayer]
                $joinedRoom = true
            }
            else if (received.event == "rematch") {
                createBoard()
                gameOver = false
                rematching = false
                nextPlayer = received.player
            }
            if (waiting) {
                selectedPiece = []
                destination = []
                waiting = false
            }
        } )
    })

    onDestroy(async() => {
        leaveRoom()
    })

    function handleClick(x: number, y: number) {
        if (socket.readyState == 1 && !waiting) {
            if (selectedPiece.length != 0) {
                if (board[x][y].getOwner() != 0) {
                    selectedPiece = []
                    return
                }
                destination = [x,y]
                if (player == 1) {
                    socket.send(JSON.stringify({
                        "event": "move",
                        "current_position": [Math.abs(selectedPiece[0]-7),Math.abs(selectedPiece[1]-7)],
                        "next_position": [Math.abs(destination[0]-7),Math.abs(destination[1]-7)]
                    }))
                } else {
                    socket.send(JSON.stringify({
                        "event": "move",
                        "current_position": selectedPiece,
                        "next_position": destination
                    }))
                }
                waiting = true
            } else {
                if (board[x][y].getOwner() != player) return

                selectedPiece = [x,y]
            }
        }
    }

    function displayResult() {
        let result = ""
        if (gameOver) {
            if (nextPlayer == 3) {
                result = "Draw!"
            }
            else if (nextPlayer == player) {
                result = "You won!"
            }
            else {
                console.log(nextPlayer)
                result = "You lost!"
            }
        }
        return result
    }

    function leaveRoom() {
        socket.close()
    }

    function voteRematch() {
        socket.send(JSON.stringify({
            "event": "rematch",
        }))
        rematching = true
    }
</script>

{#if $joinedRoom}
    {#if gameOver}
    <div class="flex flex-col items-center justify-center absolute h-screen w-full bg-base-200 top-0 left-0 bg-opacity-50 z-40">
        <div class="card bg-base-100 w-72">
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
    <div class="flex flex-col items-center justify-center h-screen w-full">

        <div class="mb-5 text-2xl mt-5">
            {#if player == nextPlayer}
            Your turn
            {:else}
            Opponent's turn
            {/if}
        </div>
        <div class="relative board grid grid-cols-8 p-3">
            {#each board as column, i}
                <div class="grid grid-rows-8">
                    {#each column as square, j}
                        <div class="square w-11 h-11 sm:h-14 sm:w-14 md:h-20 md:w-20 flex items-center justify-center" on:click={() => {handleClick(i,j)}} class:square-type-1={(i+j) % 2 == 0} class:square-type-2={(i+j) % 2 == 1} class:is_selected={selectedPiece.length == 2 && i == selectedPiece[0] && j == selectedPiece[1]}>
                            <div class="rounded-full piece circle w-4/5 h-4/5" class:black={square.getOwner() == 1} class:white={square.getOwner() == 2} class:king={square.isKing()}></div>
                        </div>
                    {/each}
                </div>
            {/each}
        </div>
        <div class="w-full mt-6 flex justify-center items-center flex-col">
                <div class="badge badge-warning py-3 px-3">{$name} (you): <span class="font-bold ml-1" class:black-text={player == 1} class:white-text={player == 2}>{player == 1 ? 'black' : 'white'}</span></div>
                vs
                <div class="badge badge-warning py-3 px-3">{opponent} (opponent): <span class="font-bold ml-1" class:black-text={player == 2} class:white-text={player == 1}>{player == 1 ? 'white' : 'black'}</span></div>
        </div>
    </div>
{/if}

<style>

    .is_selected {
        opacity: 0.5;
    }

    .piece {
        background-color: transparent;
    }

    .white {
        background-color: white;
    }

    .black {
        background-color: black;
    }

    .square-type-1 {
        background-color: burlywood;
    }

    .square-type-2 {
        background-color: brown;
    }

    .black-text {
        color: black;
    }

    .white-text {
        color: white;
    }

</style>