import React from 'react';


const selectBar = (props) => {

    const { seasons } = props;
    const options = seasons.map(season => {
        return <option value="season">`S${season}`</option>;
    });
    return (
        <div>
            <select>
                {options}
            </select>
        </div>
    );
};
export default selectBar;





