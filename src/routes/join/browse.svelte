<svelte:head>
	<title>Browse public rooms | boredgames</title>
</svelte:head>

<script lang="ts">
    import {roomId} from '$lib/stores.js'
    
    let newRoomId = $roomId
    
    let rooms = ["room-1", "room5", "jojdlk", "john", "sgvs"]

    if (rooms.length > 0) {
        newRoomId = rooms[0]
    }

    function selectRoom() {
        $roomId = newRoomId
    }

</script>

<div class="home">
	<div class="hero min-h-screen bg-base-200">
		<div class="hero-content text-center">
            <div class="indicator">
                <div class="indicator-item indicator-top indicator-start">
                    <a href="/join">
                        <button class="btn btn-primary">
                            <svg class="h-6 w-6 fill-current md:h-8 md:w-8" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z"></path></svg>
                        </button>
                    </a>
                </div> 
                <div class="card w-full max-w-md shadow-2xl bg-base-100">
                    <div class="card-body">
                        <!-- svelte-ignore a11y-label-has-associated-control -->
                        <label class="label md:hidden">
                            <span class="label-text">Game</span>
                        </label>
                        <div class="grid card-wrapper sm:grid-cols-1 md:grid-cols-2">
                            <div class="games">
                                <div class="flex flex-col justify-center h-full">
                                    <div class="form-control">
                                        <label class="label cursor-pointer justify-start">
                                            <input type="radio" name="radio-game" class="radio checked:bg-primary mr-3" checked/>
                                            <span class="label-text">Connect-4</span> 
                                        </label>
                                    </div>
                                    <div class="form-control">
                                        <label class="label cursor-pointer justify-start">
                                            <input type="radio" name="radio-game" class="radio checked:bg-blue-500 mr-3" disabled/>
                                            <span class="label-text">Chess</span> 
                                        </label>
                                    </div>
                                    <div class="form-control">
                                        <label class="label cursor-pointer justify-start">
                                            <input type="radio" name="radio-game" class="radio checked:bg-blue-500 mr-3" disabled/>
                                            <span class="label-text">Checkers</span> 
                                        </label>
                                    </div>
                                </div>
                            </div>
                            <div class="options">
                                <div class="form-control font-bold mb-2">
                                    <label class="label" for="room-id">
                                        <span class="label-text">Rooms</span>
                                    </label>
                                    <input type="text" placeholder="Search..." class="input input-bordered" />
                                </div>
                                <div class="rooms overflow-y-auto">
                                {#each rooms as room, i}
                                  <div class="form-control mr-1">
                                    <!-- svelte-ignore a11y-label-has-associated-control -->
                                    <label class="label cursor-pointer">
                                        <span class="label-text">{room}</span>
                                        {#if i == 0}
                                            <input bind:group={newRoomId} value={room} type="radio" name="radio-room" class="radio checked:bg-blue-500" checked/>
                                        {:else}
                                            <input bind:group={newRoomId} value={room} type="radio" name="radio-room" class="radio checked:bg-blue-500"/>
                                        {/if}
                                    </label>
                                  </div>
                                  {/each}
                                </div>
                                <a href="/join" on:click={selectRoom}>
                                    <div class="form-control mt-6">
                                        <button class="btn btn-primary">Select</button>
                                    </div>
                                </a>
                                
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
	</div>
</div>

<style>
    .games {
        box-sizing: border-box;
    }
    .card-wrapper {
        grid-auto-rows: 1fr auto;
    }
    .rooms {
        height: 8rem;
    }
    /* width */
    ::-webkit-scrollbar {
    width: 4px;
    }

    /* Track */
    ::-webkit-scrollbar-track {
    background: hsl(var(--bc) / var(--tw-border-opacity));
    }

    /* Handle */
    ::-webkit-scrollbar-thumb {
    background: hsl(var(--bc) / var(--tw-bg-opacity));;
    }

    /* Handle on hover */
    ::-webkit-scrollbar-thumb:hover {
    background: hsl(var(--bc) / var(--tw-bg-opacity));;
    }
</style>