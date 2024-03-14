import React, { useState } from 'react';
import '../../style/style.scss';
import VideoCarrouselSlick from "./VideoCarrouselSlick";
import SelectBar from "./SelectBar";


//class SeriesCarousel extends Component {
const SeriesCarousel = ({ pager, videos, handleVideoSelect }) => {

    const [series, setSeries] = useState('');
    const [seriesPager, setSeriesPager] = useState(pager);
    const [seasons, setSeasons] = useState([]);
    const [episode, setEpisode] = useState('');
    const [seriesId, setSeriesId] = useState(0);
    const [reset, setReset] = useState(false);
    const [Seriesvideos, setVideos] = useState(videos);
    const [refresh, setRefresh] = useState(false);


    const getSeriesSeason = async (serie) => {
        try {
            await serie.getSeason();
            await serie.getEpisodes(serie.seasons[0]);
            setSeriesPager(serie);
            setSeries(serie.name);
            setSeasons(serie.seasons);
            setSeriesId(serie);
            setReset(false);
            setVideos(serie.videos);

        } catch(error) {
            console.log(error);
        }
    };

    const handleSeasonSelect = async (e) => {
        const serie = seriesPager;
        await serie.getEpisodes(e.target.value);
        setSeriesPager(serie);
        setVideos(serie.videos);
        setReset(false);
    };

    const handleSeriesSelect = async (video) => {
        if (series === '') {
            await getSeriesSeason(video);
            setRefresh(true);
        }
        else{
            handleVideoSelect(video);
            setEpisode(video.name);
        }
        // change tab title with the name of the selected video
        document.title = video.name;
    };

    const resetSeries = () => {
        console.log(pager.series);
        setSeriesPager(pager);
        setSeries('');
        setSeasons('');
        setEpisode('')
        setReset(true);
        setVideos(videos);
        setRefresh(true);
    };


        return (
            <div>
                <div className="seriesDisplay">
                <h4 className="centerVer hover-hilight" onClick={()=>resetSeries()}>SERIES</h4>
                {series.length > 0 &&
                    <React.Fragment>
                    <span className="centerVer"> > {series} > </span>
                    <SelectBar
                    seasons = {seasons}
                    handleSeason= {handleSeasonSelect}
                    />
                    </React.Fragment>
                }
                {episode !== '' &&  <span className="centerVer"> > {episode}</span>}
                </div>
                {Seriesvideos.length > 0 &&
                <div>
                    <VideoCarrouselSlick
                        pager={seriesPager}
                        videos={Seriesvideos}
                        handleVideoSelect={handleSeriesSelect}
                        reset={reset}
                        refresh={refresh}
                    />
                </div>
                }
            </div>
        );
}
export default SeriesCarousel;
