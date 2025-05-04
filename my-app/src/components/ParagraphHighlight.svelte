<script>
  import * as d3 from "d3";
  import { onMount, onDestroy } from "svelte";
  import { Tween } from "svelte/motion";
  import { cubicInOut, cubicOut } from "svelte/easing";

  let darkGray = "#2F2F2F";
  let midGray = "#9A9A9A";
  let lightGray = "#e6e6e6";
  let errorRed = "#880000";

  export let transitionHeight;
  export let transitionWidth;

  let selectedText = "";
  let content = ``;
  let rootContent = "";
  let rootCount = 0;
  let rootDenominator = 0;

  let hintButtonOpacity = 0;
  let structuredData;
  export let gameCounter;

  let windowWidth = 0;

  const gameContentOpacity = new Tween(0, {
    duration: 1000,
    easing: cubicOut,
  });
  const gameHeight = new Tween(transitionHeight, {
    delay: 500,
    duration: 500,
    easing: cubicInOut,
  });
  const gameWidth = new Tween(transitionWidth, {
    duration: 500,
    easing: cubicInOut,
  });
  const sidePanelWidth = new Tween(0, {
    delay: 1000,
    duration: 500,
    easing: cubicInOut,
  });

  function setGameDimensions(width) {
    if (width >= 1200) {
      // large screens
      gameWidth.target = 400;
      gameHeight.target = 525;
    } else if (width >= 900) {
      // medium screens
      gameWidth.target = 400;
      gameHeight.target = 525;
    } else if (width >= 480) {
      // small screens
      gameWidth.target = 400;
      gameHeight.target = 525;
    } else {
      // mobile screens
      gameWidth.target = 320;
      gameHeight.target = 600;
    }
    sidePanelWidth.target = 10;
  }

  function handleResize() {
    windowWidth = window.innerWidth;
    setGameDimensions(windowWidth);
  }

  function animateParagraphWordsRandom(elementId, finalText, delay = 5) {
    const el = document.getElementById(elementId);
    const words = finalText.split(/(\s+)/); // split words but keep spaces
    el.innerHTML = ""; // clear paragraph first

    words.forEach((word, i) => {
      const span = document.createElement("span");
      span.textContent = word;

      // Skip animation for spaces
      if (word.trim() === "") {
        span.style.whiteSpace = "pre";
        span.style.display = "inline-block";
        el.appendChild(span);
        return;
      }

      const randomX = Math.floor(Math.random() * 60 - 30); // -15px to 15px
      const randomY = Math.floor(Math.random() * 60 - 30); // -15px to 15px

      span.style.opacity = 0;
      span.style.display = "inline-block";
      span.style.transition = "opacity 0.4s ease, transform 0.4s ease";
      span.style.transform = `translate(${randomX}px, ${randomY}px)`;

      el.appendChild(span);

      setTimeout(() => {
        span.style.opacity = 1;
        span.style.transform = "translate(0px, 0px)";
      }, i * delay);
    });
  }

  onMount(() => {
    if (gameCounter == 1) {
      setTimeout(() => {
        typeWriter("title", "ETYMOLOGY");
      }, 1000);
      setTimeout(() => {
        typeWriter("title", "");
      }, 2500);
      setTimeout(() => {
        gameContentOpacity.target = 1;

        setTimeout(() => {
          animateParagraphWordsRandom("highlighted-para", 'The gnome, capable and congenial, is alone in the immense hospice, impervious is the attenuation of agency. This innate fusion, this adult protagonist, added capacity. Essential is the essence of the command, the quintessential hospitality. There, this agnostic agent click, complete and agile, attended the hospitable agenda. The diagnosis is circumspect, the ignoble circumstance that demand attenuation. Capiche? The top gnome intend not abnegate the capacity of captivating, inciting hostility in the perfunctory agency of the industry. Circa the perennial diagnosis, the plebeian renegade performed the perfuse effusion of essence, the anagogical fusion of physiognomy and genealogy. The plebiscite inflict not confusion; the essence managed circumnavigating the perimeter of congenital antagonism. Adorned in the negligee of ignorance, the plebe manufactured the symmetry of the circumstance. Thereabout, that perfumed hostage diffused the hostility of effusive compliment. The perplexed gnome demanded cryogenic supply, piecemeal, capable of negotiating tender, refunds. The circumstance abated, agonized, confused the hospitality of the adult gnome, instantly. The protagonist atoned, permanently, presently. None ignored the circuit of the metronome, the circumference of isometric supply. Alone, not lonely, the left gnome is capable of the intrinsic introspect, that instant of perspective in the permanent interior. Invert the corner circumstance, yes, and the quintessential one of the introduction is increasingly impervious. Represent the gentile, the genteel, the gentry—yes, the gnome is indigenous of the genre.');
          content = `'The gnome, capable and congenial, is alone in the immense hospice, impervious is the attenuation of agency. This innate fusion, this adult protagonist, added capacity. Essential is the essence of the command, the quintessential hospitality. There, this agnostic agent click, complete and agile, attended the hospitable agenda. The diagnosis is circumspect, the ignoble circumstance that demand attenuation. Capiche? The top gnome intend not abnegate the capacity of captivating, inciting hostility in the perfunctory agency of the industry. Circa the perennial diagnosis, the plebeian renegade performed the perfuse effusion of essence, the anagogical fusion of physiognomy and genealogy. The plebiscite inflict not confusion; the essence managed circumnavigating the perimeter of congenital antagonism. Adorned in the negligee of ignorance, the plebe manufactured the symmetry of the circumstance. Thereabout, that perfumed hostage diffused the hostility of effusive compliment. The perplexed gnome demanded cryogenic supply, piecemeal, capable of negotiating tender, refunds. The circumstance abated, agonized, confused the hospitality of the adult gnome, instantly. The protagonist atoned, permanently, presently. None ignored the circuit of the metronome, the circumference of isometric supply. Alone, not lonely, the left gnome is capable of the intrinsic introspect, that instant of perspective in the permanent interior. Invert the corner circumstance, yes, and the quintessential one of the introduction is increasingly impervious. Represent the gentile, the genteel, the gentry—yes, the gnome is indigenous of the genre.'`
        }, 200);
        setTimeout(() => {
          typeWriter("game-title", "ETYMOLOGY");

        }, 400);
      }, 3500);

      setTimeout(() => {
        hintButtonOpacity = 1;
      }, 20000);
    }
    if (typeof window !== "undefined") {
      handleResize(); // set initial size
      window.addEventListener("resize", handleResize);
    }

    // get cognate data
    d3.csv("./cognates.csv").then(function (data) {
      let columns = Object.keys(data[0]); // Get column headers
      structuredData = { definition: {}, words: {} };

      columns.forEach((column) => {
        let values = data.map((row) => row[column]); // Extract column values
        structuredData.definition[column] = values.shift(); // Remove first value and store it separately
        structuredData.words[column] = values.filter(
          (str) => str.trim().toLowerCase() !== "",
        ); // Store the rest in columns
      });

      rootDenominator = Object.keys(structuredData.definition).length;
    });
  });

  // Variable to hold the dynamically updated content with highlighted text
  let highlightedContent = content;

  // Detect the selected text when the mouse is released
  function highlightSelectedText() {
    const selection = window.getSelection();
    if (!selection.rangeCount) return;

    const range = selection.getRangeAt(0);
    const container = document.querySelector("#highlighted-para");

    if (!container.contains(range.commonAncestorContainer)) {
      // Selection is outside the allowed area, so clear it
      selection.removeAllRanges();
    }
    highlightedContent = getHighlightedContent(selection?.toString()); // Update the highlighted content
  }

  // Replace the content with highlighted text
  function getHighlightedContent(selectedWords) {
    // if (!selectedWords) {
    //   return content.replace(/<span class="highlighted">(.*?)<\/span>/gi, "$1");
    // }

    // Split the input string into individual words
    let wordsToHighlight = selectedWords
      .replace(/[^\w\s]|_/g, "")
      .replace(/\s+/g, " ")
      .split(" ")
      .map((word) => word.trim())
      .filter(Boolean);
    let allCognates = [];
    let allRoots = [];

    // Find cognates for each word and collect them
    wordsToHighlight.forEach((word) => {
      let cognatesAndKey = findCognates(word);
      if (cognatesAndKey.length > 0) {
        allCognates = allCognates.concat(cognatesAndKey[1]); // Add matching words to list
        allRoots = allRoots.concat(cognatesAndKey[0]);
      }
    });

    let uniqueRoots = [...new Set(allRoots)];
    let formatted = "";
    rootCount = uniqueRoots.length;

    uniqueRoots.forEach((root) => {
      let def = structuredData.definition[root];
      formatted =
        formatted +
        `<div class="root-def"><span class='bold-root'>${root.toUpperCase()}</span><br><span class='root-def-text'>${def.toUpperCase()}</span></div>`;
    });

    // roots
    rootContent = formatted;

    // If no cognates were found, return original content
    if (allCognates.length === 0) {
      return content.replace(/<span class="highlighted">(.*?)<\/span>/gi, "$1");
    }

    // Create a regex pattern to match any of the cognates/keywords
    const regex = new RegExp(`\\b(${allCognates.join("|")})\\b`, "gi");

    // Highlight the matched words
    return content
      .replace(
        selectedWords,
        `<span class="highlighted">${selectedWords}</span>`,
      )
      .replace(regex, (match) => `<span class="highlighted">${match}</span>`);
  }

  function winCondition() {
    setTimeout(() => {
      gameContentOpacity.target = 0;
    }, 0);
    setTimeout(() => {
      transitionHeight = gameHeight.target;
      transitionWidth = gameWidth.target;
      gameCounter = 2;
    }, 1000);
  }

  // Find cognates for a given word
  function findCognates(word) {
    // Search in structuredData to find cognates
    for (let key in structuredData.words) {
      if (structuredData.words[key].includes(word.toLowerCase())) {
        return [key, structuredData.words[key]]; // Return the key and all matching words
      }
    }
    return []; // Return an empty array if no cognates are found
  }

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
  let hintCount = 0;
  let hintsLeft = 2;

  async function hintButton() {
    if (isRunning) return; // prevent overlapping calls
    isRunning = true;
    if (hintCount == 0) {
      typeWriter("hint", "WHAT WORDS AREN'T BEING HIGHLIGHTED?");
      hintsLeft = 1;
      hintCount++;
    } else if (hintCount == 1) {
      typeWriter(
        "hint",
        "IS THERE A MESSAGE IN THE UNHIGHLIGHTED WORDS?",
      );
      hintsLeft = 0;
      hintCount = 0;
    }
  }

  onDestroy(() => {
    if (typeof window !== "undefined") {
      window.removeEventListener("resize", handleResize);
    }
  });
