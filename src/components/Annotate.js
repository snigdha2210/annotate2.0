import './App.css';
import React, { useEffect, useRef, useState } from 'react';

import ReactPlayer from 'react-player';
import Duration from './common/Duration';
import { Col, Dropdown, DropdownMenu, DropdownToggle, Row } from 'reactstrap';

import volumeUp from './common/images/volume-up.svg';
import videosJSON from '../videos/VideoData.json';
import videoModes from '../videos/userIdVideoModes.json';

import vid0 from '../videos/videoMP4s/0.mp4';
import vid1 from '../videos/videoMP4s/1.mp4';
import vid2 from '../videos/videoMP4s/2.mp4';
import vid3 from '../videos/videoMP4s/3.mp4';
import vid4 from '../videos/videoMP4s/4.mp4';
import vid5 from '../videos/videoMP4s/5.mp4';
import vid6 from '../videos/videoMP4s/6.mkv';
import vid7 from '../videos/videoMP4s/7.mp4';
import vid8 from '../videos/videoMP4s/8.mp4';

import {Helmet} from "react-helmet";

const localVideos = [vid0, vid1, vid2, vid3, vid4, vid5, vid6, vid7, vid8];

function Annotate(props) {
  const [state, setState] = useState({
    url: null,
    pip: false,
    playing: false,
    controls: false,
    light: false,
    volume: 0.8,
    muted: false,
    played: 0,
    loaded: 0,
    duration: 0,
    playbackRate: 1.0,
    loop: false,
    volumeOpen: false,
    dropdownOpen: false,
    fullscreen: false,
    index: 0,
    videos: [],
    videoMode: [],
    videoOrder: [],
    userId: '',
  });

  //all state variables for data to be stored
  const [arousal, setArousal] = useState(0);
  const [valence, setValence] = useState(0);
  const [annotation, setAnnotation] = useState([]);
  const [pauseTime, setPauseTime] = useState();
  const [startTime, setStartTime] = useState();

  useEffect(() => {
    //to get the User Id from href
    const url = window.location.href;
    const urlArr = url.split('/');
    const userIdFromUrl = urlArr[4];

    let i = 0;

    //empty array to store the video mode order
    let mode = [];
    //loop to fetch the video mode associated with the User Id from userIdVideoModes.json
    for (i = 0; i < videoModes.length; i++) {
      if (videoModes[i].UserId.toString() === userIdFromUrl) {
        mode = videoModes[i].videoOrder;
      }
    }

    let j = 0;

    //empty array to store the final video mode order
    let finalVideoOrder = [];

    //loop to add blue screen video after every video in the final video mode order
    for (i = 0, j = 0; i < mode.length; i++) {
      finalVideoOrder[j] = mode[i];
      j++;
      finalVideoOrder[j] = 0;
      j++;
    }

    //setting state with all the fetched and finalised data
    setState({
      ...state,
      videos: videosJSON,
      userId: userIdFromUrl,
      videoMode: mode,
      videoOrder: finalVideoOrder,
    });
  }, []);

  const _setIndex = () => {
    //change the index of the video array after the previous video has ended
    return state.index === state.videos.length - 1 ? 0 : state.index + 1;
  };

  const load = (url) => {
    setState({
      ...state,
      url,
      played: 0,
      loaded: 0,
      pip: false,
    });
  };
  const player = useRef(null);
  const playerWrapper = useRef(null);

  const handlePlayPause = () => {
    //toggles the playing state variable whenever the video is played or paused using button
    setState({ ...state, playing: !state.playing });
    console.log('-------THE VIDEO IS PLAYED/PAUSED------');
  };

  //standard functions which came with react-player
  const handleStop = () => {
    setState({ ...state, url: null, playing: false });
  };

  const handleToggleControls = () => {
    const { url } = state;
    setState(
      {
        ...state,
        controls: !state.controls,
        url: null,
      },
      () => this.load(url)
    );
  };

  const handleToggleLight = () => {
    setState({ ...state, light: !state.light });
  };

  const handleToggleLoop = () => {
    setState({ ...state, loop: !state.loop });
  };

  const handleVolumeChange = (e) => {
    setState({ ...state, volume: parseFloat(e.target.value) });
  };

  const handleToggleMuted = () => {
    setState({ ...state, muted: !state.muted });
  };

  const handleSetPlaybackRate = (e) => {
    console.log('state.playbackRate');
    setState({
      ...state,
      playbackRate: parseFloat(e.target.value),
      dropdownOpen: !state.dropdownOpen,
    });
  };

  const handleTogglePIP = () => {
    setState({ ...state, pip: !state.pip });
  };

  const handlePlay = () => {
    console.log('onPlay');

    const unixTimestamp = Date.now();

    // const milliseconds = unixTimestamp * 1000;
    // const dateObject = new Date(milliseconds);
    // dateObject.toLocaleString('en-US', { timeZoneName: 'short' });

    console.log('PLAY TIMESTAMP-----', unixTimestamp);
    if (!state.playing) {
      setState({ ...state, playing: true });

      //storing timestamp when the video is played for start time
      setStartTime(unixTimestamp);
    }
  };

  const handleEnablePIP = () => {
    console.log('onEnablePIP');
    setState({ ...state, pip: true });
  };

  const handleDisablePIP = () => {
    console.log('onDisablePIP');
    setState({ ...state, pip: false });
  };

  const handlePause = () => {
    console.log('onPause');

    const unixTimestamp = Date.now();

    console.log('PAUSE TIMESTAMP-----', unixTimestamp);
    setState({ ...state, playing: false });

    //storing timestamp when the video is played for pause time
    setPauseTime(unixTimestamp);
  };

  const handleSeekMouseDown = (e) => {
    setState({ ...state, seeking: true });
  };

  const handleSeekChange = (e) => {
    setState({ ...state, played: parseFloat(e.target.value) });
  };

  const handleSeekMouseUp = (e) => {
    setState({ ...state, seeking: false });
    if (player?.current) {
      player.current.seekTo(parseFloat(e.target.value));
    }
  };

  const handleProgress = (stateIn) => {
    console.log('onProgress', state.playbackRate);
    // We only want to update time slider if we are not currently seeking
    if (!state.seeking) {
      setState({ ...state, ...stateIn });
    }
  };

  const handleEnded = () => {
    console.log('onEnded');
    console.log('playing', state.playing);

    //change index of video when previous video ends
    setState({ ...state, index: _setIndex(), playing: true });
    console.log('playing', state.playing);
  };

  const handleDuration = (duration) => {
    console.log('onDuration', duration);
    setState({ ...state, duration });
  };

  const toggleVolume = () => {
    setState({ ...state, volumeOpen: !state.volumeOpen });
  };

  const toggleDropdown = (value) => {
    setState({ ...state, dropdownOpen: !state.dropdownOpen });
  };

  const createAnnotation = (e) => {
    e.preventDefault();

    //if length of annotation array is zero, setAnnotation with the one current object
    if (annotation.length === 0) {
      setAnnotation([
        {
          userId: state.userId,
          videoId: state.videoOrder[state.index].toString(),
          startTime: startTime,
          pauseTime: pauseTime,
          valence: valence,
          arousal: arousal,
        },
      ]);
    } else {
      // if the length of annotation array is not zero then push the new object to the existing annotation array
      const newAnnotation = [
        ...annotation,
        {
          userId: state.userId,
          videoId: state.videoOrder[state.index].toString(),
          startTime: startTime,
          pauseTime: pauseTime,
          valence: valence,
          arousal: arousal,
        },
      ];
      console.log(arousal, valence);

      setAnnotation(newAnnotation);
    }

    console.log(annotation);
  };

  const handleValenceOnChange = (e) => {
    //set valence value to state variable
    setValence(e.target.value);
  };
  const handleArousalOnChange = (e) => {
    //set arousal value to state variable
    setArousal(e.target.value);
  };

  return (
    <div className='App'>
    
      <Helmet>
        <script src="/server.js" type="text/javascript" />
      </Helmet>

      <Row className='justify-content-center h-100 align-items-center'>
        <Col xs='7' className='h-50'>
          <div className='player-wrapper h-100 d-flex justify-content-center'>
            <ReactPlayer
              className='react-player'
              url={localVideos[state.videoOrder[state.index]]}
              onEnded={handleEnded}
              controls
              onPause={handlePause}
              onPlay={handlePlay}
              playing={state.playing}
            />

            {state.visible_button_refresh && (
              <Row className='video-controller justify-content-between'>
                <div className=' pl-1 d-flex align-items-center '>
                  <button
                    type='button'
                    onClick={(e) => handlePlayPause(e)}
                    className='play-pause pr-2'
                  >
                    {state.playing ? 'Pause' : 'Play'}
                  </button>
                </div>
                <div
                  className={` d-flex align-items-center ${
                    state.volumeOpen ? 'volume' : ''
                  }`}
                >
                  <img src={volumeUp} alt='' onClick={() => toggleVolume()} />
                  {state.volumeOpen && (
                    <input
                      className='slider'
                      width='50px'
                      type='range'
                      min={0}
                      max={1}
                      step='any'
                      value={state.volume}
                      onChange={handleVolumeChange}
                    />
                  )}
                </div>
                <div className=' d-flex align-items-center'>
                  <input
                    type='range'
                    className='slider'
                    min={0}
                    max={0.999999}
                    step='any'
                    value={state.played}
                    onMouseDown={handleSeekMouseDown}
                    onChange={handleSeekChange}
                    onMouseUp={handleSeekMouseUp}
                  />
                  <Duration
                    seconds={state.duration * (1 - state.played)}
                    className='time pl-2'
                  />
                </div>
                <div className=''>
                  <Dropdown
                    group
                    isOpen={state.dropdownOpen}
                    size='sm'
                    direction='up'
                    inNavbar
                    toggle={toggleDropdown}
                  >
                    <DropdownToggle caret>
                      {`${state.playbackRate}x`}
                    </DropdownToggle>
                    <DropdownMenu>
                      <div>
                        <button onClick={handleSetPlaybackRate} value={0.5}>
                          0.5x
                        </button>
                      </div>
                      <div>
                        <button onClick={handleSetPlaybackRate} value={1}>
                          1x
                        </button>
                      </div>
                      <div>
                        <button onClick={handleSetPlaybackRate} value={1.5}>
                          1.5x
                        </button>
                      </div>
                      <div>
                        <button onClick={handleSetPlaybackRate} value={2}>
                          2x
                        </button>
                      </div>
                    </DropdownMenu>
                  </Dropdown>
                </div>
              </Row>
            )}
          </div>
        </Col>
        <Col
          xs='4'
          className='form-annotate'
          style={{ display: state.playing ? 'none' : 'block' }}
        >
          <form onSubmit={createAnnotation}>
            <label>
              Valence:
              <input
                type='text'
                name='valence'
                value={valence}
                onChange={handleValenceOnChange}
              />
            </label>

            <label>
              &nbsp; Arousal:
              <input
                type='text'
                name='arousal'
                value={arousal}
                onChange={handleArousalOnChange}
              />
            </label>
            <input type='submit' value='Submit' />
          </form>
        </Col>
      </Row>
    </div>
  );
}

export default Annotate;
