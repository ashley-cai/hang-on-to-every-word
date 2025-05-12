<script>
    import { onMount } from "svelte";
    import ScatterPlot from "./ScatterPlot.svelte";
    import DragAndDrop from "./DragAndDrop.svelte";
    import CartPage from "./CartPage.svelte";
    import ParagraphHighlight from "./ParagraphHighlight.svelte";
    import VennDiagram from "./VennDiagram.svelte";
    import ConnectTheDots from "./ConnectTheDots.svelte";
    import Map from "./Map.svelte";
    import FinalGame from "./FinalGame.svelte";

    let gameCounter = 2;
    let transitionHeight = 0;
    let transitionWidth = 0;

    let darkGray = "#1c1c1c";
    let midGray = "#8e8d8c";
    let lightGray = "#e6e6e6";
    let errorRed = "#880000";
    let correctGreen = "#E8FFB7";
</script>

<div
    style="--dark-gray: {darkGray}; --mid-gray: {midGray}; --light-gray: {lightGray}; --correct-green: {correctGreen}; "
>
{#if gameCounter === 0}
    <CartPage bind:gameCounter bind:transitionHeight bind:transitionWidth></CartPage>
{:else if gameCounter === 1}
    <ParagraphHighlight bind:gameCounter bind:transitionHeight bind:transitionWidth></ParagraphHighlight>
{:else if gameCounter === 2}
    <Map bind:gameCounter bind:transitionHeight bind:transitionWidth></Map>
{:else if gameCounter === 3}
    <ConnectTheDots bind:gameCounter bind:transitionHeight bind:transitionWidth></ConnectTheDots>
{:else if gameCounter === 4}
    <VennDiagram bind:gameCounter bind:transitionHeight bind:transitionWidth></VennDiagram>
{:else if gameCounter === 5}
    <ScatterPlot bind:gameCounter bind:transitionHeight bind:transitionWidth></ScatterPlot>
{:else if gameCounter === 6}
    <FinalGame bind:gameCounter bind:transitionHeight bind:transitionWidth></FinalGame>
{/if}
</div>

<style>

@font-face {
        font-family: "ArialNarrow";
        font-style: normal;
        font-weight: 300;
        src: url("/fonts/arialnarrow.ttf"); /* IE9 Compat Modes */
    }
@font-face {
        font-family: "ROMMONO";
        font-style: normal;
        font-weight: 400;
        src: url("/fonts/ABCROMMono-Regular-Trial.otf"); /* IE9 Compat Modes */
    }
    :global(html) {
        background-color: #111111;
        font-family: Helvetica, sans-serif;
        font-size: 12px;
    }

    :global(#title) {
        font-family: "ROMMONO";
        color: var(--dark-gray);

    }

    :global(#instructions) {
        font-family: "ROMMONO";
        color: var(--dark-gray);
        font-size: 10px;
        letter-spacing: 1px;

    }

    :global(#hint) {
        font-family: "ROMMONO";
        font-size: 10px;
        letter-spacing: 1px;

    }
    :global(#game-title) {
        font-family: "ROMMONO";
        font-size: 10px;
        letter-spacing: 1px;
    }

    :global(.hint-button) {
        font-family: "ROMMONO";
        font-size: 10px;
        letter-spacing: 1px;
    }

    :global(.tooltip-text) {
        font-family: "ROMMONO";
        font-size: 10px;
        letter-spacing: 1px;
    }

    :global(.hint-button > *) {
        font-family: "ROMMONO";
        font-size: 10px;
        letter-spacing: 1px;
    }

</style>
