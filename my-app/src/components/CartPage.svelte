<script>
	import DragAndDrop from "./DragAndDrop.svelte";
	import { dndzone } from "svelte-dnd-action";
	import Tile from "./Tile.svelte";

	import { Tween } from "svelte/motion";
	import { cubicOut } from "svelte/easing";
	import { onMount } from "svelte";
	import { getContext } from "svelte";


	let gameStart = "";
	export let transitionHeight;
	export let transitionWidth;

	const cartHeight = new Tween(0, { duration: 500, easing: cubicOut });
	const cartWidth = new Tween(0, { duration: 500, easing: cubicOut });
	const cartOpacity = new Tween(1, { duration: 1000, easing: cubicOut });

	let darkGray = "#1c1c1c";
	let midGray = "#8e8d8c";
	let lightGray = "#e6e6e6";

	export let gameCounter = 0; // overall games
	let gameNumber = 2; // within this game

	let screenWidth = 0;

	onMount(() => {
		screenWidth = window.innerWidth;
		const handleResize = () => {
		const width = window.innerWidth;
		const height = window.innerHeight;
		cartWidth.target = width;
		cartHeight.target = height;
	};

	handleResize(); // run once on mount
	window.addEventListener("resize", handleResize);
	});

	let cartVisible = "-102vw";
	$: cartPixelOffset = cartVisible === "-92vw"
	? screenWidth * 0.060 //cart open
	: screenWidth * 0.005; //cart closed
	$: cartVisibleMargin = `${cartPixelOffset}px`;
	let cartCenter = "";

	let cartVisibleColor = midGray;
	let endTransition = .5;
	let winConditionFade = 1;
	let itemsExitingRack = [];

	let items1 = [];
	
	$: isMobile = screenWidth < 480;
	let isCartOpen = false;

	//toggle cart in and out
	function toggleCart() {
	if (gameNumber == 2) {
		const openCartOffset = isMobile ? "-50vw" : "-92vw";
		const closedCartOffset = "-102vw";

		if (cartVisible === openCartOffset) {
			cartVisible = closedCartOffset;
			cartVisibleColor = midGray;
		} else {
			cartVisible = openCartOffset;
			cartVisibleColor = darkGray;
			isCartOpen = true;

			// Step 1: Mark rack and grid items to bounce out
			items1 = items1.map(item => ({ ...item, bounceOut: true }));
			itemsStart[gameNumber] = itemsStart[gameNumber].map(item => ({ ...item, bounceOut: true }));

			// Step 2: Wait for bounce-out, then move to cart
			setTimeout(() => {
				// Move all into cart with bounceIn
				const seen = new Set();
				itemsCart = [...items1, ...itemsStart[gameNumber]].filter(item => {
					if (seen.has(item.word)) return false;
					seen.add(item.word);
					return true;
				}).map(item => ({ ...item, bounceOut: false, shouldBounce: true }));

				// Clear rack and grid
				items1 = [];
				itemsStart[gameNumber] = [];
			}, 600);
		}
	}
}




	//index of word tiles
	let idx = 0;

	let itemsStart = [
		[
			{ id: idx++, word: "HANG", x: 60, y: 20 },
			{ id: idx++, word: "ON", x: 10, y: 15 },
			{ id: idx++, word: "TO", x: 66, y: 60 },
			{ id: idx++, word: "EVERY", x: 40, y: 70 },
			{ id: idx++, word: "WORD", x: 24, y: 54 },
		],
		[
			{ id: idx++, word: "KEEP", x: 10, y: 67 },
			{ id: idx++, word: "AN", x: 65, y: 27 },
			{ id: idx++, word: "EYE", x: 34, y: 56 },
			{ id: idx++, word: "OUT", x: 24, y: 15 },
		],
		[
			{ id: idx++, word: "CART", x: 45, y: 17 },
			{ id: idx++, word: "BEFORE", x: 7, y: 24 },
			{ id: idx++, word: "THE", x: 14, y: 63 },
			{ id: idx++, word: "HORSE", x: 65, y: 47 },
		],
	];

	let itemsCart = []; //items for the cart
	let checkoutGlow = false;
	$: glowCart = false;
	$: checkoutGlow = itemsCart.length === 4;
	//win condition function
	function checkOut() {
		if (itemsCart.length == 4) {
			endTransition = 1;
			setTimeout(() => {
				winConditionFade = 0;
			}, 500);
			setTimeout(() => {
				cartVisible = "0";
			}, 1000);
			setTimeout(() => {
				cartCenter = "top: 0; left: 0; bottom: 0; right: 0;";
				gameStart = "display: none;";
				transitionHeight = cartHeight.target
				transitionWidth = cartWidth.target
				gameCounter = 1;
			}, 2000);
		}
	}

	function handleDndCart(e) {
		itemsCart = e.detail.items;
	}

	const flipDurationMs = 100;

	let showMoreGamesModal = false;
	let showAboutModal = false;

	function toggleMoreGamesModal() {
		showMoreGamesModal = !showMoreGamesModal;
	}

	function toggleAboutModal() {
		showAboutModal = !showAboutModal;
	}

	function closeModals() {
		showMoreGamesModal = false;
		showAboutModal = false;
	}
