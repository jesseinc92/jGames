// GAME DETAILS HTML WORKAROUND

const description = document.querySelector('#game-desc');
description.innerHTML = description.innerText;


/* Video API functionality */

// select each video container and extract the api_detail_url from attributes
const videoContainers = document.querySelectorAll('.game-video');

videoURLs = []
videoContainers.forEach(vid => {
    videoURLs.push(vid.attributes[1].nodeValue)
});

// to avoid rate limit issues with this API, I'm artificially spacing out the video
// source file calls with setInterval.

// count = 0;

// async function apiVideoCall() {
    
//     vid_detail_url = videoURLs[count];
    
//     resp = await axios.get('/games/videos', { params: {vid_detail_url } });
    
//     console.log(resp.results)

//     count++;

//     if (count == videoURLs.length) {
//         clearInterval(videoCalls);
//     }
// }

//apiVideoCall();

//const videoCalls = setInterval(apiVideoCall, 1250);