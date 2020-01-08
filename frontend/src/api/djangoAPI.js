import axios from 'axios';

/**
 * initialize the client with the base url
 */
const http = axios.create({
    baseURL: process.env.REACT_APP_DJANGO_API,
    responseType: 'json'
})

const VIDEOS_ENDPOINT = '/videos';


const client = {
    /**
     * performs GET request to retrieve a single video by it's ID
     *
     * @param id
     *          video's id
     * @returns {Promise<void>}
     *          videos list
     */
    getVideoById: async id => {
        var response = await http.get(`${VIDEOS_ENDPOINT}/${id}`);
        return new Video(response.data);
    },
    /**
     * performs GET request to retrieve videos list from searchbar entry
     * the param is optional, retrieve full video list instead if not provided
     * 
     * @param name 
     *          searchbar query, optional
     * @returns {Promise<void>}
     *          videos list
     */
    searchVideos: async searchQuery => {
        const params = searchQuery ? { search_query: searchQuery } : null;
        var response = await http.get(`${VIDEOS_ENDPOINT}/`, { params: params});
        return new Pager(response.data);
    }
}


function Video (response) {
    this.id = response.id;
    this.name = response.name;
    this.videoUrl = response.video_url;
    this.thumbnail = response.thumbnail;
    this.frSubtitleUrl = response.fr_subtitle_url;
    this.enSubtitleUrl = response.en_subtitle_url;
    this.ovSubtitleUrl = response.ov_subtitle_url;
}


function Pager(response) {
    this.count = response.count;
    this.videos = response.results.map(video => new Video(video));
    this.numberOfPages = Math.ceil(response.count / response.results.length);
    this.videosPerPages = response.results.length;
    this.nextPageUrl = response.next;
    this.previewsPageUrl = response.previous;

    async function getNextPage () {
        var response = await http.get(this.nextPageUrl);
        return new Pager(response.data);
    };
}


/** 
 ******************************************
 **************** HANDLER *******************
 ******************************************
 */

/**
 * handle the errors coming from api
 *
 * @param err
 *          the full catched error
 */
function handleError(err) {
    if (err.response) {
        console.log(err.response.data);
    } else if (err.request) {
        console.log(err.request);
    } else {
        console.log('err', err.message);
    }
}

export {client, handleError}