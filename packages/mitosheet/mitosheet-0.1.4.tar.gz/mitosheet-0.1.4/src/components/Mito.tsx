import React from 'react';

// Import types
import { SheetJSON, CodeJSON } from '../widget';

// Import sheet and code components
import MitoSheet from './MitoSheet';
import Codeblock from './Codeblock';

type MitoProps = {
    sheetJSON: SheetJSON;
    codeJSON: CodeJSON;
    send: any
};
type MitoState = {
    sheetJSON: SheetJSON;
    codeJSON: CodeJSON;
};


class Mito extends React.Component<MitoProps, MitoState> {

    constructor(props: MitoProps) {
        super(props);
        this.state = {
            sheetJSON: this.props.sheetJSON,
            codeJSON: this.props.codeJSON,
        };

        setInterval(() => {
            // For now, we simulate an editing event every 10 seconds. 
            console.log("Creating an new fake editing event");
            this.props.send({
                'type': 'edited' 
            })
        }, 2000);
    }

    render() {
        return (
            <div>
                <MitoSheet sheetJSON={this.state.sheetJSON}/>
                <Codeblock codeJSON={this.state.codeJSON}/>
            </div>
        );
    }

}


export default Mito;