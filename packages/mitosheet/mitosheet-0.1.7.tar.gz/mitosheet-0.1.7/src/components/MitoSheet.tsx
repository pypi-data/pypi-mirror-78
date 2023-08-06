import React from 'react';

// Import types
import { SheetJSON } from '../widget';

function buildTableData(df_json : {data: string[][]}) {
    return df_json['data']?.map((row, index) => {
        return (
            <tr key={index}>
                {row.map((value, idx) => {
                    return <td key={index + "-" + idx}>{value}</td>
                })}
           </tr>
        )
    });
}

const MitoSheet = (props : {sheetJSON: SheetJSON}): JSX.Element => {
    return (
        <div className="mito-sheet">
            <table id='mito-sheet'>
                <tbody>
                    {buildTableData(props.sheetJSON)}
                </tbody>
            </table>
        </div>
    );
}


export default MitoSheet;