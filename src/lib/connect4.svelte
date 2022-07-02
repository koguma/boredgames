<script lang="ts">
    import { onMount } from 'svelte';
    import {name, joinedRoom} from '$lib/stores.js'

    export let socket : WebSocket

    let board : number[][] = []
    let ROWS = 6
    let COLUMNS = 7
    
    for (let i = 0; i < COLUMNS; i++) {
        let row = []
        for (let j=0; j < ROWS; j++) {
            row.push(0)
        }
        board.push(row)
    }

    let selected_column = -1
    let positions : number[][] = []
    let player : number
    let opponent : string

    onMount(async() => {
        socket.addEventListener("message", (event) => {
            let received = JSON.parse(event.data)
            if (received.event == "move") {
                board[received.x][received.y] = received.player
            }
            else if (received.event == "error") {
                console.log(received.message)
            }
            else if (received.event == "end") {
                console.log(received.message)
                socket.close(1000, "game over")
            }
            else if (received.event == "connected") {
                player = received["you"]
                console.log(received["you"])
            }
            else if (received.event == "started") {
                opponent = received["opponent"]
                $joinedRoom = true
                // socket.send(JSON.stringify({
                //     "event": "ok"
                // }))
            }
        } )
    })

    function handleClick() {
        if (selected_column != -1 && socket.readyState == 1) {
            socket.send(JSON.stringify({
                "event": "move",
                "column": selected_column
            }))
        }
    }

    function handleMouseMove(event : MouseEvent) {
        if (positions.length == 0) updateCollection()
        let mouse_x = event.clientX
        for (let i = 0; i < positions.length; i++) {
            if (mouse_x > positions[i][0] && mouse_x <= positions[i][1]) {
                selected_column = i
                return
            }
        }
        selected_column = -1
    }

    function updateCollection() {
        if ($joinedRoom) {
            positions = []
            Array.from(document.getElementsByClassName("columnIdentifier")).forEach((elem) => {
                positions.push([elem.getBoundingClientRect().x,elem.getBoundingClientRect().x+ elem.getBoundingClientRect().width])
            })   
        }
    }
</script>

<svelte:window on:resize={updateCollection}/>

{#if $joinedRoom}
    <div class="game flex items-center justify-center w-screen h-screen" on:mousemove={handleMouseMove} on:click={handleClick}>
        <span class="test">{opponent}</span>
        <div class="relative board grid grid-cols-7 bg-primary bg-primary py-3">
            {#each board as column, i}
                <div class="grid grid-rows-6">
                    {#each column as square, j}
                        <div class="square w-10 h-10 sm:h-12 sm:w-12 md:h-20 md:w-20 relative" class:columnIdentifier={j == 0} class:columnIdentifierSelected={j == 0 && i == selected_column} class:redBefore={player == 1} class:yellowBefore={player == 2}>
                            <div class="rounded-full bg-primary-content circle" class:red={square == 1} class:yellow={square == 2}></div>
                        </div>
                    {/each}
                </div>
            {/each}
        </div>
    </div>
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