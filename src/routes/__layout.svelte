<script lang="ts">
	import '../app.css';
	let now = new Date().getFullYear()
</script>

<main>
	<slot />
</main>

<footer class="footer px-10 py-6 border-t bg-base-200 text-base-content border-base-300 footer-center absolute bottom-0">
	<div class="flex">
	  <p>&copy; {now} boredgames by <a class="link link-hover" href="https://github.com/koguma" target="_blank">Koguma</a>. Open-source on </p>
	  <a class="icon" href="https://github.com/koguma/boredgames" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg></a>
	</div>
</footer>

<style>
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
