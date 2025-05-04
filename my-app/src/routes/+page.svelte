<script>
    import Meta from "../components/Meta.svelte";
    import Index from "../components/Index.svelte";
	export const prerender = true;

    	const preloadFont = [
		// "https://pudding.cool/assets/fonts/tiempos/TiemposTextWeb-Regular.woff2",
		// "https://pudding.cool/assets/fonts/tiempos/TiemposTextWeb-Bold.woff2",
		// "https://pudding.cool/assets/fonts/national/National2Web-Regular.woff2",
		// "https://pudding.cool/assets/fonts/national/National2Web-Bold.woff2"
	];
</script>

<Meta {preloadFont} />
<Index />


