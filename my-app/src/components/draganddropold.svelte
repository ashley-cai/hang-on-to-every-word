<script>
	import { dndzone } from 'svelte-dnd-action';
	import { flip } from 'svelte/animate';
	
	import Tile from './Tile.svelte';
	import Slot from './Slot.svelte';

	let darkGray = '#1c1c1c';
	let midGray = '#8e8d8c';
	let lightGray = '#e6e6e6';


	let cartVisible = "-102vw";
	let cartVisibleMargin = ".5vw"; // margin for the buttons to move over

	let cartVisibleColor = midGray
	let endTransition = 1;

	//toggle cart in and out
	function toggleCart(){
		if (cartVisible == "-92vw") {
			cartVisible = "-102vw";
			cartVisibleColor = midGray
			cartVisibleMargin = ".5vw"
		} else {
			cartVisible = "-92vw";
			cartVisibleColor = darkGray
			cartVisibleMargin = "4vw"
		}
	}

	
	let idx = 0;
	let isUnderlined = false;
	let hint2 = false;


	let correct_class = "";
	
	let itemsStart = [
		{ id: idx++, word: 'HANG', x: 20, y: 10 },
		{ id: idx++, word: 'ON', x: 2, y: 3},
		{ id: idx++, word: 'TO', x: 14, y: 34},
		{ id: idx++, word: 'EVERY', x: 30, y: 20},
		{ id: idx++, word: 'WORD', x: 8, y: 16 }
	];

	let items1 = [] //items for the rack
	let items2 = [] //items for the cart

	//check to give a hint
	$: if (items1) {
    	if (areArraysEqual(items1, itemsStart)) {
			setTimeout(() => {
				isUnderlined = true;
			}, 1000)
			setTimeout(() => {
				hint2 = true;
			}, 1000)
		} 
	}

	//win condition function
	function checkOut() {
		if (items2.length == 5){
			endTransition = 0;
			setTimeout(() => {
				cartVisible = "0"
			}, 500)

		}
	}

	function areArraysEqual(arr1, arr2) {
	// First check if lengths are different
	if (arr1.length !== arr2.length) {
		return false;
	}

	// Compare each element in the arrays
	for (let i = 0; i < arr1.length; i++) {
		if (arr1[i].word !== arr2[i].word) {
		return false; // Return false if any element is different
		}
	}

	// If we get here, the arrays are equal
	return true;
	}

			
	function handleDnd(e) {
		items1 = e.detail.items;
	}

	function handleDndCart(e) {
		items2 = e.detail.items;
	}
	
	const flipDurationMs = 100;
	
</script>

