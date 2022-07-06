<script lang="ts">
	import '../app.css'
	import {joinedRoom} from '$lib/stores'
	import { onMount } from 'svelte';
	
	let now = new Date().getFullYear()
	let dark : boolean
	let darkFirst : boolean

	onMount(async() => {
		switchMode()
		darkFirst = dark
	})

	function switchMode() {
		if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
			document.getElementById("svelte-body")!.setAttribute("data-theme", "dark")
			dark = true
		} else {
			document.getElementById("svelte-body")!.setAttribute("data-theme", "light")
			dark = false
		}
	}

	function specifyMode() {
		if (dark) {
			localStorage.theme = 'light'
		} else {
			localStorage.theme = 'dark'
		}
		switchMode()
	}
</script>

<div class="navbar bg-base-100 absolute top-0">
	<div class="navbar-start">
	  	<div class="dropdown">
			<!-- svelte-ignore a11y-label-has-associated-control -->
			<label tabindex="0" class="btn btn-ghost btn-circle">
				<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7" /></svg>
			</label>
			<ul tabindex="0" class="menu menu-compact dropdown-content mt-3 p-2 shadow bg-base-100 rounded-box w-52">
				<li><a href="/">Home</a></li>
				<li><a href="/private">Play vs Friends</a></li>
				<li><a href="/public">Find Opponent</a></li>
			</ul>
	  	</div>
	</div>
	<div class="navbar-center">
		<a href="/" class="btn normal-case text-lg md:text-xl" class:btn-ghost={!$joinedRoom} class:btn-warning={$joinedRoom}>
			{#if $joinedRoom}
			Leave
			{:else}
			<img class="h-6 w-6 mr-1" src="./table-games.png" alt="logo"/> Bored Games
			{/if}
		</a>
	</div>
	<div class="navbar-end">
		<label class="btn btn-ghost btn-circle swap swap-rotate">
  
			<!-- this hidden checkbox controls the state -->
			<input type="checkbox" on:click={specifyMode}/>
			
			<!-- sun icon -->
			<svg class:swap-on={darkFirst} class:swap-off={!darkFirst} class="fill-current w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z"/></svg>
			
			<!-- moon icon -->
			<svg class:swap-on={!darkFirst} class:swap-off={darkFirst} class="fill-current w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z"/></svg>
			
		</label>
	</div>
  </div>

<main>
	<slot />
</main>

<footer class="footer px-10 py-3 md:py-6 border-t bg-base-200 text-base-content border-base-300 footer-center absolute bottom-0">
	<div class="flex">
	  	<p>&copy; {now} Bored Games by <a class="link link-hover" href="https://github.com/koguma" target="_blank">Koguma</a>. Open-source on </p>
	  	<a class="icon" href="https://github.com/koguma/boredgames" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg></a>
	</div>
	<a class="text-xxs" href="https://www.flaticon.com/free-icons/board-game" title="board game icons">Board game icons created by Freepik - Flaticon</a>
</footer>

<style>
	.text-xxs {
		font-size: 0.7rem;
		margin-top: -2rem;
	}
	.icon:hover {
		animation: bounce 0.8s ease-in-out;
	}

    @keyframes bounce {
        0% { 
			transform: scale(1,1) translateY(0);
		}
        20% {
			transform: scale(1.1,.9) translateY(0);
		}
        60% {
			transform: scale(.9,1.1) translateY(-1rem);
		}
        100% {
			transform: scale(1,1) translateY(0);
		}
    }
</style>
