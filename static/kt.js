var count = 0;
var index_set=0;
var arrchart = new Array();
function start(){
    count_up();
    setInterval(count_up,1000*60);
}
function count_up(){
    console.log(count)
    index_set = count
    axios.post('http://localhost:5000/test', {
    index: index_set,
    })
  .then(response=> {
    datas = JSON.parse(response.data)
    twoweeksdata = datas.data
    console.log(twoweeksdata.length)
    console.log(twoweeksdata)
    arrchart.push(['X', 'Y', {'type': 'string', 'role': 'style'}])
    for(i=0;i<twoweeksdata.length;i++){
    arrchart.push([twoweeksdata[i]["timestamp"],twoweeksdata[i]["value"],twoweeksdata[i]["is_anom"]])}
    console.log(arrchart)
    drawChart(arrchart)
    count = count+1
    arrchart = [];
    })
  .catch(error=> {
    console.log(error);
    });
}

