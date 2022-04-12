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

  const [arousal, setArousal] = useState(0);
  const [valence, setValence] = useState(0);
  const [showForm, setShowForm] = useState(0);

  useEffect(() => {
    const url = window.location.href;
    const urlArr = url.split('/');
    const userIdFromUrl = urlArr[4];
    let i = 0;
    let mode = [];
    for (i = 0; i < videoModes.length; i++) {
      if (videoModes[i].UserId.toString() === userIdFromUrl) {
        mode = videoModes[i].videoOrder;
      }
    }

    let j = 0;
    let finalVideoOrder = [];
    for (i = 0, j = 0; i < mode.length; i++) {
      finalVideoOrder[j] = mode[i];
      j++;
      finalVideoOrder[j] = 0;
      j++;
    }

    setState({
      ...state,
      videos: videosJSON,
      userId: userIdFromUrl,
      videoMode: mode,
      videoOrder: finalVideoOrder,
    });
  }, []);

  const _setIndex = () => {
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
    setState({ ...state, playing: !state.playing });
    console.log('-------THE VIDEO IS PLAYED/PAUSED------');
  };

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
    if (!state.playing) {
      setState({ ...state, playing: true });
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
    setState({ ...state, playing: false });
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
    setState({ ...state, index: _setIndex() });
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
    //push into json file
  };

  const handleValenceOnChange = (e) => {
    console.log(e.target.value);
    setValence(e.target.value);
  };
  const handleArousalOnChange = (e) => {
    console.log(e.target.value);
    setArousal(e.target.value);
  };

  useEffect(() => {
    console.log('paused/played', state.playing);
  }, [state.playing]);

  return (
    <div className='App'>
      <Row className='justify-content-center h-100 align-items-center'>
        <Col xs='7' className='h-50'>
          <div className='player-wrapper h-100 d-flex justify-content-center'>
            {/* <video width='320' height='240' controls onEnded={handleEnded}>
              <source
                src={localVideos[state.videoOrder[state.index]]}
                type='video/mp4'
              />
            </video> */}

            <ReactPlayer
              className='react-player'
              url={localVideos[state.videoOrder[state.index]]}
              onEnded={handleEnded}
              controls
            />

            {state.visible_button_refresh && (
              <Row className='video-controller justify-content-between'>
                <div className=' pl-1 d-flex align-items-center '>
                  <button
                    type='button'
                    onClick={() => handlePlayPause()}
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
          style={{ display: !state.playing ? 'block' : 'none' }}
        >
          <form>
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
              Arousal:
              <input
                type='text'
                name='arousal'
                value={arousal}
                onChange={handleArousalOnChange}
              />
            </label>
            <input type='submit' value='Submit' onClick={createAnnotation} />
          </form>
        </Col>
      </Row>
    </div>
  );
}

export default Annotate;
