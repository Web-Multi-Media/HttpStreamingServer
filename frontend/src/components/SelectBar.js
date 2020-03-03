import React from 'react';


const SelectBar = (props) => {

    const { seasons, handleSeason} = props;
    const options = seasons.map(season => {
        return <option key={season} value={season}>S {season}</option>;
    });
    return (
            <select className="centerVer" onChange={handleSeason}>
                {options}
            </select>
    );
};
export default SelectBar;
