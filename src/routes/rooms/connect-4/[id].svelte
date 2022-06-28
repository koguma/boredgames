<script>
    import { page } from '$app/stores'

    let grid = []
    let ROWS = 6
    let COLUMNS = 7
    for (let i = 0; i < ROWS; i++) {
        let row = []
        for (let j=0; j < COLUMNS; j++) {
            row.push(0)
        }
        grid.push(row)
    }

    let path = $page.params.id
</script>

<div class="game flex items-center justify-center w-screen h-screen">
    <div class="board">
        {#each grid as row}
            <div class="grid grid-cols-7">
                {#each row as square}
                    <div class="square border w-20 h-20">{square}</div>
                {/each}
            </div>
        {/each}
    </div>
</div>