import renderer from 'react-test-renderer';
import React, { useState } from 'react';
import VideoCarrouselSlick from './VideoCarrouselSlick';

it('test carrousel creation', () => {

    const testvideo = {
        id : 1,
        name : "test",
        videoUrl : "http://fakeurl.mpd",
        thumbnail : "http://test.jpeg",
        subtitles : ["http://test.vtt"],
        series : "3",
        episode : "1",
        season : 3,
        time : 3,
        nextEpisode : 2,
    }


    let testpager = {}
    testpager.count = 2;
    testpager.videos = [testvideo]

    let handleVideoSelect = function () {}

    const component = renderer.create(
        <VideoCarrouselSlick
            pager={testpager}
            videos={testpager.videos}
            handleVideoSelect={handleVideoSelect}
        />
    );
    const testInstance = component.root;
    let coveritem = testInstance.findByProps({className: "img-cover"})
    expect(coveritem.props.src).toBe('http://test.jpeg');

});