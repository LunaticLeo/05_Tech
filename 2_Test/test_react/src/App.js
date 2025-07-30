import logo from './logo.svg';
import './App.css';

import React, {useEffect, useState} from 'react';
import Exam from './component/Exam';

function App() {

  return (
    <div className="App">
      <Exam input={false}></Exam>
      <Exam input={[1,2,3]}></Exam>
      <Exam input={"input"}></Exam>
    </div>
  );
}

export default App;
