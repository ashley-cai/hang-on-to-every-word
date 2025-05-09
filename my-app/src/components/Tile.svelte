<script>
  import { onMount } from 'svelte';

  export let word;
  export let correct = "";
  export let shouldBounce = false;
  export let index = 0; // index for delay
    export let hidden = false;
    export let bounceOut = false;

  let tileOpacity;

  let applyBounce = false;
  let delay = 0;

  if (shouldBounce) {
    tileOpacity = 0;
  } else {
    tileOpacity = 1;
  }

  onMount(() => {
    if (shouldBounce) {
      delay = index * 100; // 100ms stagger per index
      setTimeout(() => {
        applyBounce = true;
        setTimeout(() => {
          shouldBounce = false;
          applyBounce = false;
          tileOpacity = 1;
        }, 600); // match animation duration
      }, delay);
    }
  });

  let darkGray = "#1c1c1c";
  let midGray = "#8e8d8c";
  let lightGray = "#e6e6e6";
  let errorRed = "#880000";
  let correctGreen = "#E8FFB7";
</script>


<div
class="square {correct} {applyBounce ? 'bounce-in' : ''} {bounceOut ? 'bounce-out' : ''}"
style="
    --dark-gray: {darkGray};
    --mid-gray: {midGray};
    --light-gray: {lightGray};
    --correct-green: {correctGreen};
    opacity: {tileOpacity};
    visibility: {hidden ? 'hidden' : 'visible'};
  "
>
  <div class="letter no-select">
    {word.toUpperCase()}
  </div>
</div>

<style>
  .square {
    height: 2em;
    padding-left: 1em;
    padding-right: 1em;
    border-radius: calc(min(4vmin, 40px));
    cursor: grab;
    display: flex;
    user-select: none;
    align-items: center;
    justify-content: center;
    background-color: var(--light-gray);
    max-width: fit-content;
    z-index: 1;
    box-shadow: 0px 0px 8px 1.5px var(--light-gray);
    transition:
      background-color 1s ease-in-out,
      box-shadow 1s ease-in-out,
      opacity 1s 1s ease-in-out;
  }
  @media (max-width: 480px) {
    .square {
    padding-left: .75em;
    padding-right: .75em;
		}
	}

  .square:active{
    outline: none;
  }

  .square:focus {
    outline: none;
    opacity: 1 !important;

  }

  .letter {
    font-size: 0.9em;
    color: var(--dark-gray);
  }

  .square.correct {
    background-color: var(--correct-green);
    box-shadow: 0px 0px 8px 1.5px var(--correct-green);
    opacity: 0;
    animation: 1.5s 1s bounceOut
  }

  @keyframes bounceIn {
    0% {
      transform: scale(0.3);
      opacity: 0;
    }
    50% {
      transform: scale(0.9);
      opacity: 1;
    }
    70% {
      transform: scale(1.05);
      opacity: 1;
    }
    100% {
      transform: scale(1);
      opacity: 1;

    }
  }

  @keyframes bounceOut {
    100% {
      transform: scale(0.3);
      opacity: 0;
    }
    70% {
      transform: scale(1.05);
      opacity: 1;
    }
    50% {
      transform: scale(0.9);
      opacity: 1;
    }
    0% {
      transform: scale(1);
      opacity: 1;

    }
  }

  .bounce-in {
    animation: bounceIn 0.6s ease forwards;
  }
  .bounce-out {
  animation: bounceOut 0.6s ease forwards;
}
</style>
