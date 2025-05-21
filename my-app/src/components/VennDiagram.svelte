<script>
  import * as d3 from "d3";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import { fade } from "svelte/transition";
  import { tick } from "svelte";
  import { Tween } from "svelte/motion";
  import { cubicOut } from "svelte/easing";
  import { get } from "svelte/store";

  let darkGray = "#1c1c1c";
  let midGray = "#8e8d8c";
  let lightGray = "#e6e6e6";
  let errorRed = "#880000";
  let correctGreen = "#E8FFB7";

  export let gameCounter;
  export let transitionHeight;
  export let transitionWidth;
  let windowWidth = 0;
  let numColumns = 3;
  let circleRadius = 0;
  let ready = false;
  let svgElement;
  const gameContentOpacity = new Tween(0, {
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
  let hintButtonOpacity = 0;
  let oneVW = 0;
  let rowSpacing = 0;
  let titleDisplay = "";

  let width = 0; // example SVG width
  let height = 0; // example SVG height

  function setGameDimensions(wWidth) {
    console.log(wWidth);
    if (width >= 1200) {
      // large screens
      gameHeight.target = 700;
      gameWidth.target = 1000;
      circleRadius = 100;
      width = 1000;
      height = 500;
      rowSpacing = 210;
    } else if (wWidth >= 900) {
      // medium screens
      gameHeight.target = 700;
      gameWidth.target = 800;
      circleRadius = 100;
      width = 800;
      height = height = 500;
      rowSpacing = 210;
    } else if (wWidth >= 480) {
      // small screens
      gameHeight.target = 600;
      gameWidth.target = 480;
      circleRadius = 60;
      numColumns = 2;
      width = 450;
      height = 525;
      rowSpacing = 125;
    } else {
      // mobile screens
      gameHeight.target = 600;
      gameWidth.target = 350;
      circleRadius = 55;
      numColumns = 2;
      width = 340;
      height = 400;
      rowSpacing = 125;
    }
  }

  function handleResize() {
    windowWidth = window.innerWidth;
    setGameDimensions(windowWidth);
  }

  let structuredData = {};

  const greenWords = writable([]);

  onMount(() => {
    document.addEventListener(
    "touchmove",
    (e) => {
      if (e.cancelable) e.preventDefault();
    },
    { passive: false }
  );
    if (gameCounter == 4) {
      setTimeout(() => {
        typeWriter("title", "JARGON");
      }, 1000);
      setTimeout(() => {
        typeWriter("title", "");
      }, 2500);
      setTimeout(() => {
        gameContentOpacity.target = 1;
      }, 3500);
      setTimeout(() => {
        typeWriter("game-title", "5:JARGON");
        typeWriter("instructions", "EXTREMELY DARK. (2)");
        gameContentOpacity.target = 1;
      }, 4500);
      setTimeout(() => {
        hintButtonOpacity = 1;
      }, 0); //TODO: 20000
    }

    if (typeof window !== "undefined") {
      handleResize(); // set initial size
      window.addEventListener("resize", handleResize);
    }
    console.log(numColumns);
    ready = true;

    // get jargon data
    d3.csv("./jargon.csv").then(function (data) {
      let columns = Object.keys(data[0]); // Get column headers

      columns.forEach((column) => {
        let values = data.map((row) => row[column]); // Extract column values
        values = values.map((x) => {
          return x.toUpperCase();
        });
        structuredData[column] = values.filter((str) => str.trim() !== ""); // Store the rest in columns
      });
    });
    oneVW = window.innerWidth / 100;
    console.log(structuredData);

    initializeSVG();
  });

  const rackWords = writable([]);

  function addToRack(word) {
    rackWords.update((words) => {
      if (words.includes(word)) return words;
      if (words.length >= 4) return words; // limit reached
      return [...words, word]; // add new word
    });
  }

  function removeFromRack(word) {
    rackWords.update((words) => words.filter((w) => w !== word));
  }

  // Circle data with position (cx, cy), radius (r), and a word.
  let circlesData;

  function initializeSVG() {
    circlesData = writable([
      {
        id: 1,
        cx: 150,
        cy: 150,
        r: circleRadius,
        domain: "JOURNALISM",
        el: null,
      },
      { id: 2, cx: 375, cy: 150, r: circleRadius, domain: "MUSIC", el: null },
      { id: 3, cx: 600, cy: 150, r: circleRadius, domain: "CHESS", el: null },
      { id: 4, cx: 825, cy: 375, r: circleRadius, domain: "COOKING", el: null },
      { id: 5, cx: 150, cy: 375, r: circleRadius, domain: "CODING", el: null },
      { id: 6, cx: 825, cy: 375, r: circleRadius, domain: "MAGIC", el: null },
    ]);

    const colSpacing = width / (numColumns + 1);

    circlesData.update((circles) => {
      return circles.map((circle, index) => {
        const row = Math.floor(index / numColumns);
        const col = index % numColumns;

        return {
          ...circle,
          cx: (col + 1) * colSpacing,
          cy: (row + 1) * rowSpacing - 60,
          el: null, // initialize for binding
        };
      });
    });

    // Wait for DOM update
    tick().then(() => {
      const $c = get(circlesData); // import { get } from 'svelte/store';
      $c.forEach((circle, i) => {
        const el = circle.el;
        if (el) {
          const length = 2 * Math.PI * circle.r;
          el.setAttribute("stroke-dasharray", length);
          el.setAttribute("stroke-dashoffset", length);

          // Animate with stagger
          setTimeout(() => {
            el.animate(
              [{ strokeDashoffset: length }, { strokeDashoffset: 0 }],
              {
                duration: 1000,
                easing: "ease-out",
                fill: "forwards",
              },
            );
          }, 3500+ i * 300);
        }
      });
    });

    tick().then(() => {
  const $c = get(circlesData);
  $c.forEach((circle, i) => {
    const labelEl = circle.textEl;
    if (labelEl) {
      labelEl.textContent = ""; // clear any content

      setTimeout(() => {
        typeText(labelEl, circle.domain, 50);
      }, 3500 + i * 300); // stagger
    }
  });
});
  }

  function typeText(el, text, speed = 50) {
  let i = 0;
  function typeNext() {
    if (i < text.length) {
      el.textContent += text[i];
      i++;
      setTimeout(typeNext, speed);
    }
  }
  typeNext();
}


  // To track overlapping text
  const overlaps = writable([]);

  // Function to handle the dragging of circles
  let draggedCircle = null;
  function startDrag(event, circle) {
  draggedCircle = circle;
  const isTouch = event.type.startsWith("touch");
  const clientX = isTouch ? event.touches[0].clientX : event.clientX;
  const clientY = isTouch ? event.touches[0].clientY : event.clientY;
  const offsetX = clientX - circle.cx;
  const offsetY = clientY - circle.cy;

  function moveDrag(event) {
    if (isTouch) event.preventDefault(); // ⛔ stop mobile scroll

    const moveX = isTouch
      ? event.touches[0].clientX
      : event.clientX;
    const moveY = isTouch
      ? event.touches[0].clientY
      : event.clientY;

    draggedCircle.cx = Math.max(
      draggedCircle.r * 1.5,
      Math.min(width - draggedCircle.r * 1.5, moveX - offsetX)
    );
    draggedCircle.cy = Math.max(
      draggedCircle.r,
      Math.min(height - draggedCircle.r, moveY - offsetY)
    );
    circlesData.set([...get(circlesData)]); // trigger reactive update
    checkOverlaps();
  }

  function endDrag() {
    if (isTouch) {
      window.removeEventListener("touchmove", moveDrag);
      window.removeEventListener("touchend", endDrag);
    } else {
      window.removeEventListener("mousemove", moveDrag);
      window.removeEventListener("mouseup", endDrag);
    }
  }

  if (isTouch) {
    window.addEventListener("touchmove", moveDrag);
    window.addEventListener("touchend", endDrag);
  } else {
    window.addEventListener("mousemove", moveDrag);
    window.addEventListener("mouseup", endDrag);
  }
}


  function getWordOverlaps(domain1, domain2) {
    let intersection = structuredData[domain1].filter((item) =>
      structuredData[domain2].includes(item),
    );
    return intersection;
  }

  // Check if any two circles overlap and return the overlap text
  function checkOverlaps() {
    const circles = $circlesData;
    const overlapArr = [];

    for (let i = 0; i < circles.length; i++) {
      for (let j = i + 1; j < circles.length; j++) {
        const d1 = circles[i];
        const d2 = circles[j];
        const dx = d1.cx - d2.cx;
        const dy = d1.cy - d2.cy;
        const distance = Math.sqrt(dx * dx + dy * dy);

        // If the circles overlap
        if (distance < d1.r + d2.r) {
          const overlapX = (d1.cx + d2.cx) / 2;
          const overlapY = (d1.cy + d2.cy) / 2;
          const overlapText = getWordOverlaps(d1.domain, d2.domain);
          overlapArr.push({ cx: overlapX, cy: overlapY, text: overlapText });
        }
      }
    }

    overlaps.set(overlapArr);
  }

  //win condition
  $: if ($rackWords[0] == "PITCH" && $rackWords[1] == "BLACK") {
    (async () => {
      await tick(); // wait for DOM update
      await new Promise((resolve) => setTimeout(resolve, 500)); // wait
      greenWords.set(["PITCH", "BLACK"]);
      setTimeout(() => {
        gameContentOpacity.target = 0;
      }, 1000);
      setTimeout(() => {
        transitionWidth = gameWidth.target;
        transitionHeight = gameHeight.target;
        gameCounter = 5;
      }, 2000);
    })();
  }

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
      typeWriter("hint", "TRY EXPLORING THE INTERSECTIONS.");
      hintsLeft = 1;
      hintCount++;
    } else if (hintCount == 1) {
      typeWriter("hint", "WHAT'S ANOTHER 2-WORD WAY TO SAY THIS?");
      hintsLeft = 0;
      hintCount++;
    }
  }

  
