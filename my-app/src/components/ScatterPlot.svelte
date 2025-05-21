<script>
  import { onMount } from "svelte";
  import * as d3 from "d3";
  import { Tween } from "svelte/motion";
  import { cubicOut } from "svelte/easing";
  import { tick } from "svelte";

  let darkGray = "#1c1c1c";
  let midGray = "#8e8d8c";
  let lightGray = "#e6e6e6";
  let errorRed = "#880000";
  let correctGreen = "#E8FFB7";

  export let gameCounter;
  export let transitionHeight;
  export let transitionWidth;

  let windowWidth = 0;
  let gameStart = "";
  const gameContentOpacity = new Tween(0, {
    duration: 1000,
    easing: cubicOut,
  });

  let hintsLeft = 2;
  let hintButtonOpacity = 0;
  let hintButton;

  const gameContainerHeight = new Tween(transitionHeight, {
    duration: 500,
    easing: cubicOut,
  });
  const gameContainerWidth = new Tween(transitionWidth, {
    delay: 500,
    duration: 500,
    easing: cubicOut,
  });

  let svg;
  let width = 500;
  let height = 500;

  const margin = { top: 40, right: 40, bottom: 40, left: 40 };

  function setGameDimensions(wWidth) {
    if (wWidth >= 1200) {
      // large screens
      gameContainerHeight.target = 650;
      gameContainerWidth.target = 700;
    } else if (wWidth >= 900) {
      // medium screens
      gameContainerHeight.target = 700;
      gameContainerWidth.target = 800;
    } else if (wWidth >= 480) {
      // small screens
      gameContainerHeight.target = 700;
      gameContainerWidth.target = 480;
      width = 400;
    } else {
      // mobile screens
      gameContainerHeight.target = 600;
      gameContainerWidth.target = 350;
      height = 450;
      width = 300;
    }
  }

  function handleResize() {
    windowWidth = window.innerWidth;
    setGameDimensions(windowWidth);
  }

  // Set up the D3 chart on mount
  onMount(async () => {
    if (gameCounter == 5) {
      gameStart = "display: flex;";
      setTimeout(() => {
        typeWriter("title", "SYNONYM", 70);
      }, 1000);
      setTimeout(() => {
        typeWriter("title", "", 70);
      }, 2500);
      setTimeout(() => {
        gameContentOpacity.target = 1;
        typeWriter("noun", "NOUN");
        typeWriter("adjective", "ADJECTIVE");
        typeWriter("short", "SHORT");
        typeWriter("long", "LONG");
      }, 3000);
      setTimeout(() => {
        typeWriter("instructions", "HEAT OVER MEDIUM. (4)");
        typeWriter("game-title", "6:SYNONYM");


      }, 4000);
      setTimeout(() => {
        hintButtonOpacity = 1;
      }, 10000);
    }

    if (typeof window !== "undefined") {
      handleResize(); // wait one tick
      await tick();
      window.addEventListener("resize", handleResize);
    }

    const minX = margin.left;
    const maxX = width - margin.right;
    const minY = height - margin.bottom;
    const maxY = margin.top;

    // Define the scale for the axes
    const xScale = d3.scaleLinear().domain([-10, 10]).range([minX, maxX]);
    const yScale = d3.scaleLinear().domain([-10, 10]).range([minY, maxY]);

    let currentWords = ["", "", "", ""];
    let correctWords = ["EXTRA", "VIRGIN", "OLIVE", "OIL"];

    let quadrants1 = [
      ["new", "other", "unused", "additional", "ancillary", "supplemental"],
      ["extra", "further", "added", "special", "extraneous", "auxiliary"],
      ["tip", "more", "surplus", "optional", "needless", "supernumerary"],
      ["perk", "spare", "leftover", "adjunct", "accessory", "appendix"],
      ["plus", "reserve", "excess", "adornment", "complement", "extension"],
      ["bonus", "addition", "affix", "attachment", "appendage", "addendum"],
    ];

    let quadrants2 = [
      ["pure", "fresh", "clean", "sexless", "unsullied", "stainless"],
      ["first", "chaste", "vestal", "heatless", "undefiled", "unspoiled"],
      ["neat", "single", "prudish", "wholesome", "virtuous", "continent"],
      ["monk", "lady", "virgin", "virgin", "monastic", "abstinence"],
      ["monk", "lady", "ascetic", "ascetic", "celibate", "abstinence"],
      ["nun", "nun", "maiden", "maiden", "celibate", "anchorite"],
    ];

    let quadrants3 = [
      ["green", "tan", "camo", "military", "blue-green", "yellow-green"],
      ["sea", "sage", "pine", "tawny", "viridian", "chartreuse"],
      ["pea", "beryl", "sage", "kelly", "emerald", "peacock"],
      ["moss", "lime", "olive", "forest", "vegetable", "aquamarine"],
      ["jade", "drupe", "drupe", "snack", "vegetable", "stone fruit"],
      ["fruit", "fruit", "Olea", "Olea", "pickle", "appetizer"],
    ];

    let quadrants4 = [
      ["Wet", "slimy", "glossy", "shiny", "slippery", "lustrous"],
      ["Slick", "smooth", "Greasy", "Polished", "fatty", "adipose"],
      ["Art", "balm", "Butter", "Spread", "sleek", "anointed"],
      ["Wax", "rich", "tallow", "Lotion", "Lubricant", "Shortening"],
      ["Oil", "Ghee", "petrol", "Fresco", "Canvas", "Margarine"],
      ["Lard", "Lube", "Picture", "Painting", "Pomade", "butyraceous"],
    ];

    const xScaleWord = d3
      .scaleLinear()
      .domain([minX, maxX])
      .range([0, quadrants1.length - 1]);
    const yScaleWord = d3
      .scaleLinear()
      .domain([minY, maxY])
      .range([quadrants1.length - 1, 0]);

    // Data for points (could be reactive later)
    let points = [
      { id: 1, x: 3, y: 4, cx: -10, cy: 5 },
      { id: 2, x: -4, y: -7, cx: -3, cy: -1 },
      { id: 3, x: -10, y: 9, cx: -1, cy: -3 },
      { id: 4, x: 7, y: 9, cx: -10, cy: -6 },
    ];

    //gradient set for hint2
    function hex(c) {
      var s = "0123456789abcdef";
      var i = parseInt(c);

      if (i == 0 || isNaN(c)) return "00";

      i = Math.round(Math.min(Math.max(0, i), 255));
      return s.charAt((i - (i % 16)) / 16) + s.charAt(i % 16);
    }

    /* Convert an RGB triplet to a hex string */
    function convertToHex(rgb) {
      return hex(rgb[0]) + hex(rgb[1]) + hex(rgb[2]);
    }

    /* Remove '#' in color hex string */
    function trim(s) {
      return s.charAt(0) == "#" ? s.substring(1, 7) : s;
    }

    /* Convert a hex string to an RGB triplet */
    function convertToRGB(hex) {
      var color = [];
      color[0] = parseInt(trim(hex).substring(0, 2), 16);
      color[1] = parseInt(trim(hex).substring(2, 4), 16);
      color[2] = parseInt(trim(hex).substring(4, 6), 16);
      return color;
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

    function generateColor(colorStart, colorEnd, colorCount) {
      // The beginning of your gradient
      var start = convertToRGB(colorStart);

      // The end of your gradient
      var end = convertToRGB(colorEnd);

      // The number of colors to compute
      var len = colorCount;

      //Alpha blending amount
      var alpha = 0.0;

      var saida = [];

      for (let i = 0; i < len; i++) {
        var c = [];
        alpha += 1.0 / len;

        c[0] = start[0] * alpha + (1 - alpha) * end[0];
        c[1] = start[1] * alpha + (1 - alpha) * end[1];
        c[2] = start[2] * alpha + (1 - alpha) * end[2];

        saida.push(convertToHex(c));
      }

      return saida;
    }

    // Usage example
    let hintGradient = generateColor(errorRed, lightGray, 30);
    let hint2 = false;

    const svgElement = d3.select(svg);

    svgElement.append("defs").html(`
  <filter id="glow" x="-50%" y="-50%" width="250%" height="250%">
    <feGaussianBlur stdDeviation="3" result="blur" />
    <feMerge>
      <feMergeNode in="blur" />
      <feMergeNode in="SourceGraphic" />
    </feMerge>
  </filter>
`);

    // Create axes
    const xAxis = d3.axisBottom(xScale).ticks(5).tickValues([]).tickSize(0);
    const yAxis = d3.axisLeft(yScale).ticks(5).tickValues([]).tickSize(0);

    // Append axes to SVG
    const xAxisGroup = svgElement
      .append("g")
      .attr("transform", `translate(0, ${yScale(0)})`)
      .call(xAxis);

    // Animate the axis path
    xAxisGroup.selectAll("path").each(function () {
      const path = d3.select(this);
      const totalLength = this.getTotalLength();
      path
        .attr("stroke", darkGray)
        .attr("stroke-width", 1)
        .attr("fill", "none")
        .attr("stroke-dasharray", totalLength)
        .attr("stroke-dashoffset", totalLength)
        .transition()
        .delay(3500)
        .duration(1000)
        .ease(d3.easeCubicOut)
        .attr("stroke-dashoffset", 0);
    });

    const yAxisGroup = svgElement
      .append("g")
      .attr("transform", `translate(${xScale(0)}, 0)`)
      .call(yAxis);

    yAxisGroup.selectAll("path").each(function () {
      const path = d3.select(this);
      const totalLength = this.getTotalLength();
      path
        .attr("stroke", darkGray)
        .attr("stroke-width", 1)
        .attr("fill", "none")
        .attr("stroke-dasharray", totalLength)
        .attr("stroke-dashoffset", totalLength)
        .transition()
        .delay(3000)
        .duration(1000)
        .ease(d3.easeCubicOut)
        .attr("stroke-dashoffset", 0);
    });

    // Add axis labels
    svgElement
      .append("text")
      .attr("x", width / 2 - 14)
      .attr("y", height - 22)
      .attr("class", "axis-label")
      .attr("fill", darkGray)
      .attr("font-size", 10)
      .attr("font-family", "ROMMONO")
      .attr("letter-spacing", 1)
      .attr("id", "noun")
      // .text("");

    svgElement
      .append("text")
      .attr("x", width / 2 - 30)
      .attr("y", 30)
      .attr("class", "axis-label")
      .attr("fill", darkGray)
      .attr("font-size", 10)
      .attr("font-family", "ROMMONO")
      .attr("letter-spacing", 1)
      .attr("id", "adjective")

    svgElement
      .append("text")
      .attr("x", -4)
      .attr("y", height / 2 + 4)
      .attr("class", "axis-label")
      .attr("fill", darkGray)
      .attr("font-size", 10)
      .attr("font-family", "ROMMONO")
      .attr("letter-spacing", 1)
      .attr("id", "short")

    svgElement
      .append("text")
      .attr("x", width - 30)
      .attr("y", height / 2 + 4)
      .attr("class", "axis-label")
      .attr("fill", darkGray)
      .attr("font-family", "ROMMONO")
      .attr("font-size", 10)
      .attr("letter-spacing", 1)
      .attr("id", "long")

    // Set up drag behavior
    let dragOffset = { x: 0, y: 0 };

const drag = d3
  .drag()
  .on("start", function (event, d) {
    const [initialX, initialY] = d3.select(this)
      .attr("transform")
      .match(/translate\(([^,]+),([^)]+)\)/)
      .slice(1, 3)
      .map(Number);

    dragOffset.x = event.x - initialX;
    dragOffset.y = event.y - initialY;
  })
  .on("drag", function (event, d) {
    const correctedX = event.x - dragOffset.x;
    const correctedY = event.y - dragOffset.y;

    d.x = Math.max(-10, Math.min(10, xScale.invert(correctedX)));
    d.y = Math.max(-10, Math.min(10, yScale.invert(correctedY)));

    d3.select(this)
      .attr("transform", `translate(${xScale(d.x)},${yScale(d.y)})`);

    d3.select(this)
      .select("text")
      .text(determineText(d.x, d.y, d.id).toUpperCase());

    if (hint2) {
      const color = determineColor(d.x, d.y, d.id, d.cx, d.cy);
      d3.select(this)
        .select("circle")
        .attr("fill", color)
        .attr("filter", "url(#glow)")
      }

    if (areArraysEqual(currentWords, correctWords)) {
      d3.selectAll(".label-text")
        .transition()
        .delay(500)
        .duration(1000)
        .attr("fill", correctGreen);

      d3.selectAll(".scatter-point")
        .transition()
        .delay(500)
        .duration(1000)
        .attr("fill", correctGreen);

      setTimeout(() => {
        gameContentOpacity.target = 0;
      }, 2000);

      setTimeout(() => {
        transitionHeight = gameContainerHeight.target;
        transitionWidth = gameContainerWidth.target;
        gameCounter = 6;
      }, 3000);
    }
  });



    function determineText(x, y, id) {
      if (id == 1) {
        currentWords[id - 1] =
          quadrants1[Math.round(yScaleWord(yScale(y)))][
            Math.round(xScaleWord(xScale(x)))
          ];
        return currentWords[id - 1];
      } else if (id == 2) {
        currentWords[id - 1] =
          quadrants2[Math.round(yScaleWord(yScale(y)))][
            Math.round(xScaleWord(xScale(x)))
          ];
        return currentWords[id - 1];
      } else if (id == 3) {
        currentWords[id - 1] =
          quadrants3[Math.round(yScaleWord(yScale(y)))][
            Math.round(xScaleWord(xScale(x)))
          ];
        return currentWords[id - 1];
      } else {
        currentWords[id - 1] =
          quadrants4[Math.round(yScaleWord(yScale(y)))][
            Math.round(xScaleWord(xScale(x)))
          ];
        return currentWords[id - 1];
      }
    }

    function determineColor(x, y, id, cx, cy) {
      return "#" + hintGradient[Math.round(calculateDistance(x, y, cx, cy))];
    }

    //euclidean distance
    function calculateDistance(x1, y1, x2, y2) {
      const dx = x2 - x1;
      const dy = y2 - y1;
      const distance = Math.sqrt(dx * dx + dy * dy);
      return distance;
    }

    /* Define the data for the circles */
    var elem = svgElement.selectAll("circle").data(points);

    /*Create and place the "blocks" containing the circle and the text */
    var elemEnter = elem
      .enter()
      .append("g")
      .attr("transform", function (d) {
        return `translate(${xScale(d.x)},${yScale(d.y)})`;
      })
      .call(drag);

    /*Create the circle for each block */
    var circle = elemEnter
  .append("circle")
  .attr("class", "scatter-point")
  .attr("r", 0)
  .attr("stroke", "transparent")
  .attr("fill", lightGray)
  .attr("stroke-width", 50)
  .attr("filter", "url(#glow)");

circle
  .transition()
  .delay((_, i) => 3000 + i * 100)
  .duration(300)
  .ease(d3.easeCubicOut)
  .attr("r", 7)
  .transition()
  .duration(200)
  .ease(d3.easeCubicOut)
  .attr("r", 5);

    /* Create the text for each block */
    elemEnter
  .append("text")
  .attr("class", "label-text")
  .attr("dy", -16)
  .attr("text-anchor", "middle")
  .attr("fill", lightGray)
  .attr("filter", "url(#glow)")
  .style("opacity", 0) // start hidden
  .text((d) => determineText(d.x, d.y, d.id).toUpperCase())
  .transition()
  .delay((_, i) => 3000 + i * 100)
  .duration(600)
  .ease(d3.easeCubicOut)
  .style("opacity", 1); // fade in

    let hintCount = 0;
    hintButton = function () {
      if (hintCount == 0) {
        circle.transition().duration(2000).attr("r", 10);

        elemEnter
          .append("text")
          .attr("dy", function (d) {
            return 4;
          })
          .attr("text-anchor", "middle")
          .attr("font-size", "10px")
          .attr("font-weight", "bold")
          .attr("class", "circle-numbers")
          .attr("fill", darkGray)
          .text(function (d) {
            return d.id;
          })
          .attr("opacity", 0)
          .transition()
          .duration(2000)
          .attr("opacity", 1);
        hintCount++;
        hintsLeft = 1;
      } else if (hintCount == 1) {
        let color = "";
        circle
          .transition()
          .duration(2000)
          .attr("fill", function (d) {
            color = determineColor(d.x, d.y, d.id, d.cx, d.cy);
            return color;
            // return lightGray;
          })
          .attr("filter", "url(#glow)")

        hint2 = true;
        hintsLeft = 0;
      }
    };

    function areArraysEqual(arr1, arr2) {
      // First check if lengths are different
      if (arr1.length !== arr2.length) {
        return false;
      }

      // Compare each element in the arrays
      for (let i = 0; i < arr1.length; i++) {
        if (arr1[i].toUpperCase() !== arr2[i]) {
          return false; // Return false if any element is different
        }
      }

      // If we get here, the arrays are equal
      return true;
    }
  });
