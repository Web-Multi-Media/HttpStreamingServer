import React from 'react';


const SelectBar = (props) => {

    const { seasons, handleSeason} = props;
    const options = seasons.map(season => {
        return <option key={season} value={season}>S {season}</option>;
    });
    return (
        <div className="seriesDisplay">
            <select onChange={handleSeason}>
                {options}
            </select>
        </div>
    );
};
export default SelectBar;
