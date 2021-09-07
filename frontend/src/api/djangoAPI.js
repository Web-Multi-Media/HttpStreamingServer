import axios from 'axios';
import { checkPropTypes } from 'prop-types';

/**
 * initialize the client with the base url
 */
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

const http = axios.create({
    baseURL: process.env.REACT_APP_DJANGO_API,
    responseType: 'json',
});

const VIDEOS_ENDPOINT = '/videos';
const SERIES_ENDPOINT = '/series';
const SEASON_ENDPOINT = '/season';
const MOVIES_ENDPOINT = '/movies';
const TASKS_ENDPOINT = '/tasks';
const SUBTITLES_ENDPOINT = '/subtitles';
const HISTORY_ENDPOINT = '/history';
const SYNC_ENDPOINT = '/sync_subtitles';
const UPDATE_ENDPOINT = '/updatedb';
const AUTH_ENDPOINT = '/rest-auth';

function Client() {
    this.token = null;

    /**
     * Procedure to set the user API token in the axios http client
     *
     * @param token
     *          user API token
     */
    this.setToken = (token) => {
        console.log("set Token " + token.key );
        this.token = token ? `Token ${token.key}` : "";
    };

    /**
     * Procedure to check if the client token is set
     *
     */
    this.isLoggedIn = () => {
        return !(this.token === (null) ||  this.token === "")
    };

    /**
     * Procedure to reset the user API token in the axios http client
     *
     * @param token
     *          user API token
     */
     this.resetToken = () => {
        this.token = null;
    };

    /**
     * Returns the csrf cookie
     *
     * @returns {str}
     *          csrf cookie value
     */
    this.getCsrfcookie = () => {  // for django csrf protection
        let cookieValue = null,
            name = "csrftoken";
        if (document.cookie && document.cookie !== "") {
            let cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) == (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    this.csrfcookie = this.getCsrfcookie();

    /**
     * Wrapper for sending GET request to server using axios http client
     *
     * @param endPoint
     *          API endpoint to which send the GET request
     * @returns {Response}
     *
     */
    this.getRequest = (endPoint, params={}) => http.get(`${endPoint}`, {
        ...params,
        headers: {
            Authorization: this.token, // the token is a variable which holds the token
        },
    });

    /**
     * Wrapper for sending POST request to server using axios http client
     *
     * @param endPoint
     *          API endpoint to which send the POST request
     * @param body
     *          Body of the POST reuqest
     * @returns {Response}
     *
     */
    this.postRequest = (endPoint, param={}, extra_header=null) =>
    {

        const options = {
            headers : {
                Authorization: (this.token !==null) ? this.token:'', // the token is a variable which holds the token
                'X-CSRFToken': this.csrfcookie ? this.csrfcookie:'',
                ...extra_header
            }
        };


        return http.post(`${endPoint}/`, param , options);
}

    /**
     * performs GET request to retrieve a single video by it's ID
     *
     * @param id
     *          video's id
     * @returns {Promise<Video>}
     *          Video
     */
    this.getVideoById = async (id) => {

        try{
            const response = await this.getRequest(`${VIDEOS_ENDPOINT}/${id}/`);
            return new Video(response.data);
        } catch ( error ) {
            console.log( "Error caught and rethrown in ():", error.message );
            throw( error );
        }
    };

    /**
     * performs GET request to retrieve a single video by it's ID
     *
     * @param id
     *          video's id
     * @returns {Promise<Video>}
     *          Video
     */
    this.updateHistory = async (id, timeStamp = 0) => {
        const body =
        {
            body:{
                'video-id': id,
                'video-time': timeStamp,}
        };
        try {
            const response = await this.postRequest(HISTORY_ENDPOINT, body, { 'content-type': 'application/json' });
            return new MoviesPager(response.data);
        } catch (error) {
            console.log("Error caught and rethrown in ():", error.message);
            throw (error);
        }
    };


    /**
     * performs GET request to retrieve a single video by it's ID
     *
     * @param id
     *          video's id
     * @returns {Promise<Video>}
     *          Video
     */
    this.getHistory = async () => {
        try {
            const response = await this.getRequest(HISTORY_ENDPOINT);
            return new MoviesPager(response.data);
        } catch (error) {
            console.log("Error caught and rethrown in ():", error.message);
            throw (error);
        }
    };

    /**
     * performs GET request to retrieve videos list from searchbar entry
     * the param is optional, retrieve full video list instead if not provided
     *
     * @param name
     *          searchbar query, optional
     * @returns {Promise<Pager>}
     *          Pager
     */
    this.searchSeries = async (searchQuery) => {
        const params = searchQuery ? { search_query: searchQuery } : null;
        try {
            const response = await this.getRequest(SERIES_ENDPOINT, { params });
            return new SeriesPager(response.data);
        } catch (error) {
            console.log("Error caught and rethrown in ():", error.message);
            throw (error);
        }
    };

    this.searchMovies = async (searchQuery) => {
        const params = searchQuery ? { search_query: searchQuery } : null;
        try {
            const response = await this.getRequest(MOVIES_ENDPOINT, { params });
            response.data.results = response.data.results.reduce((result, element) => {
                //We filter here empty movies set
                if (element.video_set.count > 0)
                    result.push(element.video_set.results[0]);
                return result;
            }, []);
            return new MoviesPager(response.data);
        } catch (error) {
            console.log("Error caught and rethrown in ():", error.message);
            throw (error);
        }
    };

    /**
     * performs POST request to upload a new subtitles to a video
     *
        data['video_id'] = video.id
        data['language'] = 'fra'
        data['datafile'] = open('/usr/src/app/Videos/subtitles/test.srt', 'rb')
     * @returns {Promise<Video>}
     *          Video
     */
    this.uploadSubtitles = async ( video_id, language, datafile) => {
        let params = new FormData();
        params.append('datafile',datafile);
        params.append('language',language);
        params.append('video_id',video_id);
        try {
            const response = await this.postRequest(SUBTITLES_ENDPOINT, params, { 'content-type': 'multipart/form-data' });
            return response;
        } catch (error) {
            console.log("Error caught and rethrown in ():", error.message);
            throw (error);
        }
        
    };

    this.resyncSubtitle = async (video_id, subtitle_id) => {
        const response = await this.getRequest(`${SYNC_ENDPOINT}/${video_id}/${subtitle_id}/`);
        return response;
    }

    /**
     * performs GET request to a task status
     *
     * @param id
     *          Task's id
     * @returns {Promise<Video>}
     *          Video
     */
    this.getTaskStatusByID = async (id) => {
        try {
            const response = await this.getRequest(`${TASKS_ENDPOINT}/${id}/`);
            return response.data;
        } catch (error) {
            console.log("Error caught and rethrown in ():", error.message);
            throw (error);
        }
    };

    /**
     * performs GET request to retrieve a single subtitle by it's ID
     *
     * @param id
     *          subtitle's id
     * @returns {Promise<Subtitle>}
     *          Video
     */

    this.getSubtitleById = async (id) => {
        try {
            const response = await this.getRequest(`${SUBTITLES_ENDPOINT}/${id}/`);
            return new Subtitle(response.data);
        } catch (error) {
            console.log("Error caught and rethrown in ():", error.message);
            throw (error);
        }
    };

    /**
     * performs POST request to logout
     *
     * @param id
     *          subtitle's id
     * @returns {Promise<Subtitle>}
     *          Video
     */

    this.logout = async () => {
        try{
            const response = await client.postRequest("/rest-auth/logout", null);
            this.token = "";
        } catch (error) {
            console.log("Error caught and rethrown in ():", error.message);
            throw (error);
        }
    };

    /**
     * performs POST request to login
     *
     *
     * @param username, password, email
     *          
     * @returns 
     *          
     */

     this.login = async (username, password, email) => {
        const param = {
    
            'username': username,
            'password': password,
            'email': "",
          
        };
        try{
            const response = await client.postRequest("/rest-auth/login", param );
            return response;
        } catch (error) {
            console.log("Error caught and rethrown in ():", error.message);
            throw (error);
        }
    };

    /**
     * performs POST request to signup
     *
     * @param username, password, email
     *          
     * @returns 
     *          
     */

     this.signup = async (username, password, password2) => {
        const param = {
    
            'username': username,
            'password1': password,
            'password2': password2,
          
        };
         try {
             const response = await client.postRequest("/rest-auth/registration", param);
             return response;
         } catch (error) {
             console.log("Error caught and rethrown in ():", error.message);
             throw (error);
         }
    };

    /**
     * performs POST request to update video database
     *
     * @returns response
     */
    this.updatevideodb = async () => {
            const body =
            {
                body:{}
            };
            try{
                const response = await this.postRequest(UPDATE_ENDPOINT, body , null , {'content-type': 'multipart/form-data' } );
                return response;
            } catch (error) {
                console.log("Error caught and rethrown in ():", error.message);
                throw (error);
            }
    };

    /**
     * performs GET request to get user infos
     *
     * @returns response
     */

    this.getUserInfo = async () => {
        try {
            const response = await this.getRequest(`${AUTH_ENDPOINT}/user/`);
            return response.data;
        } catch (error) {
            console.log("Error caught and rethrown in ():", error.message);
            throw (error);
        }
    };

};



var client = new Client();


function Video(response) {
    this.id = response.id;
    this.name = response.movie !== null ? response.movie : response.name;
    this.videoUrl = response.video_url;
    this.thumbnail = response.thumbnail;
    this.subtitles = response.subtitles;
    this.series = response.series;
    this.episode = response.episode;
    this.season = response.season;
    this.movie = response.movie;
    this.time = response.time;
    this.nextEpisode = response.next_episode;
}

function SeriesPager(response) {
    this.count = response.count;
    this.type = 'Serie';
    this.series = response.results.map((serie) => new Serie(serie));
    this.nextPageUrl = response.next;
    this.previewsPageUrl = response.previous;
}

SeriesPager.prototype.getNextPage = async function () {
    const response = await client.getRequest(this.nextPageUrl);
    this.videos = response.data.results.map((video) => new Serie(video));
    this.nextPageUrl = response.data.next;
};

function Serie(serie) {
    this.id = serie.id;
    this.name = serie.title;
    this.thumbnail = serie.thumbnail;
}

Serie.prototype.getSeason = async function () {
    const response = await client.getRequest(`${SERIES_ENDPOINT}/${this.id}`);
    this.seasons = response.data.seasons;
};

Serie.prototype.getEpisodes = async function (season) {
    const response = await client.getRequest(`${SERIES_ENDPOINT}/${this.id}${SEASON_ENDPOINT}/${season}`);
    this.videos = response.data.results.map((video) => new Video(video));
    this.nextPageUrl = response.data.next;
};

Serie.prototype.getNextPage = async function () {
    const response = await client.getRequest(this.nextPageUrl);
    this.nextPageUrl = response.data.next;
    this.videos = response.data.results.map((video) => new Video(video));
};


function MoviesPager(response) {
    this.count = response.count;
    this.videos = response.results.map((video) => new Video(video));
    this.nextPageUrl = response.next;
    this.previewsPageUrl = response.previous;
}

MoviesPager.prototype.getNextPage = async function () {
    const response = await client.getRequest(this.nextPageUrl);
    response.data.results = response.data.results.map((result) => result.video_set.results[0]);
    this.videos = response.data.results.map((video) => new Video(video));
    this.nextPageUrl = response.data.next;
};

function Subtitle(response) {
    this.id = response.id;
    this.language = response.language;
    this.videoId = response.video_id;
    this.webvttSubtitleUrl = response.webvtt_subtitle_url;
    this.webvttSyncUrl = response.webvtt_sync_url;
}


export { client };