</script>

<div class="page-container-2" style={gameStart}>
  <div
    class="game-container"
    style="--dark-gray: {darkGray}; --mid-gray: {midGray}; --light-gray: {lightGray}; width:{gameContainerWidth.current +
      'px'}; height:{gameContainerHeight.current + 'px'};"
  >
  <div class="game-contents" style="opacity: {gameContentOpacity.current}">
    <div class="instructions-container">
      <div id="game-title"></div>
      <div id="instructions"></div>
      <div class="tooltip-container" style="opacity: {hintButtonOpacity}">
        <div class="hint-button" on:click={hintButton}>
          <span>(?)</span> <span style="font-size:10px;">{hintsLeft}</span>
        </div>
        <span class="tooltip-text">USE A HINT! MIGHT AS WELL...</span>
      </div>
    </div>
      <div class="scatterplot-container">
        <svg bind:this={svg} {width} {height} overflow="visible" style="touch-action: none;"></svg>
      </div>
    </div>
  </div>
</div>
<div id="title"></div>

<style>
  .page-container-2 {
    width: 100vw;
    height: 100dvh;
    position: absolute;
    display: none;
    justify-content: center;
    display: none;
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

  #game-title {
    color: var(--dark-gray);
    justify-self: start;
  }

  .game-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: var(--mid-gray);
    border-radius: 0.75em;
    margin: auto;
    padding: 3em;
  }

  .game-contents {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  #instructions {
    font-weight: 400;
    color: var(--dark-gray);
  }

  .instructions-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    padding-bottom: 4em;
  }
  @media (max-width: 900px) {
    .instructions-container {
      padding-bottom: 3em;
    }
  }
  @media (max-width: 480px) {
    .instructions-container {
      padding-bottom: 3em;
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

  :global(.scatter-point) {
    cursor: grab;
    transition: filter 0.3s ease-in-out; /* Animation duration and effect */
  }

  :global(.circle-numbers) {
    cursor: grab;
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
    /* top: 100%; */
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

  .axis-label {
  }
  @media (max-width: 900px) {
    .axis-label {
      font-size: smaller;
    }
  }
  @media (max-width: 480px) {
    .axis-label {
      font-size: small;
    }
  }
</style>
