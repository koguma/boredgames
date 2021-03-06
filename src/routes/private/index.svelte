<svelte:head>
	<title>Private room | boredgames</title>
</svelte:head>

<script lang="ts">
    import {roomId, name, joinedRoom, error, gameType} from '$lib/stores'
    import Error from '$lib/error.svelte'
    import GameSelection from '$lib/gameSelection.svelte'
    import Connect4 from '$lib/connect4.svelte'
    import Checkers from '$lib/checkers.svelte'
    import { page } from '$app/stores'
    import { onMount } from 'svelte'

    let joining = false
    let url = ""
    let socket : WebSocket
    let cancelRoom = false

    onMount(async() => {
        $roomId = $page.url.searchParams.get("room_id") || ""
        $gameType = $page.url.searchParams.get("game_type") || ""
    })

    async function joinRoom() {
        if (!joining) {
            if ($roomId == "" || $name == "") {
                $error = "room id and nickname must be filled"
                setTimeout(() => {
                    $error = ""
                }, 2000)
                return
            }
            else if (!$roomId.match(/^[a-z0-9]+$/i)) {
                $error = "room id can only contain alphabets and numbers"
                setTimeout(() => {
                    $error = ""
                }, 2000)
                return
            }
            else if ($gameType == "") {
                $error = "game type must be selected"
                setTimeout(() => {
                    $error = ""
                }, 2000)
                return
            }
            
            joining = true
            url = `${$page.url.href}?room_id=${$roomId}&game_type=${$gameType}`
            
            socket = new WebSocket(`ws://localhost:8000/ws/${$gameType}?nickname=${$name}&room_id=${$roomId}`)
            socket.addEventListener("close", (event) => {
                $joinedRoom = false
                joining = false
                url = ""
                console.log(event)
            })
        } else if (socket.readyState == 1) {
            socket.close(1000,"change of mind")
        }
    }

    function copy() {
        let dummy = document.createElement("textarea");
        document.body.appendChild(dummy)
        dummy.value = url
        dummy.select()
        document.execCommand("copy")
        document.body.removeChild(dummy)
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
                                <input id="nickname" type="text" placeholder="" bind:value = {$name} class="input input-bordered" required/>
                                <label class="label" for="room-id">
                                    <span class="label-text">Room ID</span>
                                </label>
                                <input id="room-id" bind:value={$roomId} type="text" placeholder="" class="input input-bordered" required/>
                                <!-- svelte-ignore a11y-label-has-associated-control -->
                                <span class="my-2 label-text-alt text-left">other players can join using the same room id</span>
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
                    {#if url != ""}
                        <button class="btn btn-outline btn-info mt-5 gap-2" on:click={copy}>
                            <span class="truncate w-3/5">{url}</span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>
                        </button>
                    {/if}
                </div>
            </div>
        </div>
    </div>
    {/if}
    {#if joining && $gameType == "connect-4"}
        <Connect4 socket={socket}></Connect4>
    {:else if joining && $gameType == "checkers"}
        <Checkers socket={socket}></Checkers>
    {/if}
</div>