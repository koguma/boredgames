<svelte:head>
	<title>Home | boredgames - play board games online </title>
</svelte:head>

<script lang="ts">
	import { onMount } from "svelte";

	let totalPlayers : number

	onMount(async() => {
		let result = await fetch("http://localhost:8000/statistics")
		let content = await result.json()
		if (result.status == 200) {
			let stats = JSON.parse(content)
			totalPlayers = stats.total
		}
	})
</script>

<div class="home">
	<div class="hero min-h-screen bg-base-200 w-screen">
		<div class="hero-content text-center">
			<div class="max-w-md">
				<h1 class="text-5xl font-bold">Bored Games</h1>
				<div class="flex items-center flex-wrap justify-center py-3">
					<span class="hidden md:inline">Play</span>
					<div class="wrapper h-4 overflow-hidden">
						<span class="flex flex-col px-1 change">
							<span class="text-secondary font-bold ">Connect 4</span>
							<span class="text-secondary font-bold ">Checkers</span>
							<span class="text-secondary font-bold ">Battleship</span>
						</span>
					</div>
					with friends or anyone online!
				</div>
				<a href="/private">
					<button class="btn btn-primary w-3/4 sm:w-2/5">Play vs friends</button>
				</a>
				<span class="mx-5 my-4 block sm:my-0 sm:inline">or</span>
				<a href="/public">
					<button class="btn btn-primary w-3/4 sm:w-2/5">Find opponent</button>
				</a>
				<div class="flex w-full justify-center items-center mt-5">
					<span class="badge badge-secondary block py-3 px-3 flex justify-center items-center">
						Online: 
						{#if totalPlayers == undefined}
							...
						{:else}
							{totalPlayers} players
						{/if}
					</span> 
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	.change {
		animation: slider 3s ease-out -3s infinite alternate forwards;
		margin-top: -0.25rem;
	}

    @keyframes slider {
        0% {
			transform: translateY(0rem);
		}
		20% {
			transform: translateY(0rem);
		}
    	40% {
			transform: translateY(-1.5rem);
		}
		60% {
			transform: translateY(-1.5rem);
		}
		80% {
			transform: translateY(-3rem);
		}
		100% {
			transform: translateY(-3rem);
		}
    }
</style>