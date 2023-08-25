
// Set up the chart
    Highcharts.chart('container', {
      chart: {
        type: 'scatter',
        zoomType: 'xy',
        height: 1000, // set the height
        width: 1000 // set the width
      },
             legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        x: 70,
        y: 50,
        floating: true,
        borderWidth: 1,
        backgroundColor: '#FFFFFF'
    },
            colors: ['#8c0fe8',
                '#ff5733',
                '#23bd10',
                '#d6e519',
                '#f03312',
                '#f012cb',
                '#1292f0',
                '#12f0cb',
                '#9ca2a1'],

      plotOptions: {
        scatter: {
            marker: {
                radius: 7,
                symbol: 'circle'
            }
        }
    },

      title: {
        text: 'PCA Distribution',

    style: {
      fontSize: '36px'
    }
      },
      xAxis: {
        title: {
          text: 'First principal component',

    style: {
      fontSize: '24px'
    }
        },
        labels: {
    style: {
      fontSize: '12px'
    }
  }
      },
      yAxis: {
        title: {
          text: 'Second principal component',

    style: {
      fontSize: '24px'
    }
        },
        labels: {
    style: {
      fontSize: '12px'
    }
  }
      },
      series: [{
        name: 'Odor : Berry',
        data: odor_berry },
      {
        name: 'Odor : Alliaceaous',
        data: odor_alliaceaous },
      {
        name: 'Odor : Coffee',
        data: odor_coffee},
             {
        name: 'Odor : Citrus',
        data: odor_citrus},
             {
        name: 'Odor : Fishy',
        data: odor_fishy},
             {
        name: 'Odor : Jasmine',
        data: odor_jasmine},
             {
        name: 'Odor : Minty',
        data: odor_minty},
             {
        name: 'Odor : Earthy',
        data: odor_earthy},
             {
        name: 'Odor : Smoky',
        data: odor_smoky}],
      credits: {
    enabled: false
},
turboThreshold: 100,
      tooltip: {
        formatter: function() {
          return '<b>' + this.point.name + '</b><br>X: ' + this.x + '<br>Y: ' + this.y ;

        }
      }
    });


















