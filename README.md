<img alt="burnt toast" src="https://png.pngtree.com/png-vector/20230925/ourmid/pngtree-burnt-toast-unattractive-png-image_10112587.png" style="width: 10vw"/>

# burnt_toast.js   v0.2 (5.63 KB)

Simple toasts for your website or app

<img alt="example" src="example.png" style="width: 20vw; border-radius: 50%"/>

## Installation and usage

1. Download burnt_toast.js and add it to your web directory
2. In your HTML head, enter
```
script type="text/javascript" src="burnt_toast.js"></script>
```
3. In a new script element AFTER burnt_toast.js has been loaded, you may be modifying.

### How to modify

burnt_toast.js should be modified when your are sure the page has been loaded.
Here's an example...
```
addEventListener("load", burnt_toast.init);
```
Use burnt_toast.init AFTER modifications and customizations have been made. Anything after initialization will not apply.
Each function must be written as burnt_toast.FUNCTION(). The list of functions is as follows

| Name                 | Params                                   | Usage                                                   |
| :------------------- | :--------------------------------------: | :-----------------------------------------------------: |
| init                 | None                                     | Initializes and applies modifications                   |
| sendToast            | Text                                     | Creates a pop-up toast                                  |
| sendTimedToast       | Text, Time                               | Creates a pop-up toast for some time                    |
| setPlateParams       | width, height, margin, color             | Edits the CSS of toasts (plates)                        |
| setButtonColors      | backgroundColor, hoverColor, activeColor | Sets colors for the close button                        |
| setIsProgressBarTop  | bool                                     | If true, the progress bar is at the top of the toast    |
| setIsToastTop        | bool                                     | If true, toasts will appear at the bottom of the screen |
| setTitleCSS          | templateString                           | Sets the CSS for the title                              |
| SetProgressBarColors | backgroundColor, color                   | Sets colors for the progress bar                        |

For an example of these in use, please check the index.html file.
