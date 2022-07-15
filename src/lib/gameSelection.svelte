<script lang="ts">
    import {gameType} from '$lib/stores'

    let dropdown : HTMLElement

    function updateGameType(newGameType: string) {
        $gameType = newGameType
        dropdown.blur()
    }

    function getGame(gameType: string) {
        let ret_val = ""
        if (gameType == "connect-4")
            ret_val = "Connect 4"
        else if (gameType == "checkers")
            ret_val = "Checkers"
        else if (gameType == "battleship")
            ret_val = "Battleship"

        return ret_val
    }

</script>

<div class="games">
    <div class="flex flex-col justify-center h-full hidden md:flex">
        <div class="form-control">
            <label class="label cursor-pointer justify-start">
                <input type="radio" name="radio-game" class="radio checked:bg-primary mr-3" bind:group={$gameType} value={"connect-4"} />
                <span class="label-text">Connect 4</span> 
            </label>
        </div>
        <div class="form-control">
            <label class="label cursor-pointer justify-start">
                <input type="radio" name="radio-game" class="radio checked:bg-blue-500 mr-3" bind:group={$gameType} value={"checkers"} />
                <span class="label-text">Checkers</span> 
            </label>
        </div>
        <div class="form-control">
            <label class="label cursor-pointer justify-start">
                <input type="radio" name="radio-game" class="radio checked:bg-blue-500 mr-3" bind:group={$gameType} value={"battleship"} />
                <span class="label-text">Battleship</span> 
            </label>
        </div>
    </div>
    <div class="dropdown block md:hidden">
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label tabindex="0" class="btn btn-outline hover:btn-primary w-full">
            {#if $gameType == ""}
                Select
            {:else}
            <div class="flex content-center items-center">
                
                <svg class="mr-1" xmlns="http://www.w3.org/2000/svg" width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
                {getGame($gameType)}
            </div>
            {/if}
        </label>
        <ul tabindex="0" class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52" bind:this={dropdown}>
            <!-- svelte-ignore a11y-missing-attribute -->
            <li on:click={() => {updateGameType("connect-4")}}><a>Connect 4</a></li>
            <!-- svelte-ignore a11y-missing-attribute -->
            <li on:click={() => {updateGameType("checkers")}}><a>Checkers</a></li>
            <!-- svelte-ignore a11y-missing-attribute -->
            <li on:click={() => {updateGameType("battleship")}}><a>Battleship</a></li>
        </ul>
    </div>
</div>