# burnt_toast.js

Simple toasts for your website

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

| Name              | Params | Usage |
| :---------------- | :--: |:----------: |
| init              | None  | Initializes and applies modifications   |
| sendToast         | Text | Creates a pop-up toast |
| sendTimedToast    | Text, Time | Creates a pop-up toast for some time   |
| setPlateParams | width, height, margin, color | Edits the CSS of toasts (plates) |
| setButtonColors | backgroundColor, hoverColor, activeColor | Sets colors for the close button |
| setIsProgressBarTop | bool | If true, the progress bar is at the top of the toast |
| setTitleCSS | templateString | Sets the CSS for the title |
| SetProgressBarColors | backgroundColor, color | Sets colors for the progress bar |

For an example of these in use, please check the index.html file.
