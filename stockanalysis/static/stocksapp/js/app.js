
$(document).ready(function() {
    $("#companytickers").on('change', function(){   //Function to support the AJAX query for retrieving the Company Data
      var company_id = document.getElementById('companytickers').value;
      if (company_id != 'invalid'){
      $.ajax({
        url: "../company_overview/"+company_id, //create a REST like endpoint
        dataType: 'json',
        success: function (data2) { //On Success, Populate the Required Fields
            document.getElementById('name').innerHTML = "<strong>"+ data2['name']+ "</strong>";
            document.getElementById('description').innerHTML = data2['description'];
            document.getElementById('gics_sector').innerHTML = '<strong>Gics Sector:</strong> ' + data2['gics_sector'];
            document.getElementById('gics_industry').innerHTML = '<strong>Gics Industry:</strong> ' + data2['gics_industry'];
            document.getElementById('gics_industry_group').innerHTML = '<strong>Gics Industry Group:</strong> ' + data2['gics_industry_group'];
            document.getElementById('gics_sub_industry_group').innerHTML = '<strong>Gics Sub Industry Group:</strong> ' + data2['gics_sub_industry_group'];

            var company_id =  data2['company_id'];
            $.getJSON('../get_json/'+company_id, function (data) {  //for the given company-id, get the price data & populate Highcharts
                // split the data set into ohlc and volume
                var stock = [],
                    volume = [],
                    dataLength = data.length,
                    // set the allowed units for data grouping
                    groupingUnits = [[
                        'week',                         // unit name
                        [1]                             // allowed multiples
                    ], [
                        'month',
                        [1, 2, 3, 4, 6]
                    ]],

                    i = 0;

                for (i; i < dataLength; i += 1) {
                    stock.push([
                        Date.parse(data[i][0]), // the date
                        data[i][1] // close
                    ]);

                    volume.push([
                        Date.parse(data[i][0]), // the date
                        data[i][2] // the volume
                    ]);
                }


                // create the chart
                var chart = Highcharts.stockChart('stock-chart', {

                    rangeSelector: {
                        selected: 4
                    },

                    title: {
                        text: 'Stocks Data'
                    },

                    yAxis: [{
                        labels: {
                            align: 'right',
                            x: -3
                        },
                        title: {
                            text: 'Price'
                        },
                        height: '60%',
                        lineWidth: 2,
                        resize: {
                            enabled: true
                        }
                    }, {
                        labels: {
                            align: 'right',
                            x: -3
                        },
                        title: {
                            text: 'Volume'
                        },
                        top: '65%',
                        height: '35%',
                        offset: 0,
                        lineWidth: 2
                    }],

                    tooltip: {
                        split: true
                    },

                    series: [{
                        type: 'area',
                        name: $('#companytickers option:selected').text(),
                        data: stock,
                        dataGrouping: {
                            units: groupingUnits
                        }
                    }, {
                        type: 'column',
                        name: 'Volume',
                        data: volume,
                        yAxis: 1,
                        dataGrouping: {
                            units: groupingUnits
                        }
                    }],
                    responsive: {
                        rules: [{
                            condition: {
                                maxWidth: 500
                            },
                            chartOptions: {
                                chart: {
                                    height: 400
                                },
                                subtitle: {
                                    text: null
                                },
                                navigator: {
                                    enabled: false
                                }
                            }
                        }]
                    }

                });
                $('#small').click(function () {
                    chart.setSize(400);
                });

                $('#large').click(function () {
                    chart.setSize(800);
                });

                $('#auto').click(function () {
                    chart.setSize(null);
                });

            });


        }
      });
    }
  });

  $('#confirm-delete').on('show.bs.modal', function(e) {
          $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
  });







//STOCK stock_comparisons

$("#tickerB").on('change', function(){    //Function to support AJAX loading for Compnay Information
  var companyA = document.getElementById('tickerA').value;
  var companyB = document.getElementById('tickerB').value;

  if(companyA!='invalid' && companyB!='invalid'){
    $.ajax({
      url: "../company_comparison_endpoint/",
      type:'GET',
      data:{'companyA':companyA, 'companyB':companyB},  //Pass the ticker information to the backend
      dataType: 'json',
      success: function (data2) {
            var dataPoints =  data2['dataPoints'];
            var date_range = data2['date_range'];
            var fitted_line = data2['fitted_line'];
            dataLength = data2.length,



          // create the chart
          Highcharts.chart('stock-chart-comparisons', {

              title: {
                  text: 'Correlation Analysis'
              },

              xAxis: {
                title: {
                    text: data2['tickerA']
                }
              },
              yAxis: {
                  title: {
                  text: data2['tickerB']
                  }
              },
              series: [{
                    type: 'line',
                    name: 'Regression Line',
                    data: fitted_line,
                    lineWidth:3,
                    color:'green',
                    marker: {
                        enabled: false
                    },
                    states: {
                        hover: {
                            lineWidth: 0
                        }
                    },
                    enableMouseTracking: false
                },{
                  type: 'scatter',
                  name: 'Observations',
                  data: dataPoints,
                  marker: {
                      symbol:'diamond',
                      radius: 4,
                      fillColor:'red',
                  }
              }]
          });

    }
  });
}
else{
  console.log('Waiting for user to select a ticker')
}


});


// JQUERY FOR LIVE PRICING-------------------------------------------------------------------

$("#liveTicker").on('change', function(){
  $('#myModal').modal('show');
  setTimeout(function(){
       $('#myModal').modal('hide');
   }, 6500);
  var ticker = $('#liveTicker').val();
  ticker = ticker.split(' ')[0];
  $.getJSON('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+ticker+'&interval=1min&outputsize=full&apikey=HSA4DNUXIR916MIH', function(data) {
  var plotData = [],
    i = 0;
    var keus = Object.keys(data)[1];
  for(i ; i < Object.keys(data[keus]).length; i++){
      var keusVal = Object.keys(data[keus])[i];
      var open = Object.keys(data[keus][keusVal])[0];
      var price = data[keus][keusVal][open]
      plotData.push(parseFloat(price));

    }
  // create the chart
  Highcharts.stockChart('live-stock-graph', {
    chart: {
      events: {
        load: function() {
          // set up the updating of the chart each second
          var series = this.series[0];
          setInterval(function() {
            //https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+ticker+'&interval=1min&outputsize=full&apikey=HSA4DNUXIR916MIH
            $.getJSON('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+ticker+'&interval=1min&outputsize=full&apikey=HSA4DNUXIR916MIH', function(intervalData) {
              var interval_keys = Object.keys(intervalData)[1];
              console.log(Object.keys(intervalData));
              console.log(interval_keys);
              if (Object.keys(intervalData[interval_keys]).length > plotData.length) {
                var interval_keusVal = Object.keys(intervalData[interval_keys])[0];//latest data
                console.log('interval_keus val is:');
                console.log(interval_keusVal);
                var x = Object.keys(intervalData[interval_keys][interval_keusVal])[0]; // current time
                console.log('Value of X is:');
                console.log(x);
                var prices = intervalData[interval_keys][interval_keusVal][x]
                series.addPoint(parseFloat(prices), true, true);
                plotData.push(parseFloat(prices));
              }
            });
            console.log(plotData);
          }, 7000)

        }
      }
    },
    title: {
      text: ticker.toUpperCase()+' stock price by minute'
    },


    xAxis: {
      gapGridLineWidth: 0,
      labels: {
            enabled: false
        }
    },
    rangeSelector: {
      enabled: false
    },

    series: [{
      name: ticker.toUpperCase(),
      type: 'area',
      data: plotData,
      gapSize: 5,
      tooltip: {
        valueDecimals: 2
      },
      fillColor: {
        linearGradient: {
          x1: 0,
          y1: 0,
          x2: 0,
          y2: 1
        },
        stops: [
          [0, Highcharts.getOptions().colors[0]],
          [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
        ]
      },
      threshold: null
    }]
  });
});

});

});

