import React from 'react';


const SelectBar = (props) => {

    const { seasons, handleSeason} = props;
    const options = seasons.map(season => {
        return <option  value={season}>S {season}</option>;
    });
    return (
        <div>
            <select onChange={handleSeason}>
                {options}
            </select>
        </div>
    );
};
export default SelectBar;





