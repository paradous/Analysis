
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
                '#blue'],

      plotOptions: {
        scatter: {
            marker: {
                radius: 7,
                symbol: 'circle'
            }
        }
    },

      title: {
        text: 'Clusters by PCA components',

    style: {
      fontSize: '36px'
    }
      },
      xAxis: {
        title: {
          text: 'Component 1 : WPath',

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
          text: 'Component 0 : MW',

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
        name: 'K-means PCA : 0',
        data: segment_1 },
      {
        name: 'K-means PCA : 1',
        data: segment_2 },
      {
        name: 'K-means PCA : 2',
        data: segment_3},
             {
        name: 'K-means PCA : 3',
        data: segment_4},
             {
        name: 'K-means PCA : 4',
        data: segment_5},
             {
        name: 'K-means PCA : 5',
        data: segment_6},
             {
        name: 'Added by user',
        data: segment_7}],
      credits: {
    enabled: false
},
turboThreshold: 100,
      tooltip: {
        formatter: function() {
          return '<b> odor : ' + this.point.odor + '</b><br><b>' + this.point.name + '</b><br>X: ' + this.x + '<br>Y: ' + this.y ;

        }
      }
    });


















