<script>
  import { onMount, onDestroy } from "svelte";
  import { Tween } from "svelte/motion";
  import { cubicOut, cubicInOut } from "svelte/easing";
  import { tick } from "svelte";

  let darkGray = "#1c1c1c";
  let midGray = "#8e8d8c";
  let lightGray = "#e6e6e6";
  let errorRed = "#880000";
  let correctGreen = "#E8FFB7";

  export let transitionHeight;
  export let transitionWidth;

  export let gameCounter;
  let gameStart = "";
  let hintButtonOpacity = 0;
  let ready = false;
  let windowWidth = 0;

  const gameContentOpacity = new Tween(0, {
    duration: 1000,
    easing: cubicOut,
  });
  let gameHeight = new Tween(transitionHeight, {
    delay: 500,
    duration: 500,
    easing: cubicInOut,
  });
  let gameWidth = new Tween(transitionWidth, {
    duration: 500,
    easing: cubicInOut,
  });

  function setGameDimensions(width) {
    if (width >= 1200) {
      // large screens
      gameWidth.target = 700;
      gameHeight.target = 700;
    } else if (width >= 900) {
      // medium screens
      gameWidth.target = 700;
      gameHeight.target = 700;
    } else if (width >= 480) {
      // small screens
      gameWidth.target = 480;
      gameHeight.target = 500;
    } else {
      // mobile screens
      gameWidth.target = 350;
      gameHeight.target = 600;
    }
  }

  function handleResize() {
    windowWidth = window.innerWidth;
    setGameDimensions(windowWidth);
  }

  let pegs = [
    { name: "COMMON", x: 0, y: 0, landed: false },
    { name: "CHARGE", x: 0, y: 0, landed: false },
    { name: "FIND", x: 0, y: 0, landed: false },
    { name: "SHOCK", x: 0, y: 0, landed: false },
    { name: "FIGURE", x: 0, y: 0, landed: false },
    { name: "FREAK", x: 0, y: 0, landed: false },
    { name: "PROGRESS", x: 0, y: 0, landed: false },
    { name: "CARRY", x: 0, y: 0, landed: false },
    { name: "POINT", x: 0, y: 0, landed: false },
    { name: "VAIN", x: 0, y: 0, landed: false },
  ];

  let inPegs = ["CHARGE", "COMMON", "PROGRESS", "SHOCK", "VAIN"];

  onMount(async () => {
    if (gameCounter == 2) {
      gameStart = "display: flex;";
      setTimeout(() => {
        typeWriter("title", "METAPHOR");
      }, 1000);
      setTimeout(() => {
        typeWriter("title", "");
      }, 2500);
      setTimeout(() => {
        gameContentOpacity.target = 1;
      }, 3500);
      setTimeout(() => {
        typeWriter("game-title", "3:METAPHOR");
      }, 4500);

      setTimeout(() => {
        hintButtonOpacity = 1;
      }, 10000);
    }

    if (typeof window !== "undefined") {
      handleResize(); // set initial size
      await tick();
      window.addEventListener("resize", handleResize);
      ready = true;
      requestAnimationFrame(() => {
        // <-- wait for next frame
        const map = document.getElementById("map");
        map.style.width = gameWidth.target;
        map.style.height = gameHeight.target;

        const mapRect = map.getBoundingClientRect();

        if (mapRect.width === 0 || mapRect.height === 0) {
          console.warn("Map dimensions not ready, retrying...");
          return;
        }

        pegs.forEach((peg) => {
          peg.x = Math.random() * mapRect.width;
          peg.y = Math.random() * (mapRect.height - 100);
        });

        const pegmen = document.querySelectorAll(".pegman-container");
        const timeout = 25;
        const maxDegrees = 50;

        // Circle detection setup
        const circle = document.getElementById("circle");
        const circleRect = circle.getBoundingClientRect();
        const circleCenter = {
          x: circleRect.left + circleRect.width / 2,
          y: circleRect.top + circleRect.height / 2,
        };
        const radius = circleRect.width / 2;

        // Get pegmen inside circle
        function getPegmenNamesInsideCircle() {
          const pegmen = document.querySelectorAll(".pegman");
          const circle = document.getElementById("circle");
          const circleRect = circle.getBoundingClientRect();
          const circleCenter = {
            x: circleRect.left + circleRect.width / 2,
            y: circleRect.top + circleRect.height / 2,
          };
          const radius = circleRect.width / 2;

          const insideNames = [];

          pegmen.forEach((pegman) => {
            const rect = pegman.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;

            const dx = centerX - circleCenter.x;
            const dy = centerY - circleCenter.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            let shadow = pegman.nextElementSibling;
            if (distance <= radius) {
              // Get the name from the label below the pegman
              const label = pegman.previousElementSibling;
              if (label) {
                insideNames.push(label.textContent.trim());
              }
              shadow.innerHTML = "IN";
            } else {
              shadow.innerHTML = "OUT";
            }
          });

          return insideNames;
        }

        function winCondition() {
          setTimeout(() => {
            const pegmen = document.querySelectorAll(".pegman");
            const labels = document.querySelectorAll(".label");
            pegmen.forEach((pegman) => {
              setTimeout(() => {
                pegman.classList.add("correct-pegman"); // Add correct class when faded out
              }, 0); // wait for fade-out to complete
            });
            console.log(labels)
            labels.forEach((label) => {
              setTimeout(() => {
                label.classList.add("correct-label"); // Add correct class when faded out
              }, 0); // wait for fade-out to complete
            });
          }, 0);
          //hold for 2 seconds
          setTimeout(() => {
            gameContentOpacity.target = 0;
          }, 3000);

          setTimeout(() => {
            transitionHeight = gameHeight.target;
            transitionWidth = gameWidth.target;
            gameCounter = 3;
          }, 4000);
        }

        pegmen.forEach((pegman, i) => {
          let isDragging = false;
          let initialX = 0;
          let initialY = 0;
          let inactivityTimeout;
          let lastX = 0;
          let dx = pegs[i].x;
          let dy = pegs[i].y;

          if (pegs[i].landed === false) {
            pegman.animate(
              [
                {
                  translate: `${pegs[i].x}px -100px`,
                  scale: "1 1",
                  opacity: 0,
                  offset: 0,
                },
                {
                  translate: `${pegs[i].x}px ${pegs[i].y - 20}px`,
                  scale: "0.8 1.2",
                  opacity: 1,
                  offset: 0.7,
                },
                {
                  translate: `${pegs[i].x}px ${pegs[i].y + 10}px`,
                  scale: "1.3 0.7",
                  offset: 0.85,
                },
                {
                  translate: `${pegs[i].x}px ${pegs[i].y}px`,
                  scale: "1 1",
                  offset: 1,
                },
              ],
              {
                delay: 3300,
                duration: 100 + i * 100,
                easing: "ease-out",
                fill: "forwards",
              },
            );
          } else {
            pegman.animate(
              { translate: `${pegs[i].x}px ${pegs[i].y}px` },
              {
                duration: 0.01,
                fill: "forwards",
              },
            );
          }

          const onMouseDown = (e) => {
            isDragging = true;
            initialY = e.clientY - dy;
            initialX = e.clientX - dx;

            pegman.animate(
              { translate: `${pegs[i].x}px ${pegs[i].y}px ` },
              {
                duration: 0.01,
                fill: "forwards",
              },
            );
          };

          const onMouseMove = (e) => {
            if (!isDragging) return;

            let newX = e.clientX - initialX;
            let newY = e.clientY - initialY;

            // Clamp X and Y within the map bounds
            const pegWidth = 35;
            const pegHeight = 50;

            newX = Math.max(0, Math.min(newX, mapRect.width - pegWidth));
            newY = Math.max(0, Math.min(newY, mapRect.height - 50 - pegHeight));

            dx = newX;
            dy = newY;

            pegs[i].x = dx;
            pegs[i].y = dy;
            pegs = [...pegs];

            let rx = Math.max(-maxDegrees, Math.min(maxDegrees, dx - lastX));
            pegman.setAttribute("style", `--r: ${rx}deg`);

            pegman.animate(
              { translate: `${dx}px ${dy}px ` },
              {
                duration: 100,
                fill: "forwards",
              },
            );

            clearTimeout(inactivityTimeout);

            inactivityTimeout = setTimeout(() => {
              lastX = dx;
              pegman.setAttribute("style", `--r: 0`);
            }, timeout);
          };

          const onMouseUp = () => {
            // console.log(getPegmenNamesInsideCircle())

            isDragging = false;
            pegman.setAttribute("style", `--r: 0`);
            inactivityTimeout = setTimeout(() => {
              lastX = 0;
            }, timeout);
            if (
              getPegmenNamesInsideCircle().sort().join(",") === inPegs.join(",")
            ) {
              winCondition();
            }
          };

// Mouse events
pegman.addEventListener("mousedown", onMouseDown);
document.addEventListener("mousemove", onMouseMove);
document.addEventListener("mouseup", onMouseUp);

// Touch events
pegman.addEventListener("touchstart", (e) => {
  const touch = e.touches[0];
  onMouseDown({ clientX: touch.clientX, clientY: touch.clientY });
});
document.addEventListener("touchmove", (e) => {
    const touch = e.touches[0];
    onMouseMove({ clientX: touch.clientX, clientY: touch.clientY });
    e.preventDefault(); // prevent scrolling while dragging
  
}, { passive: false }); // required to allow preventDefault

document.addEventListener("touchend", onMouseUp);

        });
      });
    }
  });

  
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

  async function hintButton() {
    if (isRunning) return; // prevent overlapping calls
    isRunning = true;
    if (hintCount == 0) {
      let shadows = document.querySelectorAll(".pegman-shadow");
      shadows.forEach((shadow) => {
        shadow.setAttribute("style", "filter:blur(0px)");
      });
      hintsLeft = 2;
      hintCount++;
      setTimeout(() => {
        isRunning = false;
      }, 5000);
    } else if (hintCount == 1) {
      typeWriter("hint", "TRY MOVING WORDS IN AND OUT.");
      hintsLeft = 1;
      hintCount++;
    } else if (hintCount == 2) {
      typeWriter("hint", "LABEL + POSITION = ?");
      hintsLeft = 0;
      hintCount++;
    }
  }

  onDestroy(() => {
    if (typeof window !== "undefined") {
      window.removeEventListener("resize", handleResize);
    }
  });
