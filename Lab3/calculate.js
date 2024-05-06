function disp(val) {
    document.getElementById("display").value += val
}
function clearDisplay(){
    document.getElementById("display").value = ""
} 
function result(){
    let x = document.getElementById("display").value
    if (x.includes("pow")) {
        const firstNo = x.split('pow(')[0];
        const secondNo = x.split('pow(')[1].slice(-2,1);
        let y = math.pow(firstNo, secondNo)
        document.getElementById("display").value = y;
    }
    else{
    let y = math.evaluate(x)
    document.getElementById("display").value = y;
    }
}