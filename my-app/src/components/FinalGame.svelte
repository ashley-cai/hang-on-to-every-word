<script>
	import { onMount, onDestroy } from "svelte";
	import * as d3 from "d3";
	import Matter from "matter-js";
	import { fade } from "svelte/transition";
	import { browser } from "$app/environment";
	import { Tween } from "svelte/motion";
	import { cubicOut } from "svelte/easing";

	let darkGray = "#1c1c1c";
	let midGray = "#8e8d8c";
	let lightGray = "#e6e6e6";
	let errorRed = "#880000";
	let correctGreen = "#E8FFB7";

	export let gameCounter;
	export let transitionHeight;
	export let transitionWidth;
	let windowWidth = 0;

	let wordsRevealIndex = 0;
	const wordsReveal = [
  "Hang__GLOW__", "on__GLOW__", "to__GLOW__", "every__GLOW__", "word.__GLOW__", "It’s", "a", "phrase", "we’ve", "all", "heard", "somewhere—describing", "a", "child", "captivated", "by", "his", "basketball", "idol’s", "TED", "talk,", "or", "in", "a", "housewife’s", "review", "of", "her", "favorite", "true", "crime", "podcast—but", "doubtfully", "ever", "investigated.", "The", "meaning", "of", "the", "phrase", "is", "obvious:", "pay", "attention.", "This", "time,", "let's", "direct", "that", "gaze", "inwards.", "Let’s", "pay", "attention", "to", "the", "saying", "itself.",

  "__BR__First,", "HANG__GLOW__", "ON__GLOW__", "can", "mean", "to", "keep", "a", "jacket", "your", "friend", "left", "on", "your", "couch,", "or", "to", "grab", "tightly", "onto", "your", "mom’s", "hand", "in", "the", "rain.", "It", "can", "mean", "to", "wait", "a", "moment", "while", "your", "date", "pays", "the", "bill,", "to", "grit", "your", "teeth", "as", "your", "dad", "drives", "through", "an", "unpaved", "backroad,", "or", "of", "course,", "to", "pay", "attention.", "The", "phrase", "hangs", "on", "to", "multitudes,", "yet", "somehow,", "we’re", "never", "confused.",

  "__BR__Next,", "the", "word", "EVERY__GLOW__", "comes", "from", "a", "14th", "century", "contraction", "of", "“each”", "(all)", "and", "“ever”", "(always).", "Ever", "each,", "ever-each,", "evereach,", "every.", "The", "first", "attestation", "of", "EVERY__GLOW__", "comes", "from", "The", "Canterbury", "Tales,", "the", "text", "responsible", "for", "popularizing", "English", "in", "mainstream", "literature", "and", "displacing", "French", "and", "Latin.", "Every", "word", "we", "carelessly", "toss", "around", "contains", "a", "rich,", "layered", "history.",

  "__BR__Finally,", "to", "have", "the", "ability", "to", "hang", "onto", "every", "WORD__GLOW__", "is", "to", "materialize", "language", "in", "your", "grasp.", "They", "are", "daggers", "you", "can", "have", "in", "an", "argument,", "snacks", "to", "binge", "eat", "when", "embarrassed,", "a", "fluorescent", "jungle", "gym", "to", "play", "on.", "The", "entirety", "of", "the", "English", "language", "is", "a", "physical", "thing", "we", "can", "grasp.",

  "__BR__We", "don’t", "think", "about", "these", "features", "when", "we", "use", "words.", "We", "just", "know", "where", "they’re", "allowed", "to", "be", "placed,", "so", "we", "awkwardly", "slot", "them", "into", "sentences", "like", "primitive", "pattern", "matching", "machines.", "We", "follow", "rules", "and", "sounds", "that", "we’ve", "internalized,", "but", "don’t", "fully", "understand.", "That", "internalization", "lets", "us", "stop", "paying", "attention.",

  "__BR__But", "if", "we", "know", "we", "exist", "in", "this", "storied", "world,", "if", "we", "are", "aware", "of", "the", "logic", "behind", "each", "phrase’s", "construction,", "if", "we", "peer", "a", "little", "past", "our", "expectations—a", "sudden", "turn", "of", "phrase", "can", "have", "us", "careening", "down", "an", "alleyway", "that", "we’d", "never", "noticed,", "wandering", "along", "the", "street", "paved", "with", "translation,", "stubbornly", "unfamiliar,", "feet", "sliding,", "stumbling,", "slipping", "on", "the", "rain-slicked", "tongue—we", "can", "actually", "begin", "to", "hang", "on.",

  "__BR__I__GLOW__", "hope__GLOW__", "you__GLOW__", "experience__GLOW__", "a__GLOW__", "little__GLOW__", "more__GLOW__", "in__GLOW__", "every__GLOW__", "word__GLOW__", "too.__GLOW__"
];

	const gameContentOpacity = new Tween(0, {
		delay: 1000,
		duration: 1000,
		easing: cubicOut,
	});
	const gameHeight = new Tween(transitionHeight, {
		duration: 500,
		easing: cubicOut,
	});
	const gameWidth = new Tween(transitionWidth, {
		delay: 500,
		duration: 500,
		easing: cubicOut,
	});

	let responsiveFontSize = "10px";
	let responsivePadding = 40;
	let responsiveHeight = 30;
	let responsiveRadius = 17;

	function setGameDimensions(wWidth) {
		if (width >= 1200) {
			// large screens
			gameHeight.target = 500;
			gameWidth.target = 600;
		} else if (wWidth >= 900) {
			// medium screens
			gameHeight.target = 400;
			gameWidth.target = 600;
		} else if (wWidth >= 480) {
			// small screens
			gameHeight.target = 400;
			gameWidth.target = 480;
		} else {
			// mobile screens
			gameHeight.target = 400;
			gameWidth.target = 350;
			responsiveFontSize = "7px";
			responsivePadding = 20;
			responsiveRadius = 11.5;
			responsiveHeight = 20;
		}
	}

	function handleResize() {
		windowWidth = window.innerWidth;
		setGameDimensions(windowWidth);
	}

	$: if (gameCounter == 6) {
		gameContentOpacity.target = 1;
	}

	let container;
	let engine, render, runner;
	let showModal = true;
	let width = 0;
	let height = 0;
	const boxHeight = 30;
	const boxWidth = 30;

	let boxes = [];

	let words = [];
	let data = [];

	let isRunning = false;
	function typeWriter(textID, newText, speed = 100) {
		let element = document.getElementById(textID);
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
	}

	onMount(() => {
		if (typeof window !== "undefined") {
			handleResize(); // set initial size
			window.addEventListener("resize", handleResize);
		}
		setTimeout(() => {
			typeWriter("instructions", "HANG ON...");
		}, 1000);

		if (!browser) return;

		width = window.innerWidth;
		height = window.innerHeight;

		engine = Matter.Engine.create();
		engine.gravity.y = 1;

		render = Matter.Render.create({
			element: container,
			engine,
			options: {
				width,
				height,
				wireframes: false,
				background: "transparent",
				pixelRatio: window.devicePixelRatio || 1,
			},
		});

		// Add walls
		const wallThickness = 200;
		const walls = [
			Matter.Bodies.rectangle(
				width / 2,
				height + wallThickness / 2,
				width,
				wallThickness,
				{ isStatic: true },
			),
			Matter.Bodies.rectangle(
				width / 2,
				-wallThickness / 2,
				width,
				wallThickness,
				{ isStatic: true },
			),
			Matter.Bodies.rectangle(
				-wallThickness / 2,
				height / 2,
				wallThickness,
				height,
				{ isStatic: true },
			),
			Matter.Bodies.rectangle(
				width + wallThickness / 2,
				height / 2,
				wallThickness,
				height,
				{ isStatic: true },
			),
		];
		Matter.World.add(engine.world, walls);

		// Mouse interaction
		const mouse = Matter.Mouse.create(render.canvas);
		const mouseConstraint = Matter.MouseConstraint.create(engine, {
			mouse,
			constraint: {
				stiffness: 0.2,
				render: { visible: false },
			},
		});
		Matter.World.add(engine.world, mouseConstraint);
		render.mouse = mouse;

		Matter.Events.on(mouseConstraint, "mousedown", function (event) {
			const mousePosition = event.mouse.position;
			const clickedBodies = Matter.Query.point(boxes, mousePosition);

			if (clickedBodies.length > 0) {
				const clickedBox = clickedBodies[0];

				// 1. Reveal next word
				revealWord(wordsReveal[wordsRevealIndex]);
				wordsRevealIndex++;

				// 2. Remove from Matter.js world
				Matter.World.remove(engine.world, clickedBox);

				// 3. Remove from boxes array
				boxes = boxes.filter((b) => b !== clickedBox);
			}
		});

		// Draw rounded glowing rectangles with text
		Matter.Events.on(render, "afterRender", () => {
			const ctx = render.context;
			ctx.font = responsiveFontSize + " sans-serif";
			ctx.textAlign = "center";
			ctx.textBaseline = "middle";

			boxes.forEach((box) => {
				ctx.save();
				ctx.translate(box.position.x, box.position.y);
				ctx.rotate(box.angle);

				const radius = responsiveRadius;
				const w = box.boxWidth || boxWidth;
				const h = box.boxHeight || boxHeight;

				// Rounded glowing rectangle
				ctx.beginPath();
				ctx.moveTo(-w / 2 + radius, -h / 2);
				ctx.lineTo(w / 2 - radius, -h / 2);
				ctx.quadraticCurveTo(w / 2, -h / 2, w / 2, -h / 2 + radius);
				ctx.lineTo(w / 2, h / 2 - radius);
				ctx.quadraticCurveTo(w / 2, h / 2, w / 2 - radius, h / 2);
				ctx.lineTo(-w / 2 + radius, h / 2);
				ctx.quadraticCurveTo(-w / 2, h / 2, -w / 2, h / 2 - radius);
				ctx.lineTo(-w / 2, -h / 2 + radius);
				ctx.quadraticCurveTo(-w / 2, -h / 2, -w / 2 + radius, -h / 2);
				ctx.closePath();

				ctx.shadowColor = "#ffffff";
				ctx.shadowBlur = 15;
				ctx.fillStyle = lightGray;
				ctx.fill();

				// Glowing text
				ctx.shadowColor = midGray;
				ctx.shadowBlur = 5;
				ctx.fillStyle = darkGray;
				ctx.fillText(box.label, 0, 0);

				ctx.restore();
			});
		});

		runner = Matter.Runner.create();
		Matter.Runner.run(runner, engine);
		Matter.Render.run(render);

		// get cognate data
		d3.csv("./allwords.csv").then(function (data) {
			words = data.map((d) => d.WORD);
			console.log(data);
		});
	});

	let allWordsSpawned = false;

	function spawnFromCenter() {
		const centerX = width / 2;
		const centerY = height / 4;
		const ctx = render.context;
		ctx.font = responsiveFontSize + " sans-serif";

		let i = 0;
		let delay = 1000;
		const minDelay = 150;
		const decayFactor = 0.95;

		function spawnNext() {
			if (i >= words.length) {
				allWordsSpawned = true;
				return;
			}

			const word = words[i];
			const textWidth = ctx.measureText(word).width;
			const padding = responsivePadding;
			const rectWidth = textWidth + padding;
			const rectHeight = responsiveHeight;

			const x = centerX + (Math.random() - 0.5) * 10;
			const y = centerY + (Math.random() - 0.5) * 10;

			const box = Matter.Bodies.rectangle(x, y, rectWidth, rectHeight, {
				restitution: 0.2,
				friction: 0.5,
				render: {
					fillStyle: "transparent",
					strokeStyle: "transparent",
				},
			});

			box.label = word;
			box.boxWidth = rectWidth;
			box.boxHeight = rectHeight;

			boxes.push(box);
			Matter.World.add(engine.world, box);

			i++;
			delay = Math.max(minDelay, delay * decayFactor); // Speed up
			setTimeout(spawnNext, delay);
		}

		spawnNext();
	}

	function handleModalClick() {
		showModal = false;
		spawnFromCenter();
	}

	onDestroy(() => {
		if (!browser) return;
		if (render?.frameRequestId !== undefined) Matter.Render.stop(render);
		if (runner) Matter.Runner.stop(runner);
		if (engine) {
			Matter.World.clear(engine.world);
			Matter.Engine.clear(engine);
		}
		render?.canvas?.remove();
		if (render?.textures) render.textures = {};
	});

	let revealedWords = [];

	function revealWord(word) {
		revealedWords = [...revealedWords, word];
	}
