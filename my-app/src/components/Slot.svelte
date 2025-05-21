<script>
	import { dndzone, SHADOW_ITEM_MARKER_PROPERTY_NAME } from 'svelte-dnd-action';
	
	import Tile from './Tile.svelte';
	export let items = [];
	export let disableDrag = false;
	export let x = 0;
	export let y = 0;
	export let slot;
	export let index =0;
	export let bounceOut;

	function handleDnd(e) {
		items = e.detail.items;
	}
	
	$: options = {
		dropFromOthersDisabled: items.length,
		items,
		dropTargetStyle: {},
		flipDurationMs: 100,
		dropFromOthersDisabled: disableDrag,
	};

</script>

<!-- style="{items.find(tile => tile[SHADOW_ITEM_MARKER_PROPERTY_NAME]) ? 'background: rgba(255, 255, 255, 0.2)': ''}" -->
<div bind:this={slot} class="square" style="transform:translate({x}vw,{y}vh)"	use:dndzone={options} on:consider={handleDnd} on:finalize={handleDnd}>
	{#each items as tile (tile.id)}
	<Tile
	  word={tile.word}
	  index={index}
	  hidden={tile[SHADOW_ITEM_MARKER_PROPERTY_NAME]}
	  bind:shouldBounce={tile.shouldBounce}
	  bounceOut = {bounceOut}
	/>
  {/each}
  <!-- {#each items as tile (tile.id)}
  {#if !tile[SHADOW_ITEM_MARKER_PROPERTY_NAME]}
	<Tile
	  word={tile.word}
	  index={index}
	  bind:shouldBounce={tile.shouldBounce}
	  bounceOut={bounceOut}
	/>
  {/if}
{/each} -->
</div>

<style>
  .square {
    height: calc(2px + min(5vmin, 50px));
    width: 100px;
    border-radius: calc(min(5vmin, 50px) / 6.25);
	transition: opacity 1s ease-in-out; /* Animation duration and effect */
    /* background-color: #b6b6b6; */
	}
</style>