</script>

<div class="page-container-1">
  <div
    class="game-words-container"
    style="--dark-gray: {darkGray}; --mid-gray: {midGray}; --light-gray: {lightGray}; --error-red: {errorRed}"
  >
    <div></div>
    <div
      class="game-container-1"
      style=" height: {gameHeight.current + 'px'}; width: {gameWidth.current +
        'px'};"
    >
      <div class="game-content-1" style="opacity:{gameContentOpacity.current}">
        <div class="header-container">
          <div id="game-title"></div>
          <div class="counter">
            <span bind:innerHTML={rootCount} contenteditable="false"
            ></span>/<span
              bind:innerHTML={rootDenominator}
              contenteditable="false"
            ></span>
          </div>

          <div class="tooltip-container" style="opacity: {hintButtonOpacity}">
            <div class="hint-button" on:click={hintButton}>
              <span>(?)</span> <span style="font-size:10px;">{hintsLeft}</span>
            </div>
            <span class="tooltip-text">Use a hint! I won't judge you...</span>
          </div>
        </div>
        <div id="hint"></div>

        <div contenteditable="false">
          <p>
            {#if selectedText}
              <strong>Highlighted word: {selectedText}</strong>
            {/if}
          </p>
          <p
            id="highlighted-para"
            on:mouseup={highlightSelectedText}
            bind:innerHTML={highlightedContent}
            contenteditable="false"
          ></p>
        </div>
      </div>
    </div>
    <div
      class="roots"
      bind:innerHTML={rootContent}
      contenteditable="false"
      style="opacity:{gameContentOpacity.current}; width: {sidePanelWidth}vw"
    ></div>
  </div>
</div>
<div id="title"></div>
{#if gameCounter === 1}
  <div class="win-condition" on:click={winCondition}></div>
{/if}

<style>
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

  .counter {
    font-family: "ROMMONO";
    font-size: 10px;
    justify-self: center;
    grid-column: 2;
    letter-spacing: 1px;
    color: var(--dark-gray);
    user-select: none;
  }

  .page-container-1 {
    display: flex;
    width: 100vw;
    height: 100vh;
    position: absolute;
    opacity: 1;
    justify-content: center;
  }

  #highlighted-para {
    color: var(--dark-gray);
  }

  .win-condition {
    position: absolute;
    width: 10vw;
    height: 10vh;
    z-index: 1;
    cursor: pointer;
  }

  .game-words-container {
    display: grid;
    grid-template-columns: 1fr auto 1fr; /* Center column auto-sized */
    gap: 20px; /* Adjust spacing as needed */
  }

  .roots {
    align-self: center;
    max-height: 70vh;
    color: var(--mid-gray);
    font-size: small;
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    user-select: none;
    font-family: 'ROMMONO';
    font-size: 10px;
  }

  :global(.root-def) {
    padding-top: 1em;
    padding-right: 1em;
  }

  :global(.bold-root) {
    font-weight: bold;
  }

  .game-container-1 {
    flex-direction: column;
    align-items: center;
    width: 40vw;
    height: 80vh;
    background-color: var(--mid-gray);
    border-radius: 0.75em;
    margin: auto;
    padding: 3em;
  }
  @media (max-width: 480px) {
    .game-container-1 {
      padding: 2em;
    }
  }

  /* Custom styles for the selection */
  ::selection {
    background-color: var(--light-gray);
  }

  /* Highlighted word style */
  :global(.highlighted) {
    background-color: var(--light-gray);
    padding-bottom: 0.05em;
    margin-bottom: -0.05em;
    box-shadow: 0 0 8px var(--light-gray);
    /* -webkit-filter: drop-shadow(0px 0px 4px var(--light-gray)); */
  }

  .header-container {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  position: relative;
}

#game-title {
  justify-self: start;
}

  .hint-button {
    color: var(--dark-gray);
    /* border: solid 1px var(--dark-gray); */
    border-radius: 100px;
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
    justify-self: end;
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

  .tooltip-container:hover .tooltip-text {
    visibility: visible;
    opacity: 1;
  }

  #hint {
    padding-top: .5em;
    margin-left: auto;
    width: 70%;
    height: 3.5em;
    text-align: right;
    font-weight: bold;
    color: var(--error-red);
    transition: opacity 1s ease-in-out; /* Animation duration and effect */
  }
  /* @media (max-width: 480px) {
    #hint {
      height: 1em;
      padding-bottom: 1em;
    }
  } */
</style>
