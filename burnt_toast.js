// All credits go to Jordan Lerner
// This project is licensed under MIT
//
// https://github.com/J-Lerner/burnt_toast.js
//
// burnt_toast.js version 0.2

(function () {
  let plateCSS = `width: 25vh; height: 10vh; margin: 2vw; background-color: darkslategray;`,
    buttonColor = "gray",
    buttonHoverColor = "lightgray",
    buttonActiveColor = "darkgray",
    isToastTop = true,
    isProgressBarTop = false,
    progressContainerColor = "darkgray",
    progressBarColor = "lightgray",
    titleCSS = `color: white;`;

  const setPlateParams = (w, h, m, c) =>
    (plateCSS = `width: ${w}; height: ${h}; margin: ${m}; background-color: ${c};`);
  const setButtonColors = (bg, hover, active) => {
    buttonColor = bg;
    buttonHoverColor = hover;
    buttonActiveColor = active;
  };
  const setIsToastTop = (b) => (isToastTop = b);
  const setIsProgressBarTop = (b) => (isProgressBarTop = b);
  const setTitleCSS = (css) => (titleCSS = css);
  const setProgressBarColors = (bg, color) => {
    progressBarColor = color;
    progressContainerColor = bg;
  };

  function applyBurntToastStyles() {
    const style = document.createElement("style");
    const css = `
        @keyframes load { from { width: 0% } to { width: 100% } }
        #--burnt-toast-cover { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; user-select: none; pointer-events: none; z-index: 99999; }
        .--burnt-toast-plate { position: absolute; top: ${isToastTop ? "0" : "auto"}; bottom: ${!isToastTop ? "0" : "auto"}; right: -100vw; border-radius: 1vh; box-shadow: 0 0 6px 1px black; pointer-events: visible; overflow: hidden; transition: 1s; ${plateCSS}; }
        .--burnt-toast-button { position: absolute; height: 3vh; aspect-ratio: 1; top: ${!isProgressBarTop ? "0" : "auto"}; bottom: ${isProgressBarTop ? "0" : "auto"}; right: 0; margin: 0.5vh; cursor: pointer; display: flex; justify-content: center; align-items: center; background-color: ${buttonColor}; border-radius: 1vh; transition: 350ms; }
        .--burnt-toast-text { ${titleCSS} }
        .--burnt-toast-button:hover { margin: 0.4vh; height: 3.2vh; background-color: ${buttonHoverColor}; }
        .--burnt-toast-button:active { margin: 0.58vh; height: 2.7vh; background-color: ${buttonActiveColor}; }
        .--burnt-toast-button-text { font-size: 2vh; }
        .--burnt-toast-progress-container { position: absolute; top: ${isProgressBarTop ? "0" : "auto"}; bottom: ${!isProgressBarTop ? "0" : "auto"}; left: 0; height: 0.75vh; width: 100%; border-radius: 1vh; background-color: ${progressContainerColor}; z-index: 4; }
        .--burnt-toast-progress-bar { position: absolute; top: 0; left: 0; height: 100%; width: 10%; border-radius: 1vh; background-color: ${progressBarColor}; z-index: 5; animation-timing-function: linear; }
    `;
    style.appendChild(document.createTextNode(css));
    document.head.appendChild(style);
  }

  let cover = document.querySelector("NULL"),
    visibleToasts = [false, false, false, false, false, false];

  const sendTimedToast = (text, time) => {
    const toast = buildToast(text, true);
    toast.querySelector(".--burnt-toast-progress-bar").style.animationName =
      "load";
    toast.querySelector(".--burnt-toast-progress-bar").style.animationDuration =
      time / 1000 + 1 + "s";
    setTimeout(() => (toast.style.right = "0vw"), 10);
    setTimeout(() => closeToast(toast), time + 1000);
  };

  const sendToast = (text) => {
    const toast = buildToast(text, false);
    setTimeout(() => (toast.style.right = "0vw"), 10);
  };

  const closeToast = (el) => {
    el.style.right = "-100vw";
    setTimeout(() => {
      visibleToasts[el.getAttribute("data-label")] = false;
      el.remove();
    }, 1500);
  };

  const init = () => {
    applyBurntToastStyles();
    cover = document.createElement("div");
    cover.id = "--burnt-toast-cover";
    document.body.appendChild(cover);
  };

  const buildToast = (text, isTimed) => {
    let indPos = 0;
    for (let i = 0; i < visibleToasts.length; i++) {
      if (!visibleToasts[i]) {
        visibleToasts[i] = true;
        indPos = i;
        break;
      }
    }
    const newPlate = document.createElement("div");
    newPlate.setAttribute("data-label", indPos);
    newPlate.classList.add("--burnt-toast-plate");
    newPlate.style[isToastTop ? "marginTop" : "marginBottom"] =
      `calc(1vw + ${indPos * 11}vh)`;

    const newPlateText = document.createElement("h1");
    newPlateText.innerHTML = text;
    newPlateText.classList.add("--burnt-toast-text");

    const newCloseButton = document.createElement("div");
    newCloseButton.classList.add("--burnt-toast-button");
    newCloseButton.onclick = () => closeToast(newPlate);

    const newCloseButtonText = document.createElement("span");
    newCloseButtonText.classList.add(
      "--burnt-toast-button-text",
      "material-symbols-rounded",
    );
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
  };

  // Public functions
  window.burnt_toast = {
    init,
    sendToast,
    sendTimedToast,
    setPlateParams,
    setButtonColors,
    setIsProgressBarTop,
    setIsToastTop,
    setTitleCSS,
    setProgressBarColors,
  };
})();
