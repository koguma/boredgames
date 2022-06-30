<script lang="ts">
    import { page } from '$app/stores'
    import { onMount } from 'svelte';
    import {goto} from '$app/navigation'


    let grid : number[][] = []
    let ROWS = 6
    let COLUMNS = 7
    
    for (let i = 0; i < COLUMNS; i++) {
        let row = []
        for (let j=0; j < ROWS; j++) {
            row.push(0)
        }
        grid.push(row)
    }

    let selected = -1

    let positions : number[][] = []

    let socket : WebSocket

    let player : number

    let turn = 1

    onMount(async() => {
        updateCollection()
        socket = new WebSocket('ws://localhost:8000/ws/connect-4/'+$page.params.id)
        socket.addEventListener("message", (event) => {
            let recieved = JSON.parse(event.data)
            if ("x" in recieved && "y" in recieved) {
                grid[recieved["x"]][recieved["y"]] = recieved["player"]
                if (recieved["player"] == 1) {
                    turn = 2
                } else {
                    turn = 1
                }
            } else if(!("message" in recieved)) {
                player = recieved["player"]
            } else {
                console.log(recieved["message"])
            }
        } )
        socket.addEventListener("close", () => {
            goto("/create/")
        })
    })

    function handleClick() {
        if (selected != -1) {
            for (let i = grid.length-1; i >= 0; i--) {
                if (grid[selected][i] == 0) {
                    if (socket.readyState <= 1 && turn == player) {
                        socket.send(`${selected},${i}`)
                        return
                    }
                }
            }
        }
    }

    function handleMouseMove(event : MouseEvent) {
        let mouse_x = event.clientX
        for (let i = 0; i < positions.length; i++) {
            if (mouse_x > positions[i][0] && mouse_x <= positions[i][1]) {
                selected = i
                return
            }
        }
        selected = -1
    }

    function updateCollection() {
        positions = []
        Array.from(document.getElementsByClassName("columnIdentifier")).forEach((elem) => {
            positions.push([elem.getBoundingClientRect().x,elem.getBoundingClientRect().x+ elem.getBoundingClientRect().width])
        })
    }
</script>

<svelte:window on:resize={updateCollection}/>

<div class="game flex items-center justify-center w-screen h-screen" on:mousemove={handleMouseMove} on:click={handleClick}>
    <span class="test">{selected}</span>
    <div class="relative board grid grid-cols-7 bg-primary bg-primary py-3">
        {#each grid as column, i}
            <div class="grid grid-rows-6">
                {#each column as square, j}
                    <div class="square w-20 h-20 relative" class:columnIdentifier={j == 0} class:columnIdentifierSelected={j == 0 && i == selected} class:redBefore={player == 1} class:yellowBefore={player == 2}>
                        <div class="rounded-full bg-primary-content circle" class:red={square == 1} class:yellow={square == 2}></div>
                    </div>
                {/each}
            </div>
        {/each}
    </div>
</div>

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