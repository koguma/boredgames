<svelte:head>
	<title>Create a room | boredgames</title>
</svelte:head>

<script lang="ts">
    import {name} from '$lib/stores.js'
    import {goto} from '$app/navigation'

    let roomId = ""
    let error = ""

    async function createRoom() {
        const res = await fetch('http://127.0.0.1:8000/create/', {
            method: 'POST',
            headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: "connect-4",
                room_id: roomId,
                is_private: true
            })
        })
        const content = await res
        const contentJson = await content.json()
        if (res.status == 201) {
            goto(contentJson)
        } else {
            error = contentJson.detail
            setTimeout(() => {
                error = ""
            }, 3500)
        }
    }
</script>

<div class="home">
    {#if error != ""}
    <div class="alert alert-error shadow-lg absolute mt-12 w-1/2 left-1/4">
        <div>
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            <span>Error! {error}</span>
            </div>
        </div>
    {/if}
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
                                            <input type="radio" name="radio-game" class="radio checked:bg-primary mr-3" checked />
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
                                <div class="form-control">
                                    <label class="label" for="nickname">
                                        <span class="label-text">Nickname</span>
                                    </label>
                                    <input id="nickname" type="text" placeholder="" bind:value = {$name} class="input input-bordered" required/>
                                </div>
                                <div class="form-control">
                                    <label class="label" for="room-id">
                                        <span class="label-text">Room ID</span>
                                    </label>
                                    <input id="room-id" bind:value={roomId} type="text" placeholder="" class="input input-bordered" required/>
                                </div>
                                <div class="form-control">
                                    <label class="label cursor-pointer">
                                        <span class="label-text">Private Lobby</span> 
                                        <input type="checkbox" class="toggle" />
                                    </label>
                                  </div>
                                <div class="form-control mt-6" on:click={createRoom}>
                                    <button class="btn btn-primary">Create</button>
                                </div>
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
</style>