</script>

<div
	class="page-container"
	style=" --dark-gray: {darkGray}; --mid-gray: {midGray}; --light-gray: {lightGray};"
>
	<p class="background-paragraph">
		{#each revealedWords as word}
			{#if word.includes("__BR__")}
				<br />
				<br />
				{#if word.includes("__GLOW__")}
					<span class="fade-word glow">
						{word.replace("__BR__", "").replace("__GLOW__", "")}
					</span>
				{:else}
					<span class="fade-word">
						{word.replace("__BR__", "")}
					</span>
				{/if}
			{:else if word.includes("__GLOW__")}
				<span class="fade-word glow"
					>{word.replace("__GLOW__", "")}
				</span>
			{:else}
				<span class="fade-word">
					{word}
				</span>
			{/if}
		{/each}
	</p>

	<!-- 🖼 Canvas container where Matter.js appends the canvas -->
	<div bind:this={container} class="scene" />

	<!-- 🧊 Modal overlay -->
	{#if showModal}
		<div
			class="modal"
			style=" width: {gameWidth.current}px; height: {gameHeight.current}px"
			on:click={handleModalClick}
			transition:fade
		>
			<div
				style="opacity: {gameContentOpacity.current}"
				class="loader"
			></div>
			<div
				style="opacity: {gameContentOpacity.current}"
				id="instructions"
			></div>
		</div>
	{/if}
</div>

<style>
	.page-container {
		width: 100vw;
		height: 100dvh;
		position: absolute;
		opacity: 1;
		width: 100vw;
		justify-content: center;
		align-items: center;
		display: flex;
	}

	.scene {
		position: fixed;
		top: 0;
		left: 0;
		width: 100vw;
		height: 100dvh;
		margin: 0;
		border: none;
		overflow: hidden;
		z-index: 0;
	}
	.modal {
		display: flex;
		align-self: center;
		margin: auto;
		position: fixed;
		inset: 0;
		background: var(--mid-gray);
		border-radius: 0.75em;
		z-index: 999;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		color: var(--light-gray);
		font-size: 1.2rem;
		/* cursor: pointer; */
		user-select: none;
	}

	.loader {
		border: 2px solid var(--dark-gray);
		border-top: 3px solid var(--light-gray);
		border-radius: 50%;
		width: 40px;
		height: 40px;
		animation: spin 0.8s linear infinite;
		margin-bottom: 1rem;
		-webkit-filter: drop-shadow(0px 0px 4px var(--light-gray));
	}

	#instructions {
		color: var(--dark-gray);
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	.background-paragraph {
		position: absolute;
		top: 40px;
		width: 480px;
		color: var(--light-gray);
		/* z-index: 1; */
		pointer-events: none;
	}
	@media (max-width: 480px) {
		.background-paragraph {
			width: 350px;
		}
	}

	.glow {
		-webkit-filter: drop-shadow(0px 0px 4px var(--light-gray));
	}

	.fade-word {
		animation: fadeIn 0.6s ease-out;
		display: inline-block;
		margin: 0 0.15em;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(0.5em);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
</style>
