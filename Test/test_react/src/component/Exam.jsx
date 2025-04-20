import React from 'react'
import { useState, useEffect } from 'react';

export default function Exam(props) {

    const input = props.input;
    const [time, setTime] = useState(new Date());

    useEffect(()=>{
        const clock = setInterval(() => setTime(new Date(), 1000));

        return ()=> {clearInterval(clock)};
    },[]);

    if(input === false){
        return (
            <div>{time.toLocaleString()}</div>
        )
    }else if(Array.isArray(input)){
        return (
            <div>
                {input.map((ele)=>{return (<li>{ele}</li>)})}
            </div>
        )
    }else{
        return (
            <div>{input}</div>
        )
    }
}