</script>

{#if ready}
  <div class="page-container-2">
    <div
      class="game-container"
      style="--dark-gray: {darkGray}; --mid-gray: {midGray}; --light-gray: {lightGray}; --correct-green: {correctGreen}; --error-red: {errorRed}; height: {gameHeight.current +
        'px'}; width: {gameWidth.current + 'px'};"
    >
      <div class="game-contents" style=" opacity:{gameContentOpacity.current};">
        <div class="header-container">
          <div id="game-title"></div>
          <div id="instructions"></div>
          <div class="tooltip-container" style="opacity: {hintButtonOpacity}">
            <div class="hint-button" on:click={hintButton}>
              <span>(?)</span> <span style="font-size:10px;">{hintsLeft}</span>
            </div>
            <span class="tooltip-text">USE A HINT! DON'T BE SCARED...</span>
          </div>
        </div>
        <div id="hint" 			class:animate-hint={animateHint}
        class:animate-hint-out={closeHint}></div>

        <svg
          bind:this={svgElement}
          style="width: {width}px; height: {height}px"
        >
        <defs>
          <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="4" result="blur"/>
            <feMerge>
              <feMergeNode in="blur"/>
              <feMergeNode in="blur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
          <!-- Circles -->
          {#each $circlesData as circle (circle.id)}
          <g
          transform="translate({circle.cx},{circle.cy})"
          on:mousedown={(event) => startDrag(event, circle)}
          on:touchstart={(event) => startDrag(event, circle)}
        >        
              <circle class="circle" r={circle.r} bind:this={circle.el} />
              <text
              class="venn-circle-label"
              text-anchor="middle"
              fill={darkGray}
              bind:this={circle.textEl}
            />
            </g>
          {/each}

          <!-- Overlap text -->
          {#each $overlaps as { cx, cy, text }}
            {#each text as t, i}
            <text
            class="overlap-text"
            text-anchor="center"
            x={cx}
            y={cy + i * 20}
            filter="url(#glow)"
            on:click={() => addToRack(t)}
          >
            {t}
          </text>
            {/each}
          {/each}
        </svg>

        <div class="rack">
          {#each $rackWords as word (word)}
            <div
              class="rack-word"
              on:click={() => removeFromRack(word)}
              transition:fade
              class:green={$greenWords.includes(word)}
            >
              {word}
            </div>
          {/each}
        </div>
      </div>
    </div>
  </div>
  <div id="title" style={titleDisplay}></div>
{/if}

<style>
  @font-face {
    font-family: "ArialNarrow";
    font-style: normal;
    font-weight: 400;
    src: url("./fonts/arialnarrow.ttf"); /* IE9 Compat Modes */
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
    z-index: 999;
    font-family: "ArialNarrow";
  }

  .page-container-2 {
    width: 100vw;
    height: 100dvh;
    position: absolute;
    opacity: 1;
    align-items: center;
    justify-content: center;
    display: flex;
  }
  @media (max-width: 900px) {
    .page-container-2 {
      font-size: smaller;
    }
  }
  @media (max-width: 480px) {
    .page-container-2 {
      font-size: small;
    }
  }

  svg {
    overflow: visible;
  }
  .circle {
    stroke: var(--dark-gray);
    stroke-width: 1px;
    fill: var(--dark-gray);
    fill-opacity: 0;
    cursor: move;
  }
  .overlap-text {
    fill: var(--light-gray);
    font-size: 1em;
    user-select: none;
    -webkit-user-select: none; /* Safari */
    cursor: pointer;
  }

  .game-container {
    background-color: var(--mid-gray);
    border-radius: 0.75em;
    margin: auto;
    padding: 3em;
  }

  #game-title {
    color: var(--dark-gray);
    justify-self: start;
  }

  .game-contents {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  #instructions {
    font-weight: 400;
    color: var(--dark-gray);
  }

  .venn-circle-label {
    font-family: "ROMMONO";
    letter-spacing: 1px;
    cursor: move;
    user-select: none;
    -webkit-user-select: none; /* Safari */
    font-size: 0.8em;
  }

  .rack {
    height: 40px;
    display: flex;
    justify-content: center;
    width: calc((min(5vmin, 50px) + 4px) * 8);
    border-bottom: solid;
    border-color: var(--light-gray);
    border-width: 0.5px;
  }
  .rack > * {
    margin-left: 6px;
  }

  .rack-word {
    cursor: pointer;
    height: 2em;
    /* width: calc(min(5vmin, 50px)); */
    user-select: none;
    padding-left: 12px;
    padding-right: 12px;
    border-radius: calc(min(4vmin, 40px));
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--dark-gray);
    background-color: var(--light-gray);
    max-width: fit-content;
    z-index: 1;
    box-shadow: 0px 0px 8px 1.5px var(--light-gray);
    transition:
      background-color 1s ease-in-out,
      box-shadow 1s ease-in-out,
      opacity 0.5s 2s ease-in-out; /* Animation duration and effect */
  }
  @media (max-width: 480px) {
    .rack-word {
    padding-left: .75em;
    padding-right: .75em;
		}
	}

  .rack-word.green {
    background-color: var(--correct-green);
    box-shadow: 0px 0px 8px 1.5px var(--correct-green);
  }

  .header-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    max-height: 3em;
    justify-content: space-between;
    width: 100%;
  }

  .hint-button {
    color: var(--dark-gray);
    padding-right: 0.5em;
    padding-left: 0.5em;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    align-self: right;
    cursor: pointer;
    transition: opacity 1s ease-in-out; /* Animation duration and effect */
  }

  .hint-button > * {
    padding: 0.15em;
  }

  .tooltip-container {
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
