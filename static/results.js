(function(){
  let app = new Vue({
    el: '#app',
    data: {
      results: []
    },
    mounted: function () {
      axios.get('/api/results').then(function(data) {
        app.results = data.data;
        chartSetup(data.data);
      });
    }
  });

  function chartDataConversion(data) {
    let max = Math.max(
      ...data.map(i => i.download),
      ...data.map(i => i.upload)
    );

    let count = 0;
    while (Math.abs(max) > 1000) {
      max /= 1024;
      count++;
    }

    console.log(max, count);

    let download = data.map(function(i){
      return {
        x: moment(i.timestamp),
        y: (i.download / Math.pow(1024, count)).toFixed(2)
      }
    });

    let upload = data.map(function(i){
      return {
        x: moment(i.timestamp),
        y: (i.upload / Math.pow(1024, count)).toFixed(2)
      }
    });

    let color = Chart.helpers.color;
    let red = 'rgb(255, 99, 132)';
    let blue = 'rgb(54, 162, 235)';

    return [{
      label: 'Download speed',
      fill: false,
      backgroundColor: color(red).alpha(0.5).rgbString(),
      borderColor: red,
      data: download
    }, {
      label: 'Upload speed',
      fill: false,
      backgroundColor: color(blue).alpha(0.5).rgbString(),
      borderColor: blue,
      data: upload
    }]
  }

  function chartSetup(data) {
    let myChart = new Chart('chart', {
      type: 'line',
      data: {
        datasets: chartDataConversion(data)
      },
			options: {
				title: {
					text: 'Download/Upload chart'
				},
				scales: {
					xAxes: [{
						type: 'time',
						time: {
							parser: 'DD/MM/YYYY HH:mm',
							//round: 'hour',
							tooltipFormat: 'll HH:mm'
						},
						scaleLabel: {
							display: true,
							labelString: 'Date'
						}
					}],
					yAxes: [{
						scaleLabel: {
							display: true,
							labelString: 'value'
						},
            ticks: {
                beginAtZero: true
            }
					}]
				},
			}
    });
  }
})();