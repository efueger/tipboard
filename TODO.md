#### Required:
* [x] Remove API_TOKEN from GET variable
* [x] when TOKEN_API is not correct, return 401 not 404 #31
* [ ] fix the old way to update tile
* [ ] fix the fadding possibility
* [x] publish sensors exemple
* [ ] CD AWS
* [ ] CD Openshift
* [ ] Made a dev Wiki
* [ ] Make a real wiki to deploy in clouds
* [ ] Animation when tile update
* [ ] Make compatible with Python 3.4 & 3.5 & 3.6
* [x] Grid layout with flex
* [x] Let's material design the tiles ! (Its 2019 ffs)
* [ ] Add Contrib.md
* [x] Test it on windows
* [ ] Propose real docker img with/without redis
* [ ] publish a public tipboard to show build CI/CD stats of project
* [ ] made issue #32 possible
* [ ] Update the user doc for /update
* [ ] Review the code
* [x] Fix Badge status in Readme.md
* [ ] Write script to put in production ready mode (minify JS, debug=False, etc)


#### Optional

* add color blind mode :)
* Deploy to Azure
* Eazy way to secure dashboard with authentification view
* Add matomo iframe widget as tile :D
* Propose an interactive/GUI way to build your custom_layout !


If we do that, we can go to sleep ez


##### NB To update Documentation

dans le merge des .js ChartJS tiles tu migres vbar_chart
tu dois add un filter dans parser.py utilisé dans le dashboard.dashboardRendererHandler
mais quelle fonction va etre call dans tipboard.js.getUpdateFonction(l:194)
Et comment connaitre le tile_template name dans la tiles.js ?
pour envoyer HorizontalBar au lieu de Bar
