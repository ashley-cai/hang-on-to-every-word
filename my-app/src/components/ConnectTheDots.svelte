<script>
  import { onMount, onDestroy } from "svelte";
  import { Tween } from "svelte/motion";
  import { cubicInOut, cubicOut } from "svelte/easing";

  let darkGray = "#1c1c1c";
  let midGray = "#8e8d8c";
  let lightGray = "#e6e6e6";
  let errorRed = "#880000";
  let correctGreen = "#E8FFB7";

  export let gameCounter;
  export let transitionHeight;
	export let transitionWidth;
  let gameStart = "";
  let windowWidth = 0;
  let appearIndex = 0;
  let dotsReady = false;
  let disappearIndex = null;
  let originalSVGWidth = 1300;
  let originalSVGHeight = 1477;


  let hoveredDot = { setIndex: null, dotIndex: null };
  let hintOpacity = 0;
  const gameContainerHeight = new Tween(transitionHeight, {
    duration: 500,
    easing: cubicInOut,
  });
  const gameContainerWidth = new Tween(transitionWidth, {
    delay: 500,
    duration: 500,
    easing: cubicInOut,
  });
  const gameContentOpacity = new Tween(1, {
    duration: 500,
    easing: cubicOut,
  });

  function setGameDimensions(width) {
    if (width >= 1200) {
      // large screens
      gameContainerHeight.target = 700;
      gameContainerWidth.target = 1000;
    } else if (width >= 900) {
      // medium screens
      gameContainerHeight.target = 700;
      gameContainerWidth.target = 800;
    } else if (width >= 480) {
      // small screens
      gameContainerHeight.target = 600;
      gameContainerWidth.target = 480;
    } else {
      // mobile screens
      gameContainerHeight.target = 400;
      gameContainerWidth.target = 350;
    }
  }


  function handleResize() {
    windowWidth = window.innerWidth;
    dotSets = windowWidth < 480 ? dotSets.slice(0, 3) : dotSets;
    originalSVGWidth = windowWidth < 480 ? 1400: 1300;
    originalSVGHeight = windowWidth < 480 ? 1200: 1477;
    setGameDimensions(windowWidth);
  }

  let completedSetIds = new Set();
  $: allCompleted = dotSets.every((set) => set.currentStep === set.dots.length);

  let dotSets = [
  {
    id: 1,
    color: "#34CF49",
    dots: [
      { x: 295, y: 938, label: "UNDER" },
      { x: 453, y: 769, label: "YOUR" },
      { x: 599, y: 665, label: "THUMB" },
    ],
    currentStep: 0,
    lines: [],
  },
  {
    id: 2,
    color: "#815322",
    dots: [
      { x: 599, y: 665, label: "THUMB" },
      { x: 780, y: 616, label: "HIS" },
      { x: 780, y: 817, label: "NOSE" },
      { x: 1100, y: 438 , label: "AT"},
    ],
    currentStep: 0,
    lines: [],
  },
  {
    id: 3,
    color: "#7323F4",
    dots: [
      { x: 1100, y: 438, label: "AT" },
      { x: 780, y: 77, label: "THE" },
      { x: 780, y: 297, label: "END" },
      { x: 575, y: 361, label: "OF" },
      { x: 401, y: 486, label: "MY" },
      { x: 279, y: 824, label: "ROPE" },
    ],
    currentStep: 0,
    lines: [],
  },
  {
    id: 4,
    color: "#F0484E",
    dots: [
      { x: 124, y: 253, label: "ALL" },
      { x: 227, y: 168, label: "BENT" },
      { x: 591, y: 168, label: "OUT" },
      { x: 643, y: 206, label: "OF" },
      { x: 591, y: 239, label: "SHAPE"},
    ],
    currentStep: 0,
    lines: [],
  },
  {
    id: 5,
    color: "#C948F0",
    dots: [
      { x: 591, y: 239, label: "SHAPE" },
      { x: 260, y: 239, label: "UP" },
      { x: 141, y: 369, label: "OR" },
      { x: 141, y: 915, label: "SHIP" },
      { x: 279, y: 1072, label: "OUT" },
    ],
    currentStep: 0,
    lines: [],
  },
  {
    id: 7,
    color: "#71A388",
    dots: [
      { x: 135, y: 1064, label: "ONE" },
      { x: 75, y: 946, label: "SIZE" },
      { x: 75, y: 369, label: "FITS" },
      { x: 124, y: 253, label: "ALL" },
    ],
    currentStep: 0,
    lines: [],
  },
  {
    id: 8,
    color: "#FFAE3E",
    dots: [
      { x: 279, y: 1072, label: "OUT" },
      { x: 849, y: 1072, label: "OF" },
      { x: 991, y: 942, label: "THE" },
      { x: 991, y: 739, label: "BLUE" },
    ],
    currentStep: 0,
    lines: [],
  },
  {
    id: 9,
    color: "#3E4AFF",
    dots: [
      { x: 991, y: 739, label: "BLUE" },
      { x: 1027, y: 692, label: "IN" },
      { x: 1064, y: 739, label: "THE" },
      { x: 1064, y: 950, label: "FACE" },
    ],
    currentStep: 0,
    lines: [],
  },
  {
    id: 10,
    color: "#FF3EC8",
    dots: [
      { x: 871, y: 1143, label: "PULL" },
      { x: 386, y: 1143, label: "A" },
      { x: 253, y: 1143, label: "FAST" },
      { x: 135, y: 1064, label: "ONE" },
    ],
    currentStep: 0,
    lines: [],
  },
];

  $: allDots = dotSets.flatMap((set, setIndex) => 
  set.dots.map((dot, dotIndex) => ({
    setIndex,
    dotIndex,
    dot,
  }))
);

  function scaleDotSets(
    dotSets,
    originalWidth,
    originalHeight,
    newWidth,
    newHeight,
    keepAspect = true,
    verticalPadding = 0,
  ) {
    const scaleX = newWidth / originalWidth;
    const scaleY = newHeight / originalHeight;

    let offsetX = 0;
    let offsetY = 0;

    let scaleUsedX = scaleX;
    let scaleUsedY = scaleY;

    if (keepAspect) {
      const uniformScale = Math.min(scaleX, scaleY);
      offsetX = (newWidth - originalWidth * uniformScale) / 2;
      offsetY = (newHeight - originalHeight * uniformScale) / 2;
      scaleUsedX = scaleUsedY = uniformScale;
    }

    // Add extra vertical padding
    offsetY += verticalPadding;

    return dotSets.map((set) => ({
      ...set,
      dots: set.dots.map((dot) => ({
        ...dot,
        x: dot.x * scaleUsedX + offsetX,
        y: dot.y * scaleUsedY + offsetY,
      })),
    }));
  }

  //Get right-most dot, for placing the click-fade zone
  $: atDot = (() => {
    for (const set of dotSets) {
      for (const dot of set.dots) {
        if (dot.label === "AT") {
          return dot;
        }
      }
    }
    return null;
  })();

  let mouse = { x: 0, y: 0 };
  let gameBoard;

  function isDotActive(setIndex, dotIndex) {
    const set = dotSets[setIndex];

    // If set is completed, no interaction allowed
    if (completedSetIds.has(set.id)) return false;

    // If set is in progress, allow only currentStep dot
    if (set.currentStep > 0 && set.currentStep < set.dots.length) {
      return dotIndex === set.currentStep;
    }

    // If no sets are currently active, allow first dot only
    const anyInProgress = dotSets.some(
      (s) =>
        !completedSetIds.has(s.id) &&
        s.currentStep > 0 &&
        s.currentStep < s.dots.length,
    );

    return !anyInProgress && dotIndex === 0;
  }

  function isDotDisabled(setIndex, dotIndex) {
    const set = dotSets[setIndex];

    // Disable if it's ahead of the current step
    if (dotIndex > set.currentStep) return true;

    // Disable if another set is mid-progress
    const anotherSetInProgress = dotSets.some(
      (otherSet, i) =>
        i !== setIndex &&
        !completedSetIds.has(otherSet.id) &&
        otherSet.currentStep > 0 &&
        otherSet.currentStep < otherSet.dots.length,
    );

    return anotherSetInProgress;
  }

  function handleClick(setIndex, dotIndex) {
    const set = dotSets[setIndex];

    // Check if this set is already completed
    if (completedSetIds.has(set.id)) return;

    // Check if any other set is currently being drawn
    const anyInProgress = dotSets.some((otherSet, i) => {
      return (
        i !== setIndex &&
        !completedSetIds.has(otherSet.id) &&
        otherSet.currentStep > 0 &&
        otherSet.currentStep < otherSet.dots.length
      );
    });

    if (anyInProgress) return; // disallow drawing another set until current one is finished

    // Proceed with drawing
    if (dotIndex === set.currentStep) {
      if (set.currentStep > 0) {
        set.lines = [
          ...set.lines,
          {
            from: set.dots[set.currentStep - 1],
            to: set.dots[set.currentStep],
          },
        ];
      }

      set.currentStep += 1;

      // Mark as completed
      if (set.currentStep === set.dots.length) {
        completedSetIds.add(set.id);
      }

      dotSets[setIndex] = { ...set };
      dotSets = [...dotSets]; // trigger reactivity
    }
  }

  function isFirstClickable(setIndex, dotIndex) {
    const set = dotSets[setIndex];

    const noSetInProgress = !dotSets.some(
      (s) =>
        !completedSetIds.has(s.id) &&
        s.currentStep > 0 &&
        s.currentStep < s.dots.length,
    );

    return (
      !completedSetIds.has(set.id) &&
      set.currentStep === 0 &&
      dotIndex === 0 &&
      noSetInProgress
    );
  }

  function winCondition() {
  if (allCompleted) {
    setTimeout(() => {
      disappearIndex = appearIndex; // Start with all dots visible
      const interval = setInterval(() => {
        disappearIndex -= 1;
        if (disappearIndex <= 0) {
          typeWriter("instructions", "")
          clearInterval(interval);
        }
      }, 20); // make dots disappear one by one
    }, 500);
    setTimeout(() => {
      gameContentOpacity.target = 0;
    }, 1500)
    setTimeout(() => {
      transitionHeight = gameContainerHeight.target
      transitionWidth = gameContainerWidth.target
    }, 2000)
    setTimeout(() => {
      gameCounter = 4;
    }, 2500)
  }
}

  let ready = false;
  onMount(() => {
    if (gameCounter == 3) {
    gameStart = "display: flex;";
    setTimeout(() => {
      typeWriter("title", "CLICHÉ")
    }, 1000);
    setTimeout(() => {
      typeWriter("title", "")
    }, 2500);
    setTimeout(() => {
      typeWriter("instructions", "SHARE YOUR THOUGHTS.")
      typeWriter("game-title", "4:CLICHÉ")
    }, 4500);
    setTimeout(() => {
      hintOpacity = 1
    }, 10000);
  }

    let verticalPadding = 0;
    if (typeof window !== "undefined") {
      handleResize(); // wait one tick
      dotSets = scaleDotSets(
        dotSets,
        originalSVGWidth,
        originalSVGHeight,
        gameContainerWidth.target,
        gameContainerHeight.target - 50,
        true,
        verticalPadding,
      );
      window.addEventListener("resize", handleResize);
    }
    ready = true;

    setTimeout(()=>{
      const totalDots = dotSets.reduce((sum, set) => sum + set.dots.length, 0);
    const interval = setInterval(() => {
      appearIndex += 1;
      if (appearIndex > totalDots + 10) {
        // extra buffer
        clearInterval(interval);
        dotsReady = true;
      }
    }, 20); // <-- 50ms per dot animation
    }, 3000)


    function handleMouseMove(event) {
      const bounds = gameBoard?.getBoundingClientRect();
      if (bounds) {
        mouse.x = event.clientX - bounds.left;
        mouse.y = event.clientY - bounds.top - 70;
      }
    }

    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  });


  let isRunning = false;
  let animateHint = false;
	let closeHint = false;
  
	function typeWriter(textID, newText, speed = 100) {
		let element = document.getElementById(textID);
		let typeDelay = 0;
		if (textID === "hint") {
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
  let hintsLeft = 2;

  async function hintButton() {
    if (isRunning) return; // prevent overlapping calls
    isRunning = true;
    if (hintCount == 0) {
      typeWriter("hint", "DON'T FORGET THE OVERLAPS.");
      hintsLeft = 1;
      hintCount++;
    } else if (hintCount == 1) {
      typeWriter("hint", "FOLLOW THE ARROW...");
      hintsLeft = 0;
      hintCount = 0;
    }
  }
</script>

{#if ready}
  <div class="page-container" style={gameStart}>
    <div
      bind:this={gameBoard}
      class="game-board"
      style="{gameStart} --dark-gray: {darkGray}; --mid-gray: {midGray}; --light-gray: {lightGray};  --error-red: {errorRed}; width: {gameContainerWidth.current}px; height:{gameContainerHeight.current}px;"
    >
      <div
        class="click-fade-zone"
        on:click={winCondition}
        style="
    left: {atDot ? atDot.x + 10 : 0}px;
  "
      />
      <div class="game-contents"  style=" opacity:{gameContentOpacity.current};">
        <div
          class="instructions-container"
        >
          <div id="game-title"></div>
          <div id="instructions"></div>
          <div class="tooltip-container">
            <div class="hint-button" on:click={hintButton} style="opacity: {hintOpacity}">
              <span>(?)</span> <span style="font-size:10px;">{hintsLeft}</span>
            </div>
            <span class="tooltip-text">USE A HINT! WHY NOT?</span>
          </div>
        </div>
        <div id="hint" 			class:animate-hint={animateHint}
        class:animate-hint-out={closeHint}></div>

        <div class="connect-container">
          <svg
            class="dotsSVG"
            width={gameContainerWidth.target}
            height={gameContainerHeight.target - 32}
                      >
            {#each dotSets as set}
              {#each set.lines as line}
                <line
                  x1={line.from.x}
                  y1={line.from.y}
                  x2={line.to.x}
                  y2={line.to.y}
                  stroke={allCompleted ? correctGreen : lightGray}
                  stroke-width="1"
                />
              {/each}

              {#if set.currentStep > 0 && set.currentStep < set.dots.length}
                <line
                  x1={set.dots[set.currentStep - 1].x}
                  y1={set.dots[set.currentStep - 1].y}
                  x2={mouse.x}
                  y2={mouse.y}
                  stroke={lightGray}
                  stroke-width="1"
                  stroke-dasharray="4"
                />
              {/if}
            {/each}
          </svg>

          {#each allDots as { setIndex, dotIndex, dot }, i}
          {#if i < appearIndex && (disappearIndex === null || i < disappearIndex)}
          <div
              class="dot-container"
              style="
                left: {dot.x}px;
                top: {dot.y}px;
                opacity: 1;
                transform: translate(-50%, -25%) scale(1);
                pointer-events: {isDotActive(setIndex, dotIndex) ? 'auto' : 'none'};
                transition: opacity 0.4s ease, transform 0.4s ease;
              "
            >
              <input
                type="checkbox"
                style="pointer-events: {isDotActive(setIndex, dotIndex) ? 'auto' : 'none'};"
                class="dot-radio 
                {isFirstClickable(setIndex, dotIndex) ? 'first-clickable' : ''}
                {isDotActive(setIndex, dotIndex) && hoveredDot.setIndex === setIndex && hoveredDot.dotIndex === dotIndex ? 'pulse-on-hover' : ''}"
                checked={dotIndex < dotSets[setIndex].currentStep}
                disabled={isDotDisabled(setIndex, dotIndex)}
                on:change={() => handleClick(setIndex, dotIndex)}
                on:mouseenter={() => {
                  hoveredDot = { setIndex, dotIndex };
                }}
                on:mouseleave={() => {
                  hoveredDot = { setIndex: null, dotIndex: null };
                }}
                
              />
              <div class="label">{dot.label}</div>
            </div>
          {/if}
        {/each}        
        </div>
      </div>
    </div>
  </div>
  <div id="title">
  </div>
{/if}

<style>
  .game-board {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: var(--mid-gray);
    border-radius: 0.75em;
    margin: auto;
    padding: 3em;
  }

  .connect-container {
    margin: auto;
    position: absolute;
    left: 0;
    top: 70px;
    bottom: 0;
    right: 0;
    z-index: 1;
    overflow: visible;
  }

  #game-title {
    color: var(--dark-gray);
    justify-self: start;
  }

  .dotsSVG {
    margin: auto;
    position: absolute;
    pointer-events: none;
    z-index: 2;
  }

  .dot-container {
    position: absolute;
    transform: translate(-50%, -25%);
    z-index: 3;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  @keyframes pulse {
    0% {
      box-shadow: 0 0 0 0 rgba(220, 220, 220, 0.5);
    }
    70% {
      box-shadow: 0 0 0 10px rgba(52, 207, 73, 0);
    }
    100% {
      box-shadow: 0 0 0 0 rgba(52, 207, 73, 0);
    }
  }

  .dot-radio.first-clickable {
    animation: pulse 1.5s infinite;
  }

  /* When checked, show the inner dot */
  input[type="checkbox"].dot-radio:checked::before {
    content: "";
    position: absolute;
    top: 2px;
    left: 2px;
    width: 6px;
    height: 6px;
    background-color: var(--light-gray);
    border-color: var(--dark-gray);
    border-radius: 50%;
    -webkit-filter: drop-shadow(0px 0px 4px var(--light-gray));
  }

  input[type="checkbox"].dot-radio {
    appearance: none;
    -webkit-appearance: none;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: 1px solid var(--dark-gray);
    /* background-color: #fff; */
    cursor: pointer;
    pointer-events: auto;
    margin: 0;
    padding: 0;
    display: inline-block;
    position: relative;
    transition:
      background-color 0.2s,
      border-color 0.2s;
  }

  .dot-radio.pulse-on-hover {
  animation: pulse 1s infinite;
}

  input[type="checkbox"].dot-radio:disabled {
    /* opacity: 0.5; */
    cursor: not-allowed;
  }

  .label {
    font-size: 10px;
    margin-top: 3px;
    color: var(--light-gray);
    user-select: none;
    -webkit-filter: drop-shadow(0px 0px 4px var(--light-gray));
  }
  @media (max-width: 900px) {
    .label {
      font-size: smaller;
    }
  }
  @media (max-width: 480px) {
    .label {
      font-size: 7px;
    }
  }

  line {
    -webkit-filter: drop-shadow(0px 0px 4px var(--light-gray));
    transition: stroke 1s ease;
  }

  .game-contents {
    width: 100%;
  }
  .instructions-container {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    position: relative;
    max-height: 3em;
    justify-content: space-between;
  }

  #instructions {
    font-weight: 400;
    color: var(--dark-gray);
  }

  .click-fade-zone {
    position: absolute;
    top: 100px;
    width: 200px;
    height: 50%;
    z-index: 10;
    cursor: pointer;
    background: transparent;
  }
  @media (max-width: 900px) {
    .click-fade-zone {
      width: 100px;
    }
  }
  @media (max-width: 480px) {
    .click-fade-zone {
      width: 20px;
    }
  }

  #title {
    height: 20px;
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    margin: auto 0;
    margin-inline: auto;
    width: fit-content;
    font-size: 2em;
  }

  .page-container {
    width: 100vw;
    height: 100dvh;
    position: absolute;
    opacity: 1;
    display: none;
    justify-content: center;
    flex-direction: column;
    align-items: center;
  }

  .hint-button {
    color: var(--dark-gray);
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    align-self: flex-end;
    cursor: pointer;
    z-index: 999;
    transition: opacity 1s ease-in-out; /* Animation duration and effect */
  }

  .hint-button > * {
    padding: 0.15em;
  }

  .tooltip-container {
    justify-self: right;
    position: relative;
    display: inline-block;
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
    top: 100%;
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


	#hint {
		background-color: var(--error-red);
		width: 100%;
		text-align: center;
		align-self: center;
		align-items: center;
		margin-left: auto;
		height: 1.5em;
		line-height: 1.5em;
    margin-bottom: 1em;
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


</style>
