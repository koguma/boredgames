<svelte:head>
	<title>Home | boredgames</title>
</svelte:head>

<div class="home">
	<div class="hero min-h-screen bg-base-200">
		<div class="hero-content text-center">
			<div class="max-w-md">
				<h1 class="text-5xl font-bold">Bored Games</h1>
				<div class="flex items-center">
					<p class="py-6">Play <span class="text-secondary font-bold">Connect-4</span> with friends, bots, or anyone online!</p>
				</div>
				<a href="/join">
					<button class="btn btn-primary w-80 sm:w-40">Join Room</button>
				</a>
				<span class="mx-5 my-4 block sm:my-0 sm:inline">or</span>
				<a href="/create">
					<button class="btn btn-primary w-80 sm:w-40">Create Room</button>
				</a>
			</div>
		</div>
	</div>
</div>

<style>
</style>

<script>
import { onMount } from "svelte";

	let games = ["Connect-4"]
	// let i = 0
	// let j = 0
	// function updateMessage() {
	// 	setTimeout(() => {
	// 		if (i >= 0 && i < games.length) {
	// 			if (j >= 0 && j < games[i].length) {
	// 				game += games[i][j]
	// 				j++
	// 			} else {
	// 				game = ""
	// 				i++
	// 				j = 0
	// 			}
	// 		}
	// 		else {
	// 			i = 0
	// 		}
	// 		updateMessage()
	// 	}, 200);
	// }

	// onMount(async() => {
	// 	updateMessage()
	// })
</script>