<div class="page-container" style="--dark-gray: {darkGray}; --mid-gray: {midGray}; --light-gray: {lightGray}">
	<div class="cart" style="right: {cartVisible}">
		<div class="cart-separator" style="opacity: {endTransition}"></div>
		<div class="cart-dropbox" style="opacity: {endTransition}" use:dndzone={{items: items2, flipDurationMs, morphDisabled: true, dropTargetStyle: {}}} on:consider={handleDndCart} on:finalize={handleDndCart}>
			{#each items2 as tile(tile.id)}
			<Tile word={tile.word} />
			{/each}
		</div>
	</div>
	<div class="page-contents" style="opacity: {endTransition}">
	<div class=header-container>
		<div class="logo">*</div>
		<div class="buttons" style="margin-right:{cartVisibleMargin}">
			<div>MORE GAMES</div>
			<div>ABOUT</div>
			<div on:click={toggleCart} >
				<svg 
				class="cart-button" style="stroke:{cartVisibleColor}"
				viewBox="0 0 512 450" fill="none" xmlns="http://www.w3.org/2000/svg">
					<path d="M15 15.5H102L116.263 77M164.5 285L116.263 77M116.263 77H492.5L437.5 285H165C147 285 133 298 133 317C133 336 151 345 167 345C183 345 349.333 345 437.5 345"  stroke-width="30" stroke-linecap="round"/>
					<circle cx="194.5" cy="406.5" r="28.5" stroke-width="30"/>
					<circle cx="405.5" cy="406.5" r="28.5" stroke-width="30"/>
				</svg>
					
			</div>
		</div>
	</div>
	<div class="game-container">
		<div class="instructions">Place these words in <div class="underline-animation" class:underlined={isUnderlined}>order</div>.</div>
		<div class="grid">
			{#each itemsStart as square, i}
				<div  class="my-element">
					<Slot x={square.x} y={square.y} disableDrag = {true} items = {[square]}/>
				</div>
			{/each}
		</div>
		
		<div class="rack" use:dndzone={{items: items1, flipDurationMs, morphDisabled: true, dropTargetStyle: {}}} on:consider={handleDnd} on:finalize={handleDnd}>
			{#each items1 as item(item.id)}
			<div class="tile-container" animate:flip={{ duration: flipDurationMs }}>
				<div style="z-index: 1; position: relative; {correct_class}">
					<Tile word={item.word} />
				</div>
			</div>
			{/each}
		</div>
		<div class="level-complete"></div>

	</div>
	<div class="footer">
		<div class="separator"></div>
		<div class="footer-text">
			<div>© 2025 HANGONTOEVERYWORD.com LLC. All Rights Reserved.</div>
			<div class="checkout" style="color:{cartVisibleColor}" on:click={checkOut}>CHECK OUT</div>
		</div>
	</div>
</div>
</div>

<style>
	:global(body *) {
		box-sizing: border-box;
		margin: 0;
		padding: 0;
	}

	:global(body) {
		box-sizing: border-box;
		margin: 0;
		padding: 0;
	}

	.page-container {
		position: relative;
		height: 100dvh;
		overflow:hidden;
		pointer-events: none;
	}

	.page-contents {
		padding: 8px;
		transition: opacity 1s ease-in-out;
	}

	.game-container {
		margin: auto; 
		margin-top: 14vh;
		margin-bottom: 14vh;


		display: flex;
		height: 64vh;
		width: 45vw;

		flex-direction: column;
		flex-wrap: wrap;
		justify-content:flex-start;
		align-items: center;
		
		background-color: var(--mid-gray);
		z-index: -2;
		padding: 4em;
		border-radius: .75em;
		pointer-events: auto;
	}

	.instructions{
		padding-bottom: 16vh;
		font-weight: 600;
		color: var(--light-gray);
	}
	
	.grid {
		align-self: flex-start;
		position: absolute;
	}
	
	.rack {
		height: 55px;
		display: flex;
		justify-content: center;
		width: calc((min(5vmin, 50px) + 4px) * 8);
		border-bottom: solid;
		border-color: var(--light-gray);
		border-width: .5px;
	}
	.rack > * {
		margin: 6px;
	}

	.tile-container {
		position: relative;
	}

	.tile-container:active {
        outline: none;
      }

	.tile-container:focus {
        outline: none;
	}


	.text-shadow {
		position: absolute;
		margin: auto;
		/*
			move the (positioned) element up and left 
			by half its own width/height
		*/
		transform: skewX(20deg) translateY(70%);
		color: transparent;
		text-shadow: 0 0 2.5px rgba(0,0,0,0.4);
		opacity: 0;
		transition: opacity 1.5s ease-in-out;
		z-index: 0;
		/* font-size: .9em; */
	}

	.footer {
		margin:auto;
		width: 98vw;
		z-index: 2;
		position:relative;
	}
	.separator {
		height: .5px;
		background-color:var(--mid-gray);
	}
	.footer-text{
		padding-top: .3em;
		color: var(--mid-gray);
		font-size: .8em;
		display: flex;
		flex-direction: row;
		justify-content: space-between;
	}
	.cart-separator{
		height: .5px;
		background-color:var(--light-gray);
		transition: opacity 1.5s ease-in-out;
	}
	.checkout {
		color: var(--mid-gray);
		transition: color 2s ease-in-out;
		pointer-events: auto;
	}
	.header-container{
		padding-top: .3em;
		color: var(--mid-gray);
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		pointer-events: auto;
		z-index: 2;
		position:relative;
	}
	.logo{
		font-size: 3em;
		transform: translateY(.2em);
		line-height: .3em;
		margin-left: .5vw;
	}
	.buttons{
		display: flex;
		flex-direction: row;
		gap: 4em;
		margin-right: .5vw;
		transition: margin-right 1.5s ease-in-out;
		cursor: pointer;
	}
	.cart-button {
		stroke: var(--mid-gray);
		height: 2.5vh;
		transition: stroke 1.5s ease-in-out;
	}

	.cart {
		height: 100vh;
		width: 100vw;
		padding-top: 3em;
		padding-left: 1em;
		background-color: var(--mid-gray); 
		border-radius: .75em;
		position: absolute;
		right: -22vw;
		transition: right 1.5s ease-in-out;
		z-index: 0;
		pointer-events: none;
	}
	.cart-dropbox {
		padding-top: 1em;
		pointer-events: auto;
		height: 95vh;
		display: flex;
		flex-direction: column;
		gap: 1em;
		transition: opacity 1.5s ease-in-out;
	}

	/* Style for the text with an animated underline */
	.underline-animation {
		position: relative;
		display: inline-block;
		font-weight: bold;
	}

	.underline-animation::after {
		content: '';
		position: absolute;
		bottom: 0;
		left: 0;
		width: 0;
		height: 2px; /* Thickness of the underline */
		background-color: #DB0000; /* Underline color */
		transition: width 1s ease-in-out; /* Animation duration and effect */
	}

	/* The animated state */
	.underline-animation.underlined::after {
    width: 100%;
  }
</style>