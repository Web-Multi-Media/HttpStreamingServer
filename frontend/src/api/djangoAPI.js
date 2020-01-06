import axios from 'axios';

/**
 * initialize the client with the base url
 */
const http = axios.create({
    baseURL: process.env.REACT_APP_DJANGO_API
})

class djangoAPI {

    /**
     * performs GET request to retrieve full videos list
     *
     * @returns {Promise<void>}
     *          videos list
     */
    getAllVideos() {
        return http.get('videos/');
    }

    /**
     * performs GET request to retrieve videos list from searchbar entry
     * 
     * @param name 
     *          searchbar query
     * @returns {Promise<void>}
     *          videos list
     */
    getVideosByName(name) {
        return http.get('/videos/', {params: {search_query: name}});
    }

    /**
     * performs GET request to retrieve a single video by it's ID
     *
     * @param id
     *          video's id
     * @returns {Promise<void>}
     *          videos list
     */
    getVideosById(id) {
        return http.get(`/videos/${id}/`);
    }

    /**
     * performs GET request to retrieve the next videos 
     *
     * @param nextQuery
     *          the full query to retrieve more videos
     * @returns {Promise<void>}
     *          videos list
     */
    getNextVideos(nextQuery) {
        return http.get(nextQuery);
    }
}

export default djangoAPI;