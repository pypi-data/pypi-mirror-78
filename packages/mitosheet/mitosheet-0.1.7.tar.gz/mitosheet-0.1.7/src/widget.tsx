// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

// React
import React from 'react';
import ReactDOM from 'react-dom';

// Components
import Mito from './components/Mito';

export class ExampleModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: ExampleModel.model_name,
      _model_module: ExampleModel.model_module,
      _model_module_version: ExampleModel.model_module_version,
      _view_name: ExampleModel.view_name,
      _view_module: ExampleModel.view_module,
      _view_module_version: ExampleModel.view_module_version,
      df_json: '',
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'ExampleModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'ExampleView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

// We save a Mito component in the global scope, so we
// can set the state from outside the react component
declare global {
  interface Window { Mito: any; }
}

export interface SheetJSON {
  columns: string[];
  index: string[];
  data: string[][];
}

export interface CodeJSON {
  code: string;
}

export class ExampleView extends DOMWidgetView {
  render() {
    const send = (msg: {}) => {
      this.send(msg);
    }

    // TODO: there is a memory leak, in the case where
    // we rerender the component (e.g. we run the mito.sheet)
    // cell again. We need to clean up the component somehow!
    ReactDOM.render(
        <Mito 
          sheetJSON={this.getSheetJSON()}
          codeJSON={this.getCodeJSON()}
          send={send}
          ref={(Mito : any) => { window.Mito = Mito }}
          />,
        this.el
    )
    this.model.on('msg:custom', this.handleMessage, this);
  }

  getSheetJSON(): SheetJSON {
    let sheetJSON: SheetJSON = {
      columns: [],
      index: [],
      data: []
    };

    const unparsedSheetJSON = this.model.get('sheet_json');
    try {
      sheetJSON['columns'] = JSON.parse(unparsedSheetJSON)['columns'];
      sheetJSON['index'] = JSON.parse(unparsedSheetJSON)['index'];
      sheetJSON['data'] = JSON.parse(unparsedSheetJSON)['data'];
    } catch (e) {
      // Suppress error
    }

    return sheetJSON;
  }

  getCodeJSON(): CodeJSON {
    let codeJSON: CodeJSON = {
      code: '# No code has been written yet!'
    };

    const unparsedCodeJSON = this.model.get('code_json');
    try {
      codeJSON['code'] = JSON.parse(unparsedCodeJSON)['code'];
    } catch (e) {
      // Suppress error
    }

    return codeJSON;
  }



  handleMessage(message : any) {
    /* 
      This route handles the messages sent from the Python widget
    */

    console.log("Got a message, ", message);
    if (message.type === 'update_sheet') {
      console.log("Updating sheet");


    } else if (message.type === 'update_code') {
      console.log("Updating code 1");
      const code_json = this.model.get('code_json');
      if (code_json !== '') {
        window.Mito.setState({
          codeJSON: JSON.parse(code_json)
        });
      }
    }
  }
}
