<script>
	import { dndzone } from "svelte-dnd-action";
	import { flip } from "svelte/animate";
	import { onMount, onDestroy } from "svelte";
	import Tile from "./Tile.svelte";
	import Slot from "./Slot.svelte";
	import { error } from "@sveltejs/kit";
	import { Tween } from "svelte/motion";
	import { fade } from "svelte/transition";
	import { cubicInOut, cubicOut } from "svelte/easing";
	import { SHADOW_ITEM_MARKER_PROPERTY_NAME } from 'svelte-dnd-action';

	export let itemsStart = [];
	export let gameNumber = 0;
	export let items1 = []; //items for the rack

	let ready = false;

	let darkGray = "#1c1c1c";
	let midGray = "#8e8d8c";
	let lightGray = "#e6e6e6";
	let errorRed = "#880000";
	

	const gameContainerHeight = new Tween(500, {
		duration: 500,
		easing: cubicInOut,
	});
	const gameContainerWidth = new Tween(500, {
		duration: 500,
		easing: cubicInOut,
	});

	let windowWidth = 0;

	function setGameDimensions(width) {
		console.log(width);
		if (width >= 1200) {
			// large screens
			gameContainerHeight.target = 500;
			gameContainerWidth.target = 700;
		} else if (width >= 900) {
			// medium screens
			gameContainerHeight.target = 500;
			gameContainerWidth.target = 550;
		} else if (width >= 480) {
			// small screens
			gameContainerHeight.target = 500;
			gameContainerWidth.target = 450;
		} else {
			// mobile screens
			gameContainerHeight.target = 500;
			gameContainerWidth.target = 350;
		}
	}

	function handleResize() {
		windowWidth = window.innerWidth;
		setGameDimensions(windowWidth);
	}

	let isUnderlined = false;
	let hintButtonOpacity = 0;

	let correct_class = "";
	let slotOpacity = 1;

	let isRunning = false;
	let animateHint = false;
	let closeHint = false;
	let transitioningGames = false;

	function typeWriter(textID, newText, speed = 100) {
		let element = document.getElementById(textID);
		let typeDelay = 0;
		if (textID === "hint" && transitioningGames === false) {
			setTimeout(() => {
				animateHint = true;
			}, 10);
			typeDelay = 1000;
		}

		setTimeout(() => {
			return new Promise((resolve) => {
				let currentText = element.innerHTML;
				let i = currentText.length;
				let j = 0;

				function deleteText() {
					if (i > 0) {
						element.innerHTML = currentText.substring(0, i - 1);
						i--;
						setTimeout(deleteText, speed);
					} else {
						typeText();
					}
				}

				function typeText() {
					if (j < newText.length) {
						element.innerHTML += newText.charAt(j);
						j++;
						setTimeout(typeText, speed);
					} else {
						isRunning = false;
						resolve(); // done!
					}
				}

				deleteText();
			});
		}, typeDelay);
	}
	let hintCount = 0;
	let hintsLeft = 3;
	export let glowCart = false;

	//check to give a hint
	function checkConditions() {
		if (gameNumber == 0) {
			// first game
			if (areArraysEqual(items1, itemsStart)) {
				setTimeout(() => {
					correct_class = "correct";
					slotOpacity = 0;
				}, 700);
				setTimeout(() => {
					items1 = [];
					gameNumber = 1;
					slotOpacity = 1;
					correct_class = "";
					setTimeout(() => {
						hintButtonOpacity = 1;
					}, 10000);
				}, 3000);
			}
		} else if (gameNumber == 1) {
			//second game

			if (areArraysEqual(items1, itemsStart)) {
				setTimeout(() => {
					isUnderlined = true;
				}, 1000);
			} else if (areArraysEqual(items1, sortArrayByWord(itemsStart))) {
				// win
				setTimeout(() => {
					correct_class = "correct";
					slotOpacity = 0;
					isUnderlined = false;
					hintButtonOpacity = 0;
					transitioningGames = true;
					typeWriter("hint", "", 50);
					setTimeout(() => {
						if (animateHint === true) {
							closeHint = true;
						}
						animateHint = false;
					}, 3000);
					transitioningGames = false;
				}, 700);
				setTimeout(() => {
					items1 = [];
					gameNumber = 2;
					slotOpacity = 1;
					correct_class = "";
					hintsLeft = 4;
					setTimeout(() => {
						hintButtonOpacity = 1;
					}, 10000);
				}, 3000);
			}
		} else if (gameNumber == 2) {
			// third game
			if (items1.length == itemsStart.length) {
				setTimeout(() => {
					isUnderlined = true;
				}, 1000);
			}
		}
	}

	async function hintButton() {
		if (hintButtonOpacity > 0) {
			if (isRunning) return; // prevent overlapping calls
			isRunning = true;
			if (gameNumber == 1) {
				if (hintCount == 0) {
					typeWriter("hint", "HAVE YOU TRIED DIFFERENT ORDERS?");
					hintsLeft = 1;
					hintCount++;
				} else if (hintCount == 1) {
					typeWriter(
						"hint",
						"TRY A DIFFERENT ORDER, LIKE WORD LENGTH OR ALPHABETICAL...",
					);
					hintsLeft = 0;
					hintCount = 0;
				}
			} else if (gameNumber == 2) {
				if (hintCount == 0) {
					typeWriter("hint2", "YOUR ORDER");
					hintsLeft = 3;
					hintCount++;
				} else if (hintCount == 1) {
					typeWriter("hint", "WHAT ELSE CAN ORDER MEAN?");
					hintsLeft = 2;
					hintCount++;
				} else if (hintCount == 2) {
					typeWriter(
						"hint",
						"HAVE YOU TRIED LOOKING AROUND THE PAGE?",
					);
					hintsLeft = 1;
					hintCount++;
				} else if (hintCount == 3) {
					typeWriter("hint", "REALLY LOOK!");
					glowCart = true;
					hintsLeft = 0;
					hintCount = 1;
				}
			}
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

	function sortArrayByWord(arr) {
		return [...arr].sort((a, b) => a.word.localeCompare(b.word));
	}

	function handleDnd(e) {
		items1 = e.detail.items;
	}

	const flipDurationMs = 100;
	let screenWidth = 0;

	onMount(() => {
		screenWidth = window.innerWidth;

		if (typeof window !== "undefined") {
			handleResize();
			window.addEventListener("resize", handleResize);
			ready = true;
		}
		setTimeout(() => {
			typeWriter("instructions", "PLACE THESE WORDS IN ");
			setTimeout(() => {
				typeWriter("hint2", "ORDER");
			}, 2000);
			setTimeout(() => {
				typeWriter("instructions2", ".");
			}, 2500);
		}, 500);

		window.addEventListener("mouseup", checkConditions);
		window.addEventListener("touchend", checkConditions);


		return () => {
			window.removeEventListener("mouseup", checkConditions);
			window.removeEventListener("touchend", checkConditions);
		};
	});
	
</script>

{#if ready}
	<div
		class="game-container"
		style="--dark-gray: {darkGray}; --mid-gray: {midGray}; --light-gray: {lightGray}; --error-red: {errorRed};"
	>
		<div class="instructions-container">
			<div></div>
			<div>
				<div id="instructions"></div>
				<div
					class="underline-animation"
					class:underlined={isUnderlined}
				>
					<div id="hint2" style="display:inline"></div>
				</div>
				<div id="instructions2"></div>
			</div>

			<div class="tooltip-container" style="opacity: {hintButtonOpacity}">
				<div
					class="hint-button"
					on:click={hintButton}
					style={hintButtonOpacity ? "cursor: pointer;" : ""}
				>
					<span>(?)</span>
					<span>{hintsLeft}</span>
				</div>
				<span class="tooltip-text"
					>Use a hint! I won't judge you...</span
				>
			</div>
		</div>
		<div
			id="hint"
			class:animate-hint={animateHint}
			class:animate-hint-out={closeHint}
		></div>

		<div class="grid">
			{#each itemsStart as square, i}
				<div
					class="slot-container"
					style="
			opacity: {slotOpacity};
			position: absolute;
			left: {(gameContainerWidth.target * square.x) / 100}px;
			top: {(gameContainerHeight.target * square.y) / 100}px;
		  "
				>
					<Slot disableDrag={true} items={[square]} index={i} bounceOut={square.bounceOut} />
				</div>
			{/each}
		</div>

		<div
			class="rack"
			use:dndzone={{
				items: items1,
				flipDurationMs,
				morphDisabled: true,
				dropTargetStyle: {},
			}}
			on:consider={handleDnd}
			on:finalize={handleDnd}
		>
		{#each items1 as item, i (item.id)}
		<div class="tile-container" animate:flip={{ duration: flipDurationMs }}>
		  <div style="z-index: 1; position: relative; opacity: {item[SHADOW_ITEM_MARKER_PROPERTY_NAME] ? 0 : 1};">
			<Tile correct={correct_class} word={item.word} bounceOut={item.bounceOut} />
		  </div>
		</div>
	  {/each}
	  
		</div>
		<div class="level-complete"></div>
	</div>
{/if}

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

	.hint-button {
		color: var(--dark-gray);
		border-radius: 100px;
		padding-right: 0.5em;
		padding-left: 0.5em;
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
		align-self: right;
		transition: opacity 1s ease-in-out; /* Animation duration and effect */
	}

	.hint-button > * {
		padding: 0.15em;
	}

	#hint2 {
		font-family: "ROMMONO";
		font-weight: 400;
		color: var(--dark-gray);
		display: inline;
		font-size: 10px;
		letter-spacing: 1px;
	}

	.game-container {
		margin: auto;

		display: flex;

		flex-direction: column;
		flex-wrap: wrap;
		justify-content: flex-start;
		align-items: center;

		background-color: var(--mid-gray);
		z-index: -2;
		padding: 3em;
		border-radius: 0.75em;
		pointer-events: auto;
	}
	@media (min-width: 1200px) {
		.game-container {
			height: 500px;
			width: 700px;
		}
	}
	@media (max-width: 1200px) {
		.game-container {
			height: 500px;
			width: 550px;
		}
	}
	@media (max-width: 900px) {
		.game-container {
			height: 500px;
			width: 450px;
		}
	}
	@media (max-width: 480px) {
		.game-container {
			height: 500px;
			width: 350px;
			padding: 2em;
		}
	}

	.my-element {
		-webkit-animation: fadein 1s; /* Safari, Chrome and Opera > 12.1 */
		-moz-animation: fadein 1s; /* Firefox < 16 */
		-ms-animation: fadein 1s; /* Internet Explorer */
		-o-animation: fadein 1s; /* Opera < 12.1 */
		animation: fadein 1s;

		transition: opacity 1s ease-in-out; /* Animation duration and effect */
	}

	@keyframes fadein {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}

	.instructions-container {
		width: 100%;
		display: grid;
		grid-template-columns: 1fr auto 1fr;
		align-items: center;
		position: relative;
	}

	#instructions {
		justify-self: center;
		font-weight: 400;
		color: var(--dark-gray);
		display: inline;
	}

	#instructions2 {
		justify-self: center;
		font-weight: 400;
		color: var(--dark-gray);
		display: inline;
	}

	#hint {
		background-color: var(--error-red);
		width: 100%;
		text-align: center;
		align-self: center;
		align-items: center;
		margin-left: auto;
		height: 1.5em;
		line-height: 1.5em;
		margin-bottom: 14em;
		font-weight: bold;
		color: var(--light-gray);
		transform: scaleX(0%);

		transition: opacity 3s ease-in-out; /* Animation duration and effect */
	}

	@keyframes slideIn {
		from {
			transform: scaleX(0%);
		}
		to {
			transform: scaleX(100%);
		}
	}

	#hint.animate-hint {
		animation: slideIn 0.5s ease-out forwards;
	}

	@keyframes slideOut {
		from {
			transform: scaleX(100%);
		}
		to {
			transform: scaleX(0%);
		}
	}

	#hint.animate-hint-out {
		animation: slideOut 0.5s ease-out forwards;
	}

	.grid {
		align-self: flex-start;
		position: absolute;
		transition: opacity 1s ease-in-out; /* Animation duration and effect */
	}

	.slot-container {
		transition: opacity 1s ease-in-out; /* Animation duration and effect */
	}

	.rack {
		height: 45px;
		display: flex;
		justify-content: center;
		width: 400px;
		border-bottom: solid;
		border-color: var(--light-gray);
		border-width: 0.5px;
	}
	@media (max-width: 900px) {
		.rack {
			width: 275px;
		}
	}
	@media (max-width: 480px) {
		.rack {
			width: 250px;
		}
	}

	.rack > * {
		margin: 6px;
	}
	@media (max-width: 480px) {
		.rack > * {
		margin: 3px;
	}
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

	/* Style for the text with an animated underline */
	.underline-animation {
		/* color: var(--error-red); */
		position: relative;
		display: inline-block;
		transition: color 1s ease-in-out; /* Animation duration and effect */
	}

	.underline-animation::after {
		content: "";
		position: absolute;
		bottom: 0;
		left: 0;
		width: 0;
		height: 2px; /* Thickness of the underline */
		background-color: var(--error-red); /* Underline color */
		transition: width 1s ease-in-out; /* Animation duration and effect */
	}

	/* The animated state */
	.underline-animation.underlined::after {
		width: 100%;
	}
	.tooltip-container {
		justify-self: end;
		position: relative;
		display: inline-block;
		transition: opacity 1s ease-in-out; /* Animation duration and effect */
	}

	.tooltip-text {
		visibility: hidden;
		opacity: 0;
		background-color: var(--dark-gray);
		color: var(--light-gray);
		text-align: center;
		border-radius: 6px;
		padding: 4px 8px;
		position: absolute;
		z-index: 1000;
		top: 120%;
		left: 50%;
		transform: translateX(-50%);
		transition: opacity 0.2s ease-in-out;
		pointer-events: none;
		white-space: nowrap;
		font-size: 0.75em;
		max-width: calc(100vw - 20px);
		box-sizing: border-box;
	}
	@media (max-width: 480px) {
		.tooltip-text  {
			display: none;
		}
	}

	.tooltip-container:hover .tooltip-text {
		visibility: visible;
		opacity: 1;
	}
</style>
