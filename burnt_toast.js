// All credits go to Jordan Lerner
// This project is licensed under MIT
//
// https://github.com/J-Lerner/burnt_toast.js
//

(function () {
  let plateCSS = `
      margin: 2vw;
      background-color: darkslategray;
      height: 10vh;
      width: 25vh;
    `;
  let buttonColor = "gray";
  let buttonHoverColor = "lightgray";
  let buttonActiveColor = "darkgray";
  let isProgressBarTop = false;
  let progressContainerColor = "darkgray";
  let progressBarColor = "lightgray";
  let titleCSS = `
      color: white;
    `;

  function setPlateParams(width, height, margin, color) {
    plateCSS = `
        margin: ${margin};
        background-color: ${color};
        height: ${height}vh;
        width: ${width}vw;
      `;
  }

  function setButtonColors(backgroundColor, hoverColor, activeColor) {
    buttonColor = backgroundColor;
    buttonHoverColor = hoverColor;
    buttonActiveColor = activeColor;
  }

  function setIsProgressBarTop(bool) {
    isProgressBarTop = bool;
  }

  function setTitleCSS(css) {
    titleCSS = css;
  }

  function setProgressBarColors(backgroundColor, color) {
    progressBarColor = color;
    progressContainerColor = backgroundColor;
  }

  function applyBurntToastStyles() {
    // Create a <style> element
    const style = document.createElement("style");

    // Define the CSS styles as a string
    const css = `
        @keyframes load {
            from { width: 0% }
            to { width: 100% }
        }

        #--burnt-toast-cover {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            user-select: none;
            pointer-events: none;
        }

        .--burnt-toast-plate {
            position: absolute;
            top: 0;
            right: -100vw;

            border-radius: 1vh;
            box-shadow: 0 0 6px 1px black;
            pointer-events: visible;

            overflow: hidden;
            transition: 1s;

            ${plateCSS};
        }

        .--burnt-toast-button {
            position: absolute;
            height: 3vh;
            aspect-ratio: 1;
            top: ${!isProgressBarTop ? "0" : "auto"};
            bottom: ${isProgressBarTop ? "0" : "auto"};
            right: 0;
            margin: 0.5vh;
            cursor: pointer;

            display: flex;
            justify-content: center;
            align-items: center;

            background-color: ${buttonColor};

            border-radius: 1vh;
            transition: 350ms;
        }

        .--burnt-toast-text {
            ${titleCSS}
        }

        .--burnt-toast-button:hover {
            margin: 0.4vh;
            height: 3.2vh;
            background-color: ${buttonHoverColor};
        }

        .--burnt-toast-button:active {
            margin: 0.58vh;
            height: 2.7vh;
            background-color: ${buttonActiveColor};
        }

        .--burnt-toast-button-text {
            font-size: 2vh;
        }

        .--burnt-toast-progress-container {
            position: absolute;
            top: ${isProgressBarTop ? "0" : "auto"};
            bottom: ${!isProgressBarTop ? "0" : "auto"};
            left: 0;

            height: 0.75vh;
            width: 25vh;
            border-radius: 1vh;

            background-color: ${progressContainerColor};
            z-index: 4;
        }

        .--burnt-toast-progress-bar {
            position: absolute;
            top: 0
            left: 0;

            height: 100%;
            width: 10%;
            border-radius: 1vh;

            background-color: ${progressBarColor};
            z-index: 5;
            animation-timing-function: linear;
        }
    `;

    // Set the CSS text inside the style element
    style.appendChild(document.createTextNode(css));

    // Append the style element to the head of the document
    document.head.appendChild(style);
  }

  cover = document.querySelector("NULL");

  visibleToasts = [false, false, false, false, false, false];

  function sendTimedToast(text, toastVisibilityTime) {
    const newToast = buildToast(text, true);
    newToast.querySelector(".--burnt-toast-progress-bar").style.animationName =
      "load";
    newToast.querySelector(
      ".--burnt-toast-progress-bar",
    ).style.animationDuration = toastVisibilityTime / 1000 + 1 + "s";

    setTimeout(() => {
      newToast.style.right = "0vw";
    }, 10);

    setTimeout(() => {
      closeToast(newToast);
    }, toastVisibilityTime + 1000);
  }

  function sendToast(text) {
    const newToast = buildToast(text, false);

    setTimeout(() => {
      newToast.style.right = "0vw";
    }, 10);
  }

  function closeToast(el) {
    el.style.right = "-100vw";

    setTimeout(() => {
      visibleToasts[el.getAttribute("data-label")] = false;
      el.remove();
    }, 1500);
  }

  function init() {
    applyBurntToastStyles();

    cover = document.createElement("div");
    cover.id = "--burnt-toast-cover";

    document.body.appendChild(cover);
  }

  function buildToast(text, isTimed) {
    let indPos = 0;

    for (let i = 0; i < visibleToasts.length; i++) {
      if (visibleToasts[i] === false) {
        visibleToasts[i] = true;
        indPos = i;
        break;
      }
    }

    const newPlate = document.createElement("div");
    newPlate.setAttribute("data-label", indPos);
    newPlate.classList.add("--burnt-toast-plate");
    newPlate.style.marginTop = "calc(1vw + " + indPos * 11 + "vh)";

    const newPlateText = document.createElement("h1");
    newPlateText.innerHTML = text;
    newPlateText.classList.add("--burnt-toast-text");

    const newCloseButton = document.createElement("div");
    newCloseButton.classList.add("--burnt-toast-button");
    newCloseButton.onclick = () => {
      closeToast(newPlate);
    };

    const newCloseButtonText = document.createElement("span");
    newCloseButtonText.classList.add("--burnt-toast-button-text");
    newCloseButtonText.classList.add("material-symbols-rounded");
    newCloseButtonText.innerHTML = "close";

    if (isTimed) {
      const newProgressContainer = document.createElement("div");
      newProgressContainer.classList.add("--burnt-toast-progress-container");

      const newProgressBar = document.createElement("div");
      newProgressBar.classList.add("--burnt-toast-progress-bar");

      newProgressContainer.appendChild(newProgressBar);
      newPlate.appendChild(newProgressContainer);
    }

    newCloseButton.appendChild(newCloseButtonText);
    newPlate.appendChild(newPlateText);
    newPlate.appendChild(newCloseButton);
    cover.appendChild(newPlate);

    return newPlate;
  }

  // Public functions
  window.burnt_toast = {
    init: init,
    sendToast: sendToast,
    sendTimedToast: sendTimedToast,
    setPlateParams: setPlateParams,
    setButtonColors: setButtonColors,
    setIsProgressBarTop: setIsProgressBarTop,
    setTitleCSS: setTitleCSS,
    setProgressBarColors: setProgressBarColors,
  };
})();
