import axios from 'axios';

/**
 * initialize the client with the base url
 */
const http = axios.create({
    baseURL: process.env.REACT_APP_DJANGO_API,
    responseType: 'json',
});

const VIDEOS_ENDPOINT = '/videos';


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
     * performs GET request to retrieve videos list from searchbar entry
     * the param is optional, retrieve full video list instead if not provided
     *
     * @param name
     *          searchbar query, optional
     * @returns {Promise<Pager>}
     *          Pager
     */
    searchVideos: async (searchQuery) => {
        const params = searchQuery ? { search_query: searchQuery } : null;
        const response = await http.get(`${VIDEOS_ENDPOINT}/`, { params });
        return new Pager(response.data);
    },
};


function Video(response) {
    this.id = response.id;
    this.name = response.name;
    this.videoUrl = response.video_url;
    this.thumbnail = response.thumbnail;
    this.frSubtitleUrl = response.fr_subtitle_url;
    this.enSubtitleUrl = response.en_subtitle_url;
    this.ovSubtitleUrl = response.ov_subtitle_url;
    if (response.movie) {
        this.movie = response.movie;
    }
    if (response.series) {
        this.series = response.series;
    }
    if (response.episode) {
        this.episode = response.episode;
    }
    if (response.season) {
        this.season = response.season;
    }
}


function Pager(response) {
    this.count = response.count;
    this.videos = response.results.map((video) => new Video(video));
    this.numberOfPages = Math.ceil(response.count / response.results.length);
    this.videosPerPages = response.results.length;
    this.nextPageUrl = response.next;
    this.previewsPageUrl = response.previous;
}

Pager.prototype.getNextPage = async function () {
    const response = await http.get(this.nextPageUrl);
    return new Pager(response.data);
};


export { client };
