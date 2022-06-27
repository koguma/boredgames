<svelte:head>
	<title>Home | boredgames</title>
</svelte:head>

<div class="home">
	<div class="hero min-h-screen bg-base-200">
		<div class="hero-content text-center">
			<div class="max-w-md">
				<h1 class="text-5xl font-bold">Bored Games</h1>
				<p class="py-6">Play {game} with friends, bots, or anyone online!</p>
				<button class="btn btn-primary">Create Room</button>
			</div>
		</div>
	</div>
</div>

<style>
	.home {
		margin-bottom: -5rem;
	}
</style>

<script>
import { onMount } from "svelte";

	let games = ["Connect-4", "Chess", "Checkers"]
	let game = ""
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