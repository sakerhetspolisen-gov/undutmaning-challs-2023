function get_stats() {
    fetch('/api/stats/status')
    .then(response => response.text())
    .then(text => document.getElementById('stats').innerText = text.match(/^Pid.*|VmPeak.*|VmSize.*|VmData.*|Threads.*|VmSwap.*/gm).join('\n'));
}
get_stats();
setInterval(function() {
    get_stats();
}, 5000);