</script>

{#if ready}
  <div class="page-container" style={gameStart}>
    <div
      class="game-container"
      style="{gameStart} --dark-gray: {darkGray}; --mid-gray: {midGray}; --light-gray: {lightGray};  --error-red: {errorRed}; --correct-green: {correctGreen}; height: {gameHeight.current +
        'px'}; width: {gameWidth.current + 'px'};"
    >
      <div
        class="game-contents"
        style="opacity:{gameContentOpacity.current}; height: {gameHeight.current +
          'px'}; width: {gameWidth.current + 'px'};"
      >
        <div class="instructions-container">
          <div id="game-title"></div>
          <div></div>
          <div class="tooltip-container" style="opacity: {hintButtonOpacity}">
            <div class="hint-button" on:click={hintButton}>
              <span>(?)</span> <span style="font-size:10px;">{hintsLeft}</span>
            </div>
            <span class="tooltip-text">USE A HINT! LOOK CLOSELY...</span>
          </div>
        </div>
        <div id="hint"
        class:animate-hint={animateHint}
        class:animate-hint-out={closeHint}
        ></div>
        <div
          id="map"
          style="height: calc({gameHeight.target}px - 7em); width: calc({gameWidth.target}px - 6em);"
        >
        <div class="circle-container">
          <div class="drawn-circle"></div>
        </div>
        
          <div id="circle"></div>
          <!-- <div id="in">IN</div>
            <div id="out">OUT</div> -->
          {#each pegs as peg, i}
            <div class="pegman-container">
              <div class="label">{peg.name}</div>
              <div class="pegman" data-index={i}></div>
              <div class="pegman-shadow">IN</div>
            </div>
          {/each}
        </div>
      </div>
    </div>
  </div>
  <div id="title"></div>
{/if}

<style>
  .page-container {
    width: 100vw;
    height: 100dvh;
    overflow: hidden;
    position: absolute;
    opacity: 1;
    display: none;
    justify-content: center;
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

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  .instructions-container {
    display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  position: relative;
  }

  .game-container {
    display: none;
    background-color: var(--mid-gray);
    border-radius: 0.75em;
    margin: auto;
    padding: 3em;
  }
  @media (max-width: 480px) {
    .game-container {
      padding: 2em;
    }
  }

  .game-contents {
    flex-direction: column;
    align-items: center;
  }

  #game-title {
    color: var(--dark-gray);
    justify-self: start;
  }

  :root {
    --pegman-initial: url("/pegman-initial.png");
    --pegman-moving: url("/pegman-moving.png");
    --pegman-correct: url("/pegman-correct.png");
  }

  :global(.correct-pegman) {
    background-image: var(--pegman-correct) !important;
  }

  #map {
    background-size: cover;
    background-position: center center;
    overflow: visible;
  }

  .pegman {
    width: 35px;
    height: 45px;
    background-image: var(--pegman-initial);
    background-size: 55px;
    background-position: -8px -9px;
    rotate: var(--r);
    transform-origin: 50% 0%;
    transition: rotate 200ms;
    cursor: grab;
    transition:
      background-image 1s linear,
      opacity 1s linear,
      rotate 200ms;
    opacity: 1;
  }

  @font-face {
    font-family: "ArialNarrow";
    font-style: normal;
    font-weight: 300;
    src: url("./fonts/arialnarrow.ttf"); /* IE9 Compat Modes */
  }

  .pegman-shadow {
    width: 15px;
    height: 15px;
    font-family: "ArialNarrow";
    color: var(--dark-gray);
    -webkit-transform: skew(40deg) translate(10px, -6px);
    border-radius: 50px;
    filter: blur(6px);
    opacity: 50%;
    user-select: none;
    transition: filter 2s ease-in-out;
  }
  @media(max-width: 480px) {
    .pegman-shadow {
      filter: blur(3px);
    }
  }

  .pegman-container {
    position: absolute;
    width: 35px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .label {
    text-align: center;
    color: var(--light-gray);
    font-size: 12px;
    user-select: none;
    pointer-events: none;
    font-family: sans-serif;
    -webkit-filter: drop-shadow(0px 0px 4px var(--light-gray));
  }

  :global(.correct-label) {
    color: var(--correct-green) !important;
    -webkit-filter: drop-shadow(0px 0px 4px var(--correct-green)) !important;
  }

  .pegman:active {
    background-image: var(--pegman-moving);
    cursor: grabbing;
    background-size: 55px;
    background-position: -8px -9px;
  }

  @keyframes circleDraw {
    0% {
			stroke-dashoffset: 100%;
		}
		100% {
			stroke-dashoffset: 0%;
		}
  }

  #circle {
    position: absolute;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    border: 1px dashed var(--dark-gray);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
    animation: 10s ease-in 1s circleDraw;
  }
  @media (max-width: 900px) {
    #circle {
      width: 300px;
      height: 300px;
    }
  }
  @media (max-width: 480px) {
    #circle {
      width: 250px;
      height: 250px;
    }
  }

  .hint-button {
    color: var(--dark-gray);
    border-radius: 100px;
    padding-right: 0.5em;
    padding-left: 0.5em;
    display: flex;
    flex-direction: row;
    align-items: center;
    cursor: pointer;
    transition: opacity 1s ease-in-out; /* Animation duration and effect */
  }

  .hint-button > * {
    padding: 0.15em;
  }

  .tooltip-container {
    justify-self: right;
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
    margin-bottom: 4vh;
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
