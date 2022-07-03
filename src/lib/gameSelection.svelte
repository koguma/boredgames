<div class="games">
    <div class="flex flex-col justify-center h-full hidden md:flex">
        <div class="form-control">
            <label class="label cursor-pointer justify-start">
                <input type="radio" name="radio-game" class="radio checked:bg-primary mr-3" checked />
                <span class="label-text">Connect-4</span> 
            </label>
        </div>
        <div class="form-control">
            <label class="label cursor-pointer justify-start">
                <input type="radio" name="radio-game" class="radio checked:bg-primary mr-3" />
                <span class="label-text">Tic-Tac-Toe</span> 
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
    <div class="dropdown block md:hidden">
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label tabindex="0" class="btn btn-outline hover:btn-primary w-full">Select</label>
        <ul tabindex="0" class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52">
            <!-- svelte-ignore a11y-missing-attribute -->
            <li><a>Connect-4</a></li>
            <!-- svelte-ignore a11y-missing-attribute -->
            <li><a>Tic-Tac-Toe</a></li>
            <!-- svelte-ignore a11y-missing-attribute -->
            <li><a>Chess</a></li>
            <!-- svelte-ignore a11y-missing-attribute -->
            <li><a>Checkers</a></li>
        </ul>
    </div>
</div>