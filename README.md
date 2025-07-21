# cintel-06-custom

## Get the Code
Clone your GitHub repo down to your local machine.
Use your GitHub **username** and your GitHub **repo name** in place of cintel-06-cintel.

```shell
git clone https://github.com/abeaderstadt/cintel-06-cintel
```

## Run Locally - Initial Start

After cloning your project down to your Documents folder, open the project folder for editing in VS Code.

Create a local project virtual environment named .venv, activate it, and install the requirements.

When VS Code asks to use it for the workspace, select Yes.

```shell
py -m venv .venv
.venv\Scripts\Activate
py -m pip install --upgrade pip setuptools
py -m pip install --upgrade -r requirements.txt
```

Open a terminal (VS Code menu "View" / "Terminal") in the root project folder and run these commands to launch app.

```shell
shiny run --reload --launch-browser dashboard/app.py
```

Open a browser to <http://127.0.0.1:8000/> and test the app.

## Run Locally - Subsequent Starts

Open a terminal (VS Code menu "View" / "Terminal") in the root project folder and run these commands.

```shell
.venv\Scripts\Activate
shiny run --reload --launch-browser dashboard/app.py
```

## After Changes, Export to Docs Folder

Export to docs folder and test GitHub Pages locally.

Open a terminal (VS Code menu "Terminal" / "New Terminal") in the root project folder and run these commands.

```shell
shiny static-assets remove
shinylive export dashboard docs
py -m http.server --directory docs --bind localhost 8008
```

Open a browser to <http://[::1]:8008/> and test the Pages app.

## Push Changes back to GitHub

Open a terminal (VS Code menu "Terminal" / "New Terminal") in the root project folder and run these commands.

```shell
git add .
git commit -m "Useful commit message"
git push -u origin main
```

## Enable GitHub Pages

Go to your GitHub repo settings and enable GitHub Pages for the docs folder.

## Explore

This section guides you through exploring and interacting with the app to fully appreciate its features and functionality.

1. **Launch the App**  
   Open the live app using the GitHub Pages link or run it locally following the setup instructions above.

2. **Interact with Filters**  
   - Use the **Bill Amount** slider in the sidebar to filter data by the total bill value.  
   - Select/deselect **Food Service** times (Lunch, Dinner) and **Sex** checkboxes to explore tipping behaviors across these categories.  
   - Click the **Reset Filter** button to quickly restore all filters to their default states.

3. **Review Summary Value Boxes**  
   At the top of the main page, review key summary statistics that update reactively based on your filter selections:  
   - **Total Tippers** — number of tips matching filters  
   - **Average Tip** — average tip percentage given  
   - **Average Bill** — average bill amount within your filters

4. **Analyze the Charts**  
   The app presents four interactive charts that respond to your filter inputs:  
   - **Total Bill vs Tip Scatterplot** — Explore tipping trends and relationships by category, with options to color the points by sex, smoker status, day, or time.  
   - **Tip Percentage Distribution by Category** — Histograms display how tip percentages vary across selected categories.  
   - **Average Tip by Sex** — Compare average tip amounts between males and females dynamically.  
   - **Total Tips by Day of Week** — View how total tips vary by day, showing patterns across the week.

5. **Customize Your View**  
   Use input controls within popovers on the charts to change color variables or categories, giving you additional ways to slice and dice the data.

6. **Observe Reactive Updates**  
   Try adjusting filters and note how all statistics, tables, and charts update instantly — demonstrating the power of reactive analytics with PyShiny.
