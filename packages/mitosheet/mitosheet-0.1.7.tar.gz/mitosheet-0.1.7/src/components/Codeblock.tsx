import React from 'react';

// Import types
import { CodeJSON } from '../widget';


const Codeblock = (props : {codeJSON: CodeJSON}): JSX.Element => {

    return (
        <div className="mito-codeblock">
            {props.codeJSON['code']}
        </div>
    );

}


export default Codeblock;