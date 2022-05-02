# Biomedical Signal Analysis for Opportunistic Probing of Emotion Self-Report Collection

This is the web app associated with the system of OCEAN dataset project.

# About the code

> **react-player** npm package has been used for making the video player.

### The whole process:

Below is the whole step-by-step process for the same:

1. Google form will be filled by the subject which will be used to allot userId to them
2. Subject opens app and puts in userId
3. The app will fetch the videos in order pre-defined (random order, just predefined for easier mapping) for the specific userId
4. Start button for the video is provided, subject will click on it and the video will start playing
5. Trigger is sent to Arduino that the video had started so that it starts collecting data (physiological signal data)
6. ML model runs and sends signal to the web app (through web socket programming) to pause the video
7. Video is paused, { _Valence, Arousal_ } values are taken from the subject
8. { _User id, Video id, Start time, Pause time, Valence, Arousal_ } - saved in json file locally
9. Start time is the time at which the video had been played the last time before pausing
10. Play button is present, subject clicks on it to start the video again after annotating
11. Step 4 to 9 keep on running in loops till all the videos have been viewed by the subject
12. When the videos are over, a signal is sent to stop taking the physiological data
13. Google form will be filled by the subject for feedback

### Structure of the code

> The functions and code has been described in the files itself in form of comments.
> Since the system being build is heavily dependent on functionality, we have not taken much time to beautify the UI/UX.

Relevant files/folders inside **src** folder:

- **components/**
  - **common/**: Contains files for react-player
  - Annotate.js: Contains react-player component, the main component having everything
  - App.css: CSS file for App.js
  - AppRouter.js: Browser router component for navigation
  - Header.js: High level component for the app
  - UserIdForm.js: First apprearing component
- **videos/**
  - **videoMP4s/**: Contains all videos (9)
  - VideoData.json: Contains information regarding all the videos
  - userIdVideoModes.json: Contains pre-defined random orders of videos for each userId (1-30)
- index.js: Starter file
- index.css: main css file

> The 9th video is missing from the **videoMP4s/** folder.
> The videos will stop whenever 9th video comes in the list.

## &nbsp;

## Available Scripts

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
