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

    function handleClick() {
        if (selected != -1) {
            for (let i = grid.length-1; i >= 0; i--) {
                if (grid[selected][i] == 0) {
                    grid[selected][i] = 1
                    return
                }
            }
        }
    }
    
    onMount(async() => {
        updateCollection()
        
        let socket = new WebSocket('ws://localhost:8000/ws/connect-4/'+$page.params.id)
        socket.addEventListener("open", (event) => {
            console.log(event)
        } )
        socket.addEventListener("messages", (event) => {
            console.log(event)
        } )
        socket.addEventListener("close", () => {
            goto("/browse/")
        })
    })

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
                    <div class="square w-20 h-20 relative" class:columnIdentifier={j == 0} class:columnIdentifierSelected={j == 0 && i == selected}>
                        <div class="rounded-full bg-primary-content circle" class:red={square == 1}></div>
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

    .columnIdentifierSelected::before {
        position: absolute;
        content: "";
        width: 0; 
        height: 0; 
        border-left: 0.5rem solid transparent;
        border-right: 0.5rem solid transparent;
        
        border-top: 0.5rem solid #f00;
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