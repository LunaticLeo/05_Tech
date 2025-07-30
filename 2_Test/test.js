function solution(startTime, finishTime) {
    const digitCount = Array(10).fill(0);
    
    function toSeconds([h,m,s]){
        return h*3600+m*60+s;
    }
    
    function fromSeconds(totalSeconds){
        const h = Math.floor(totalSeconds/3600);
        const m = Math.floor((totalSeconds%3600)/60);
        const s = Math.floor(totalSeconds%60);
        
        return [
            h.toString().padStart(2,'0'),
            m.toString().padStart(2,'0'),
            s.toString().padStart(2,'0')
        ];
    }
    
    let start = toSeconds(startTime);
    let end = toSeconds(finishTime);
    
    for(let t = start;t<=end;t++){
        const [hh,mm,ss] = fromSeconds(t);
        const timeStr = hh+mm+ss;
        for(const char of timeStr){
            digitCount[parseInt(char)]++;
        }
    }
    return digitCount;
}
