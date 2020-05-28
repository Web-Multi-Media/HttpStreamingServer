import axios from 'axios';

/**
 * initialize the client with the base url
 */
const http = axios.create({
    baseURL: process.env.REACT_APP_DJANGO_API,
    responseType: 'json',
});

const createAxiosGetRequest = (endPoint, token) => http.get(`${endPoint}/`, {
    headers: {
        Authorization: token, // the token is a variable which holds the token
    },
});

const createAxiosPostRequest = (endPoint, token, body) => http.post(`${endPoint}/`, {
    headers: {
        Authorization: token, // the token is a variable which holds the token
    },
    body,
});
const VIDEOS_ENDPOINT = '/videos';
const SERIES_ENDPOINT = '/series';
const SEASON_ENDPOINT = '/season';
const MOVIES_ENDPOINT = '/movies';
const HISTORY_ENDPOINT = '/history';


const client = {
    /**
     * performs GET request to retrieve a single video by it's ID
     *
     * @param id
     *          video's id
     * @returns {Promise<Video>}
     *          Video
     */
    getVideoById: async (id) => {
        const response = await http.get(`${VIDEOS_ENDPOINT}/${id}`);
        return new Video(response.data);
    },


    /**
     * performs GET request to retrieve a single video by it's ID
     *
     * @param id
     *          video's id
     * @returns {Promise<Video>}
     *          Video
     */
    updateHistory: async (token, id, timeStamp = 0) => {
        const body = {
            'video-id': id,
            'video-time': timeStamp,
        };
        const response = await createAxiosPostRequest(HISTORY_ENDPOINT, token, body);
        return new MoviesPager(response.data);
    },

    /**
     * performs GET request to retrieve a single video by it's ID
     *
     * @param id
     *          video's id
     * @returns {Promise<Video>}
     *          Video
     */
    getHistory: async (token) => {
        const response = await createAxiosGetRequest(HISTORY_ENDPOINT, token);
        return new MoviesPager(response.data);
    },


    /**
     * performs GET request to retrieve videos list from searchbar entry
     * the param is optional, retrieve full video list instead if not provided
     *
     * @param name
     *          searchbar query, optional
     * @returns {Promise<Pager>}
     *          Pager
     */
    searchSeries: async (searchQuery) => {
        const params = searchQuery ? { search_query: searchQuery } : null;
        const response = await http.get(`${SERIES_ENDPOINT}/`, { params });
        return new SeriesPager(response.data);
    },

    searchMovies: async (searchQuery) => {
        const params = searchQuery ? { search_query: searchQuery } : null;
        const response = await http.get(`${MOVIES_ENDPOINT}/`, { params });
        response.data.results = response.data.results.map((result) => result.video_set.results[0]);
        return new MoviesPager(response.data);
    },


};


function Video(response) {
    this.id = response.id;
    this.name = response.movie !== null ? response.movie : response.name;
    this.videoUrl = response.video_url;
    this.thumbnail = response.thumbnail;
    this.frSubtitleUrl = response.fr_subtitle_url;
    this.enSubtitleUrl = response.en_subtitle_url;
    this.ovSubtitleUrl = response.ov_subtitle_url;
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
    const response = await http.get(this.nextPageUrl);
    this.videos = response.data.results.map((video) => new Serie(video));
    this.nextPageUrl = response.data.next;
};

function Serie(serie) {
    this.id = serie.id;
    this.name = serie.title;
    this.thumbnail = serie.thumbnail;
}

Serie.prototype.getSeason = async function () {
    const response = await http.get(`${SERIES_ENDPOINT}/${this.id}`);
    this.seasons = response.data.seasons;
};

Serie.prototype.getEpisodes = async function (season) {
    const response = await http.get(`${SERIES_ENDPOINT}/${this.id}${SEASON_ENDPOINT}/${season}`);
    this.videos = response.data.results.map((video) => new Video(video));
    this.nextPageUrl = response.data.next;
};

Serie.prototype.getNextPage = async function () {
    const response = await http.get(this.nextPageUrl);
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
    const response = await http.get(this.nextPageUrl);
    response.data.results = response.data.results.map((result) => result.video_set.results[0]);
    this.videos = response.data.results.map((video) => new Video(video));
    this.nextPageUrl = response.data.next;
};


export { client };