</script>

<div
	class="page-container-1"
	style="{gameStart} --dark-gray: {darkGray}; --mid-gray: {midGray}; --light-gray: {lightGray}"
>
	<div
		class="cart"
		style="right: {cartVisible}; opacity:{cartOpacity.current}; height: {cartHeight.current +
			'px'}; width: {cartWidth.current + 'px'}; {cartCenter}"
	>
		<div class="cart-separator" style="opacity: {winConditionFade}"></div>
		<div
			class="cart-dropbox"
			style="opacity: {winConditionFade}"
			use:dndzone={{
				items: itemsCart,
				flipDurationMs,
				morphDisabled: true,
				dropTargetStyle: {},
			}}
			on:consider={handleDndCart}
			on:finalize={handleDndCart}
		>
			{#each itemsCart as tile (tile.id)}
			<Tile word={tile.word} shouldBounce={tile.shouldBounce} />
			{/each}
		</div>
	</div>
	{#if isCartOpen}
		<div class="overlay" style="opacity: {endTransition}"></div>
	{/if}
	<div class="page-contents">
		<div class="header-container" style="opacity: {winConditionFade}">
			<div class="logo">*</div>
			<div class="buttons" style="margin-right:{cartVisibleMargin}">
				<div on:click={toggleMoreGamesModal}>MORE GAMES</div>
				<div on:click={toggleAboutModal}>ABOUT</div>
				<div class="tooltip-container">
					<div on:click={toggleCart}>
						<svg 
							class="cart-button {glowCart ? 'glow' : ''}" 
							style="stroke:{glowCart ? lightGray : cartVisibleColor}"
							viewBox="0 0 512 450" 
							fill="none" 
							xmlns="http://www.w3.org/2000/svg">
							<path d="M15 15.5H102L116.263 77M164.5 285L116.263 77M116.263 77H492.5L437.5 285H165C147 285 133 298 133 317C133 336 151 345 167 345C183 345 349.333 345 437.5 345"  stroke-width="30" stroke-linecap="round"/>
							<circle cx="194.5" cy="406.5" r="28.5" stroke-width="30"/>
							<circle cx="405.5" cy="406.5" r="28.5" stroke-width="30"/>
						</svg>
					</div>
					<span class="tooltip-text" style="opacity: {gameNumber === 2 ? "0": "1"}">Shhh... try again later</span>
				</div>
				
			</div>
		</div>

		<div class="main-content">
			<DragAndDrop bind:glowCart itemsStart={itemsStart[gameNumber]} bind:gameNumber bind:items1 />
		</div>

		<div class="footer" style="opacity: {winConditionFade}">
			<div class="separator"></div>
			<div class="footer-text">
				<div>
					© 2025 HANGONTOEVERYWORD.com.
				</div>
				<div
				class="checkout {checkoutGlow ? 'glow' : ''}"
				style="color:{cartVisibleColor}"
				on:click={checkOut}
			>
				CHECK OUT
			</div>			
			</div>
		</div>
	</div>

	{#if showMoreGamesModal}
	<div class="modal-backdrop" on:click={closeModals}>
		<div class="modal-content" on:click|stopPropagation>
			<div>Why don't you finish this game before trying out some others?</div>
		</div>
	</div>
{/if}

{#if showAboutModal}
	<div class="modal-backdrop" on:click={closeModals}>
		<div class="modal-content" on:click|stopPropagation>
			<div>This is a game by Ashley Cai, Brown|RISD 2025.</div>
		</div>
	</div>
{/if}

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

	.page-container-1 {
		position: absolute;
		inset: 0;
		display: flex;
		flex-direction: column;
		height: 100vh;
		overflow: hidden;
		pointer-events: none;
	}
	@media (max-width: 900px) {
    .page-container-1 {
      font-size: smaller;
    }
  }
  @media (max-width: 480px) {
    .page-container-1 {
      font-size: small;
		padding-left: 6px;
		padding-right: 6px;
    }
  }

	.page-contents {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		height: 100%;
		transition: opacity .8s ease-in-out;
	}

	.main-content {
		flex-grow: 1;
		display: flex;
		justify-content: center;
		align-items: center;
	}
	
	.footer {
		margin: auto;
		width: 98vw;
		z-index: 2;
		position: relative;
		margin-bottom: 0.5em;
		transition: opacity .8s ease-in-out;
	}
	@media (max-width: 480px) {
		.footer {
		padding-left: 6px;
		padding-right: 6px;
    }
  }
  .overlay {
	position: fixed;
	top: 0;
	left: 0;
	width: 100vw;
	height: 100dvh;
	background-color: var(--dark-gray);
	opacity: 0.5;
	z-index: -1; /* between .cart (10) and .page-contents (5) */
	pointer-events: none;
	transition: opacity .5s ease-in-out;
}

	.separator {
		height: 0.5px;
		background-color: var(--mid-gray);
	}
	.footer-text {
		padding-top: 0.3em;
		color: var(--mid-gray);
		font-size: 0.8em;
		display: flex;
		flex-direction: row;
		justify-content: space-between;
	}
	.cart-separator {
		height: 0.5px;
		background-color: var(--light-gray);
		transition: opacity .8s ease-in-out;
	}
	.checkout {
		color: var(--mid-gray);
		transition: color .8s ease-in-out;
		pointer-events: auto;
		cursor: pointer;
	}
	@keyframes glowPulse {
	0% {
		-webkit-filter: drop-shadow(0px 0px 4px var(--mid-gray));
	}
	50% {
		-webkit-filter: drop-shadow(0px 0px 4px var(--light-gray));
	}
	100% {
		-webkit-filter: drop-shadow(0px 0px 4px var(--mid-gray));
	}
}

		.glow {
			animation: glowPulse 1s ease-in-out infinite;
		}
		
	.header-container {
		padding-top: .75em;
		color: var(--mid-gray);
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		pointer-events: auto;
		z-index: 2;
		position: relative;
		transition: opacity .8s ease-in-out;
	}
	.logo {
		font-size: 3em;
		transform: translateY(0.2em);
		line-height: 0.3em;
		margin-left: 0.5vw;
	}
	.buttons {
		display: flex;
		flex-direction: row;
		gap: 4em;
		transition: margin-right .8s ease-in-out;
		cursor: pointer;
	}
	.cart-button {
		stroke: var(--mid-gray);
		height: 1.3em;
		transition: stroke .8s ease-in-out;
	}

	.cart {
		padding-top: 3em;
		padding-left: 1em;
		background-color: var(--mid-gray);
		border-radius: 0.75em;
		position: absolute;
		margin: auto;
		right: -22vw;
		transition: right .8s ease-in-out;
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
		transition: opacity .8s ease-in-out;
	}
.modal-backdrop {
	position: fixed;
	top: 0;
	left: 0;
	width: 100vw;
	height: 100dvh;
	background: rgba(0, 0, 0, 0.5);
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 10;
	pointer-events: auto;
	cursor: pointer;
}

.modal-content {
	background: white;
	padding: 2em;
	border-radius: 1em;
	box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
	max-width: 400px;
	text-align: center;
	cursor: auto;
}

.tooltip-container {
	position: relative;
	display: inline-block;
}

.tooltip-text {
	visibility: hidden;
	opacity: 0;
	background-color: black;
	color: white;
	text-align: center;
	border-radius: 6px;
	padding: 4px 8px;
	position: absolute;
	z-index: 1000;
	top: 120%;
	left: 50%;
	transition: opacity 0.2s ease-in-out;
	pointer-events: none;
	white-space: nowrap;
	font-size: 0.75em;
	transform: translateX(-90%);
	max-width: calc(100vw - 20px); /* Prevents it from overflowing screen */
	overflow-wrap: break-word;
	box-sizing: border-box;
}

.tooltip-container:hover .tooltip-text {
	visibility: visible;
	opacity: 1;
}

</style>