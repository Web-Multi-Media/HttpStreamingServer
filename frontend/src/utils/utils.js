import queryString from 'query-string';
import { client } from '../api/djangoAPI';

/**
 * retrieve movies and series
 * @returns {Promise<void>}
 */
export const getMoviesAndSeries = async (setPager, setVideos, setSeriesPager, setSeriesVideos, setMoviesPager, setMoviesVideos) => {
    try {
        const [fetchPager, fetchPager2] = await Promise.all([client.searchSeries(), client.searchMovies()]);
        setPager(fetchPager);
        setVideos(fetchPager.videos);
        setSeriesPager(fetchPager);
        setSeriesVideos(fetchPager.series);
        setMoviesPager(fetchPager2);
        setMoviesVideos(fetchPager2.videos);
    } catch (error) {
        console.log(error);
    }
};

/**
 * check in the url if a video is specified
 * load it in the player if exist
 * @returns {Promise<void>}
 */
export const getUrlVideo = async (location, setSelectedVideo) => {
    const values = queryString.parse(location.search);
    if (values.video) {
        const id = parseInt(values.video);
        // API call to retrieve current video
        // We look here if a query string for the video is provided, if so load the video
        try {
            const video = await client.getVideoById(id);
            setSelectedVideo(video);
        } catch (error) {
            console.log(error);
        }
    }
};
