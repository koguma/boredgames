<svelte:head>
	<title>Public room | boredgames</title>
</svelte:head>

<script lang="ts">
    import {name, joinedRoom} from '$lib/stores.js'
    import GameSelection from '$lib/gameSelection.svelte'
    import Connect4 from '$lib/connect4.svelte'
    import Error from '$lib/error.svelte'
    import { onMount } from 'svelte'

    let error = ""
    let joining = false
    
    let nickname: HTMLElement
    onMount(async() => {
        nickname.focus()
    })

    let socket : WebSocket
    async function findRoom() {
        if ($name == "") {
            error = "nickname must be filled"
            setTimeout(() => {
                error = ""
            }, 3000)
            return
        }
        joining = true
        socket = new WebSocket(`ws://localhost:8000/ws/connect-4?nickname=${$name}`)
        
        socket.addEventListener("close", () => {
            $joinedRoom = false
            joining = false
        })
    }
    
</script>

<div class="home">
    {#if !$joinedRoom}
    <Error error={error}></Error>
	<div class="hero min-h-screen bg-base-200">
		<div class="hero-content text-center">
            <div class="indicator">
                <div class="indicator-item indicator-top indicator-start">
                    <a href="/">
                        <button class="btn btn-primary">
                            <svg class="h-6 w-6 fill-current md:h-8 md:w-8" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z"></path></svg>
                        </button>
                    </a>
                </div> 
                <div class="card w-full max-w-md shadow-2xl bg-base-100">
                    <div class="card-body w-full">
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
                                <div class="form-control mt-6" on:click={findRoom}>
                                    <button class="btn btn-primary">{#if joining}Joining...{:else}Join{/if}</button>
                                </div>
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