import axios from 'axios';

/**
 * initialize the client with the base url
 */
const http = axios.create({
    baseURL: process.env.REACT_APP_DJANGO_API,
    responseType: 'json'
})

const VIDEOS_ENDPOINT = '/videos';
const SERIES_ENDPOINT = '/series';
const SEASON_ENDPOINT = '/season';
const MOVIES_ENDPOINT = '/movies';


const client = {
    /**
     * performs GET request to retrieve a single video by it's ID
     *
     * @param id
     *          video's id
     * @returns {Promise<void>}
     *          Video
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
     *          Pager
     */
    searchSeries: async searchQuery => {
        const params = searchQuery ? { search_query: searchQuery } : null;
        var response = await http.get(`${SERIES_ENDPOINT}/`, { params: params});
        return new Pager(response.data);
    },

    searchMovies: async searchQuery => {
        const params = searchQuery ? { search_query: searchQuery } : null;
        var response = await http.get(`${MOVIES_ENDPOINT}/`, { params: params});
        response.data.results = response.data.results.map(result => {
            return result.video_set.results[0];
        });
        return new Pager(response.data);
    },

    getSeason: async (id) => {
        var response = await http.get(`${SERIES_ENDPOINT}/${id}`);
        const serie = {
            seasons: response.data.seasons,
            title : response.data.title
        };
        return serie;
    },

    getEpisodes: async (id, season) => {
        var response = await http.get(`${SERIES_ENDPOINT}/${id}${SEASON_ENDPOINT}/${season}`);
        return new Pager(response.data);
    }


};


function Video (response) {
    this.id = response.id;
    this.name = response.name ?  response.name : response.title;
    this.videoUrl = response.video_url;
    this.thumbnail = response.thumbnail;
    this.frSubtitleUrl = response.fr_subtitle_url;
    this.enSubtitleUrl = response.en_subtitle_url;
    this.ovSubtitleUrl = response.ov_subtitle_url;
    if(response.movie){
        this.movie = response.movie;
    }
    if(response.series){
        this.series = response.series;
    }
    if(response.episode){
        this.episode = response.episode;
    }
    if(response.season){
        this.season = response.season;
    }
}

function Pager(response, seasons, title) {
    this.count = response.count;
    this.videos = response.results.map(video => new Video(video));
    this.nextPageUrl = response.next;
    this.previewsPageUrl = response.previous;
    this.seasons = seasons ? seasons : null;
}

Pager.prototype.getNextPage = async function () {
    var response = await http.get(this.nextPageUrl);
    return new Pager(response.data);
};


export {client}