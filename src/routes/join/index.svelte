<svelte:head>
	<title>Join a room | boredgames</title>
</svelte:head>

<div class="home">
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
                                    <input id="nickname" type="text" placeholder="" class="input input-bordered" required/>
                                </div>
                                <div class="form-control">
                                    <label class="label" for="room-id">
                                        <span class="label-text">Room ID</span>
                                    </label>
                                    <input id="room-id" type="text" placeholder="" class="input input-bordered" required/>
                                </div>
                                <div class="form-control mt-6">
                                    <button class="btn btn-primary">Join</button>
                                </div>
                            </div>
                        </div>
                        <a href="/join/browse" class="font-bold underline mt-5">Browse all public rooms</a>
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