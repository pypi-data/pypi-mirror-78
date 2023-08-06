import React, { useState } from 'react';

const App = (props : {message : string}): JSX.Element => {
    const [counter, setCounter] = useState(0);

    return (
        <div>
            <p>You clicked {counter} times!</p>
            <button
                onClick={(): void => {
                    setCounter(counter + 1);
                }}
            >
                {props.message}
            </button>
        </div>
    );
};

export default App;