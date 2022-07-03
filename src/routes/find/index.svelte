<svelte:head>
	<title>Public room | boredgames</title>
</svelte:head>

<script lang="ts">
    import {name, joinedRoom, error} from '$lib/stores.js'
    import GameSelection from '$lib/gameSelection.svelte'
    import Connect4 from '$lib/connect4.svelte'
    import Error from '$lib/error.svelte'
    import { onMount } from 'svelte'

    let joining = false
    let cancelRoom = false
    
    let nickname: HTMLElement
    onMount(async() => {
        nickname.focus()
    })

    let socket : WebSocket
    async function joinRoom() {
        if (!joining) {
            if ($name == "") {
                $error = "nickname must be filled"
                setTimeout(() => {
                    $error = ""
                }, 2000)
                return
            }
            joining = true
            socket = new WebSocket(`ws://localhost:8000/ws/connect-4?nickname=${$name}`)
            
            socket.addEventListener("close", () => {
                $joinedRoom = false
                joining = false
            })
        }
        else if (socket.readyState == 1) {
            socket.close(1000,"change of mind")
        }
    }
    
</script>

<div class="home">
    <Error></Error>
    {#if !$joinedRoom}
	<div class="hero min-h-screen bg-base-200 w-screen">
        <div class="indicator">
            <div class="indicator-item indicator-top indicator-start">
                <a href="/">
                    <button class="btn btn-primary">
                        <svg class="h-6 w-6 fill-current md:h-8 md:w-8" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z"></path></svg>
                    </button>
                </a>
            </div> 
            <div class="card shadow-2xl bg-base-100 w-72 md:w-full">
                <div class="card-body">
                    <!-- svelte-ignore a11y-label-has-associated-control -->
                    <label class="label md:hidden">
                        <span class="label-text">Game</span>
                    </label>
                    <div class="grid sm:grid-cols-1 md:grid-cols-2">
                        <GameSelection></GameSelection>
                        <div class="options">
                            <div class="form-control">
                                <label class="label" for="nickname">
                                    <span class="label-text">Nickname</span>
                                </label>
                                <input bind:this={nickname} id="nickname" type="text" placeholder="" bind:value = {$name} class="input input-bordered" required/>
                            </div>
                            <div class="form-control mt-3" on:click={joinRoom} on:mouseover={() => cancelRoom = true} on:mouseleave={() => cancelRoom = joining && false} on:focus={() => cancelRoom = true} on:blur={() => cancelRoom = false}>
                                <button class="btn btn-primary">
                                    {#if joining && cancelRoom}
                                    Cancel
                                    {:else if joining}
                                    Joining...
                                    {:else}
                                    Join
                                    {/if}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {/if}
    {#if joining}
        <Connect4 socket={socket}></Connect4>
    {/if}
</div>